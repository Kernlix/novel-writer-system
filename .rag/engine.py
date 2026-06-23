"""
NovelRAG — 本地 RAG 引擎

基于 ChromaDB + Ollama (qwen3-embedding:4b) 的网文语义检索系统。
支持对章节、人物卡、设定文件的索引与检索。
"""

import hashlib
import json
import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

import chromadb
import ollama
from chromadb import Documents, EmbeddingFunction, Embeddings


# ---------------------------------------------------------------------------
# Custom embedding function wrapping Ollama
# ---------------------------------------------------------------------------

class OllamaEmbed(EmbeddingFunction):
    """ChromaDB embedding function backed by an Ollama model.""ENDCLASS"""

    def __init__(self, model: str = "qwen3-embedding:4b"):
        self.model = model

    def __call__(self, input: Documents) -> Embeddings:
        # Ollama supports batched input via embeddings() but we iterate to
        # stay safe across model versions.
        results: list[list[float]] = []
        for doc in input:
            resp = ollama.embeddings(model=self.model, prompt=doc)
            results.append(resp["embedding"])
        return results


# ---------------------------------------------------------------------------
# Chunking helpers
# ---------------------------------------------------------------------------

def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    """Split a long document into overlapping chunks (by character count)."""
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


def _clean_markdown(text: str) -> str:
    """Strip markdown heading markers, but keep content."""
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    return text.strip()


# ---------------------------------------------------------------------------
# Cross-encoder reranker (sentence-transformers via FastAPI)
# ---------------------------------------------------------------------------

class Reranker:
    """Cross-encoder reranker backed by a local FastAPI service.

    The service runs Qwen3-Reranker-0.6B via sentence-transformers.
    Expected endpoint: POST /v1/rerank
      Request:  {"query": str, "documents": [str, ...], "top_n": int|null}
      Response: {"results": [{"index": int, "relevance_score": float}, ...]}
    """

    def __init__(
        self,
        api_url: str = "http://127.0.0.1:8081/v1/rerank",
        top_n: int | None = None,
        timeout: int = 180,
    ):
        self.api_url = api_url
        self.top_n = top_n
        self.timeout = timeout

    def rerank(self, query: str, documents: list[str]) -> list[tuple[int, float]]:
        """Sort documents by relevance to *query*.

        Returns [(original_index, score), ...] sorted descending by score.
        """
        payload = json.dumps(
            {
                "query": query,
                "documents": documents,
                "top_n": self.top_n,
            }
        ).encode("utf-8")

        req = urllib.request.Request(
            self.api_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            raise RuntimeError(f"Reranker API call failed: {exc}") from exc

        results = data.get("results", [])
        sorted_results = sorted(results, key=lambda x: x["relevance_score"], reverse=True)
        return [(r["index"], r["relevance_score"]) for r in sorted_results]


# ---------------------------------------------------------------------------
# Main RAG engine
# ---------------------------------------------------------------------------

class NovelRAG:
    """Lightweight local RAG for Chinese web novel project.""ENDCLASS"""

    def __init__(
        self,
        novel_root: str | Path,
        cache_dir: str | Path | None = None,
        embedding_model: str = "qwen3-embedding:4b",
        collection_prefix: str = "",
    ):
        self.novel_root = Path(novel_root).resolve()
        self.embedding_model = embedding_model

        # Default cache lives beside the project
        if cache_dir is None:
            cache_dir = self.novel_root / ".rag"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Chroma client (persistent)
        self.client = chromadb.PersistentClient(
            path=str(self.cache_dir / "chroma_db")
        )

        # Collection names (must be ASCII-safe)
        if collection_prefix:
            prefix = collection_prefix
        else:
            prefix = self._collection_prefix()
        self.collections: dict[str, chromadb.Collection] = {}
        embed_fn = OllamaEmbed(model=embedding_model)

        for name in ("chapters", "characters", "outlines", "settings"):
            cname = f"{prefix}_{name}"
            try:
                col = self.client.get_collection(name=cname, embedding_function=embed_fn)
            except (ValueError, chromadb.errors.NotFoundError):
                col = self.client.create_collection(
                    name=cname,
                    embedding_function=embed_fn,
                    metadata={"hnsw:space": "cosine"},
                )
            self.collections[name] = col

    DEFAULT_RERANK_K: int = 10

    def _collection(self, kind: str) -> chromadb.Collection:
        col = self.collections.get(kind)
        if col is None:
            msg = f"Unknown collection kind: {kind}, choose from {list(self.collections)}"
            raise KeyError(msg)
        return col

    def index_file(
        self,
        kind: str,
        file_path: str | Path,
        *,
        doc_id: str | None = None,
        metadata: dict | None = None,
    ) -> int:
        """Index a single markdown file into *kind* collection.

        Returns number of chunks indexed.
        """
        path = Path(file_path).resolve()
        text = path.read_text(encoding="utf-8")
        text = _clean_markdown(text)

        if not text.strip():
            return 0

        chunks = _chunk_text(text)
        doc_id = doc_id or path.stem
        meta = {"source": str(path.relative_to(self.novel_root)), "file": path.name}
        if metadata:
            meta.update(metadata)

        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{**meta, "chunk_index": i} for i in range(len(chunks))]

        col = self._collection(kind)
        # Upsert: remove existing doc first to avoid duplicates
        try:
            existing = col.get(ids=[f"{doc_id}_chunk_0"])
            if existing["ids"]:
                col.delete(ids=[f"{doc_id}_chunk_{i}" for i in range(len(chunks))])
        except Exception:
            pass

        col.add(documents=chunks, ids=ids, metadatas=metadatas)
        return len(chunks)

    def index_directory(
        self,
        kind: str,
        directory: str | Path,
        pattern: str = "*.md",
        *,
        base_id: str | None = None,
        metadata_factory=None,
    ) -> int:
        """Index all matching files in a directory.

        Returns total chunk count.
        """
        total = 0
        for fp in sorted(Path(directory).glob(pattern)):
            doc_id = base_id or fp.stem
            meta = metadata_factory(fp) if metadata_factory else {}
            total += self.index_file(kind, fp, doc_id=doc_id, metadata=meta)
        return total

    def index_novel(self) -> dict[str, int]:
        """Convenience: index the whole novel project at once.

        Returns {collection_kind: chunk_count}.
        """
        stats: dict[str, int] = {}

        chapters_dir = self.novel_root / "章节"
        if chapters_dir.is_dir():
            stats["chapters"] = self.index_chapters(chapters_dir)

        characters_dir = self.novel_root / "人物"
        if characters_dir.is_dir():
            stats["characters"] = self.index_directory("characters", characters_dir)

        outlines_dir = self.novel_root / "大纲"
        if outlines_dir.is_dir():
            stats["outlines"] = self.index_directory("outlines", outlines_dir)

        # Root-level setting files
        root_settings = list(self.novel_root.glob("*.md"))
        root_settings = [
            p
            for p in root_settings
            if p.stem
            not in (
                "novel_design_document",
                "whimsical-humming-lynx",
                "cover",
            )
        ]
        count = 0
        for fp in root_settings:
            count += self.index_file("settings", fp, doc_id=f"root_{fp.stem}")
        stats["settings"] = count

        return stats

    def index_chapters(self, chapters_dir: str | Path) -> int:
        """Index all chapter files, enriched with chapter-number metadata."""
        total = 0
        for fp in sorted(Path(chapters_dir).glob("*.md")):
            m = re.search(r"(\d+)", fp.stem)
            chap_num = int(m.group(1)) if m else 0
            total += self.index_file(
                "chapters",
                fp,
                doc_id=f"ch{chap_num:04d}",
                metadata={"chapter": chap_num},
            )
        return total

    # ----- Querying --------------------------------------------------------

    def query(
        self,
        query_text: str,
        kinds: list[str] | None = None,
        n_results: int = 5,
        where: dict | None = None,
        reranker: Reranker | None = None,
        rerank_k: int | None = None,
    ) -> dict[str, list]:
        """Search across one or more collections.

        When *reranker* is provided, the pipeline is:
          initial_retrieve(k=rerank_k) → reranker.sort() → top_n(n_results)

        Args:
            query_text: Natural language query.
            kinds: Which collections to search (default: all).
            n_results: Results per collection.
            where: Optional chroma filter dict.
            reranker: Optional ``Reranker`` instance for cross-encoder re-ranking.
            rerank_k: Initial retrieval count before re-ranking (only used when
                      ``reranker`` is not None).

        Returns:
            {collection_kind: [{id, document, metadata, distance}, ...]}
        """
        if kinds is None:
            kinds = list(self.collections)

        out: dict[str, list] = {}
        for kind in kinds:
            col = self._collection(kind)
            fetch_k = (rerank_k or self.DEFAULT_RERANK_K) if reranker else n_results
            try:
                results = col.query(
                    query_texts=[query_text],
                    n_results=fetch_k,
                    where=where,
                )
            except Exception:
                continue

            items = []
            if results["ids"]:
                for i in range(len(results["ids"][0])):
                    items.append(
                        {
                            "id": results["ids"][0][i],
                            "document": results["documents"][0][i],
                            "metadata": results["metadatas"][0][i],
                            "distance": results["distances"][0][i]
                            if results.get("distances")
                            else None,
                        }
                    )

            # Re-rank with cross-encoder if provided
            if reranker and len(items) > 1:
                docs = [it["document"] for it in items]
                try:
                    ranked = reranker.rerank(query_text, docs)
                    items = [items[idx] for idx, _ in ranked[:n_results]]
                except RuntimeError:
                    # Fall back to Chroma ranking if reranker fails
                    items = items[:n_results]
            elif reranker:
                pass  # single item, nothing to re-rank

            out[kind] = items
        return out

    def query_chapters(
        self, query_text: str, n_results: int = 5, reranker: Reranker | None = None
    ) -> list[dict]:
        """Shorthand: search only chapters."""
        return self.query(query_text, kinds=["chapters"], n_results=n_results, reranker=reranker)[
            "chapters"
        ]

    # ----- Info / stats ----------------------------------------------------

    def collection_info(self) -> dict[str, int]:
        """Return {kind: document_count} for each collection."""
        info: dict[str, int] = {}
        for kind, col in self.collections.items():
            info[kind] = col.count()
        return info

    def _collection_prefix(self) -> str:
        """Return the ASCII-only prefix used for ChromaDB collection names."""
        raw = self.novel_root.name.encode("utf-8")
        return "n" + hashlib.sha256(raw).hexdigest()[:10]

    def wipe_collection(self, kind: str) -> None:
        """Delete and recreate a collection (for re-indexing)."""
        prefix = self._collection_prefix()
        cname = f"{prefix}_{kind}"
        embed_fn = OllamaEmbed(model=self.embedding_model)
        try:
            self.client.delete_collection(cname)
        except ValueError:
            pass
        self.collections[kind] = self.client.create_collection(
            name=cname,
            embedding_function=embed_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def wipe_all(self) -> None:
        """Delete all collections for this novel."""
        for kind in list(self.collections):
            self.wipe_collection(kind)
