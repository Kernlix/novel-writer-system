# 以管理员身份运行此脚本来创建计划任务
# 右键 → 以管理员身份运行 PowerShell，然后执行此脚本

$taskName = "NovelReranker"
$python = "C:\Python314\python.exe"
$script = "D:\allproject\GitHub项目\novel-writer-system\.rag\server_reranker.py"
$workDir = "D:\allproject\GitHub项目\novel-writer-system\.rag"

# 删除旧任务
schtasks /Delete /TN $taskName /F 2>$null | Out-Null

$action = New-ScheduledTaskAction -Execute $python -Argument "$script --port 8081" -WorkingDirectory $workDir
$trigger = New-ScheduledTaskTrigger -AtLogon
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit 0
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force

Write-Host "Done! Task [$taskName] created."
