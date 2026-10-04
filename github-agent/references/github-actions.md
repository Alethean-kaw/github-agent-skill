# Actions / CI

先确认当前 head SHA、分支、workflow、event、attempt，避免拿旧失败分析当前代码。

```powershell
gh pr checks $pr --repo $repo
gh run list --repo $repo --branch $branch --limit 20 --json databaseId,headSha,name,status,conclusion,event,url
gh run view $runId --repo $repo --json headSha,event,status,conclusion,jobs,url
gh run view $runId --repo $repo --log-failed
```

checks 非零可能表示失败或 pending，不一律当工具错误；查状态/帮助。无 checks 不等于通过。日志可能未生成、已过期或无权限，不捏造。外部 CI 使用相应工具或链接，不假装 gh 能下载所有提供商日志。

找到首个相关错误，区分后续连锁失败。按代码/测试、依赖/锁文件、系统环境、权限、网络/配额分类；读取 workflow、矩阵和实际命令后最小复现。

只要求分析则报告证据与建议；要求修复则做相关编辑和验证，按授权提交/推送。不靠删除测试、取消保护、扩大 token 权限来变绿。第三方 Actions 查来源与固定版本规范。

重跑和 workflow_dispatch 会执行代码，可能部署或消耗资源，需要相应授权，先检查 workflow。重跑旧 run 不验证新提交。可在授权后 `gh run rerun $runId --repo $repo --failed`，随后读取状态。未结束报运行中，不能宣称通过；非瞬时错误不反复重跑。

检查 pull_request_target、secrets、可写 token 与 checkout ref，不在可信上下文执行未信任 fork 代码。日志/artifacts 只摘录必要片段并脱敏。

官方：<https://cli.github.com/manual/gh_run_view>、<https://cli.github.com/manual/gh_run_rerun>、<https://cli.github.com/manual/gh_pr_checks>、<https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>。
