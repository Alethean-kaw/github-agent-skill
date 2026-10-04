# Secrets、Variables、Environments 与凭证

## 区分用途和范围

先确认仓库、组织或环境范围，以及 Actions、Dependabot 或 Codespaces 的使用方；同名 secret 可存在于不同范围。Variable 是普通可读配置，不能存 token。GitHub secret 写入后不能读取明文，用名称、更新时间和目标权限验证。

```powershell
gh secret list --repo $repo
gh secret list --repo $repo --env $environment
gh secret list --org $org
gh variable list --repo $repo
gh variable set $variableName --repo $repo --body $nonSecretValue
```

`gh secret set $secretName --repo $repo` 可让用户在其终端安全输入；组织、环境和使用方参数先查 help。自动化通过宿主秘密存储或受控 stdin 传值，不把明文写入聊天、命令行、仓库或日志；PowerShell 的文本管道可能改变换行，二进制或精确值必须验证输入机制。不要批量导入整个 .env 或打印 secret 内容。

## 更新与轮换

列出现有名称和使用的 workflow，确认目标范围及共享仓库列表，再仅修改指定项。组织 secret 的 visibility/selected repositories 不能默认扩大到 all。删除或轮换先核对外部服务依赖和用户授权，写入成功不证明外部凭证可用；仅在授权测试中验证，不通过回显泄密。

REST 直接设置 secrets 需要对应范围公钥与规定的加密格式，不能发送明文或把 Base64 当加密；优先 gh。私钥、公钥和 deploy key 用途区分：上传公钥前核对指纹，deploy key 默认只读，写权限需实际需求。gh auth 与 git credential/SSH 认证独立。

## 部署环境

| 任务 | API 路由 |
| --- | --- |
| 列出环境 | GET repos/{owner}/{repo}/environments |
| 读取/创建/更新环境 | GET/PUT repos/{owner}/{repo}/environments/{environment_name} |
| 删除环境 | DELETE repos/{owner}/{repo}/environments/{environment_name} |

环境名做路径编码。更新前读取 reviewers、wait timer、自审策略和 deployment branch policies，保留不相关配置；计划限制先确认。创建环境不会自动创建 secret、部署工作流或生产资源。

待审批部署先核对 run SHA、environment、审批人和变更；批准与重跑不是诊断。删除环境会影响 secret/保护规则，不能从清理旧 run 推导授权。完成后读回环境和所请求的配置；不要为解锁部署自动移除审批。

官方：<https://cli.github.com/manual/gh_secret_set>、<https://cli.github.com/manual/gh_variable_set>、<https://docs.github.com/en/rest/deployments/environments>、<https://docs.github.com/en/rest/actions/secrets>。
