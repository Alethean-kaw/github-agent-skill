# Actions / CI

先确认当前 PR head SHA、分支、workflow、event、attempt 和实际 checkout SHA。pull_request 可能验证合并引用，pull_request_target 的运行上下文来自 base；不能只比较 run.headSha 就判断验证了哪份代码。结合 PR 关联、事件和 checkout 日志建立映射，避免拿旧失败分析当前代码。

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

## 工作流与运行管理

```powershell
gh workflow list --repo $repo
gh workflow view $workflow --repo $repo --yaml
gh workflow run $workflow --repo $repo --ref $ref -f environment=$environment
gh run watch $runId --repo $repo --exit-status
gh run cancel $runId --repo $repo
gh run download $runId --repo $repo --name $artifactName --dir $newDownloadDir
```

dispatch 的输入先从 workflow_dispatch schema 核对；示例 environment 仅用于确有该输入的工作流。工作流需要存在于默认分支等条件以当前文档为准。返回成功不一定包含 run ID；按 workflow、event、ref、SHA、时间查对应运行，多个候选时不能只选最新一条。

启用/禁用使用 `gh workflow enable/disable`，确认不会停止必要安全检查；取消运行后查最终状态和已发生的部署副作用。删除 run、artifact/cache 分别核对保留需求；批量删除先清单，不从 CI 排错推导删除授权。

## 创建和修改 CI

读取项目构建/测试命令、lockfile、支持系统、运行时版本和已有工作流。明确 push/PR/schedule/manual 触发条件、路径过滤、并发取消与超时。第三方 Actions 核验来源并固定完整 commit SHA，注释标注版本；仅授予任务所需权限。

按实际风险使用矩阵而非随意排列版本。fork PR 使用 pull_request 的低权限上下文，禁止 pull_request_target checkout 不可信代码再配 secrets。actionlint 等工具只有实际可用才调用，不假称校验。

required checks 要保持名称稳定；路径过滤可能使保护检查长期等待。合并队列项目核对 merge_group 事件。可复用 workflow 核对 permissions、输入类型和 secrets 传递，避免宽泛 inherit。

## Artifact、缓存与 Runners

下载到新目录，验证 run/head SHA、名称、大小和内容；解包时防止路径穿越和符号链接越界，不执行未知产物。`gh cache list/delete` 先核对 key、ref 和大小，删除缓存可能增加后续耗时/费用。

自托管 runners / runner groups 用官方 Actions API 和目标组织策略；注册令牌、runner 凭证不能输出。核对工作负载隔离、标签、组访问、临时/持久类型和更新策略。不要让公开 fork 任意代码访问持久宿主或内网。调试优先最小日志，不启用全局秘密日志。

官方扩展：<https://cli.github.com/manual/gh_workflow_run>、<https://cli.github.com/manual/gh_run_download>、<https://cli.github.com/manual/gh_cache>、<https://docs.github.com/en/rest/actions/self-hosted-runners>。
