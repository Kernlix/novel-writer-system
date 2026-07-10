"""
灵境系统 Langfuse 追踪工具
所有 .rag/ 模块和 Agent 共享的追踪接口
"""
import os
import time
import functools

def _get_client():
    """延迟初始化，只在有密钥时创建"""
    from langfuse import get_client
    
    # 如果环境变量缺失，从配置文件读取
    if not os.environ.get('LANGFUSE_PUBLIC_KEY'):
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'langfuse_config.json')
        if os.path.exists(config_path):
            import json
            with open(config_path) as f:
                cfg = json.load(f)
            for k, v in cfg.items():
                env_key = f'LANGFUSE_{k.upper()}'
                if not os.environ.get(env_key):
                    os.environ[env_key] = v
    
    return get_client()

def trace_lcm_query(query: str, caller: str, result_len: int, duration_ms: float):
    """记录一次 LCM+RAG 查询"""
    try:
        lf = _get_client()
        with lf.start_as_current_observation(
            as_type="generation",
            name=f"lcm-rag [{caller}]",
            model="lcm+rag",
            input=query[:200],
            metadata={"caller": caller, "result_len": result_len, "duration_ms": duration_ms}
        ) as gen:
            gen.update(output=f"结果长度: {result_len} 字符, 耗时: {duration_ms:.0f}ms")
    except Exception:
        pass  # 追踪失败不影响主流程

def trace_agent_work(agent_name: str, task: str, output_len: int, duration_ms: float):
    """记录一次 Agent 工作任务"""
    try:
        lf = _get_client()
        with lf.start_as_current_observation(
            as_type="span",
            name=f"[{agent_name}] {task[:80]}",
            metadata={"agent": agent_name, "output_len": output_len, "duration_ms": duration_ms}
        ) as span:
            span.update(output=f"完成: {output_len} 字符, 耗时: {duration_ms:.0f}ms")
    except Exception:
        pass

class TraceContext:
    """上下文管理器，用于追踪一段代码执行"""
    def __init__(self, name: str, **metadata):
        self.name = name
        self.metadata = metadata
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        duration_ms = (time.time() - self.start_time) * 1000
        try:
            lf = _get_client()
            lf.create_event(
                name=self.name,
                metadata={**self.metadata, "duration_ms": duration_ms}
            )
        except Exception:
            pass

def flush():
    """确保追踪数据发送完毕"""
    try:
        _get_client().flush()
    except Exception:
        pass
