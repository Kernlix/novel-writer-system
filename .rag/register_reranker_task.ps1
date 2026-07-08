# 创建 NovelReranker 开机自启任务（方案 A — 任务计划程序）
$taskName = "NovelReranker"
$python   = "C:\Python314\python.exe"
$script   = "D:\allproject\GitHub项目\novel-writer-system\.rag\server_reranker.py"
$workDir  = "D:\allproject\GitHub项目\novel-writer-system\.rag"

# 删除旧任务
schtasks /Delete /TN $taskName /F 2>$null | Out-Null

# 创建任务：用户登录时启动，隐藏窗口，有限权限
$action = New-ScheduledTaskAction `
    -Execute $python `
    -Argument "`"$script`" --port 8081" `
    -WorkingDirectory $workDir

$trigger = New-ScheduledTaskTrigger -AtLogon

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit 0  # 永不超时终止

$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Limited

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Force | Out-Null

Write-Host "[OK] Task [$taskName] created. Reranker will start automatically at next logon."
