# 仓库生命周期与文件管理

## 检查与创建

```powershell
gh repo view $repo --json nameWithOwner,url,visibility,defaultBranchRef,isFork,parent
gh repo list $owner --limit 100
gh repo clone $repo $localPath
```

克隆到不存在或已确认空的目录；明确默认分支、浅克隆和子模块是否需要。新建仓库先核对账号/组织、名称、公开性和现有同名对象；`gh repo create $repo --private` 或 `--public` 只在用户已选择公开性后执行。导入已有项目先检查未跟踪文件、忽略规则、秘密、remote；授权上传时才使用 `--source`、`--remote`、`--push`，不覆盖已存在 origin。

从模板创建先读模板文件、许可及初始化脚本，再查 `gh repo create --template`；fork 先查 fork 是否存在，用 `gh repo fork $repo --clone=false`，复查 parent。fork 不等于完整复制 Issues、Secrets 和设置。

## 修改元数据

先记录当前字段，只改变请求项：

```powershell
gh repo edit $repo --description $description
gh repo edit $repo --homepage $homepage
gh repo edit $repo --add-topic $topic
gh repo edit $repo --default-branch $branch
```

主题移除、启停 Issues/Wiki/Discussions、模板属性、合并方式、自动删分支等先查 `gh repo edit --help`。默认分支变更前检查目标存在及 CI、Pages、保护规则、PR base 的影响。完成后用 `gh repo view` 或 `GET repos/{owner}/{repo}` 读取字段验证。

## 文件、目录与初始化材料

读远端文件可用连接器或 `GET repos/{owner}/{repo}/contents/{path}?ref=...`，目录响应与文件响应结构不同。大文件/二进制按官方响应和下载 URL 处理，不把截断预览当全文。编辑优先在独立分支中提交、检查完整 diff，再按授权推送或开 PR。

初始化可准备 README、LICENSE、.gitignore、CONTRIBUTING、SECURITY、CODE_OF_CONDUCT、Issue/PR 模板、CODEOWNERS。许可证由用户选择或沿用已有许可；CODEOWNERS 规则按路径与实际团队权限检查。启用讨论、模板、自动关闭 Issue 的行为不能隐含在纯文档修改中。

## 协作者与访问

| 任务 | REST 路由 |
| --- | --- |
| 列出协作者 | GET repos/{owner}/{repo}/collaborators |
| 查看某用户权限 | GET repos/{owner}/{repo}/collaborators/{username}/permission |
| 添加/调整协作者 | PUT repos/{owner}/{repo}/collaborators/{username} |
| 查看待接受邀请 | GET repos/{owner}/{repo}/invitations |
| 移除协作者 | DELETE repos/{owner}/{repo}/collaborators/{username} |

核对账号和最小所需角色；邀请已发送不等于已接受。移除访问可能影响自动化，不从“整理仓库”推导授权。组织仓库也检查团队与继承权限。

## 改名、转移、归档和删除

先展示旧/新 full name、受影响 URL、权限、Pages/Packages/Actions 和恢复限制。已获对应授权就执行，不重复要求用户确认。

- 改名：`gh repo rename $newName --repo $repo`；验证新 URL，再处理用户要求更新的 remote 和文档链接。
- 归档/取消归档：`gh repo archive` / `gh repo unarchive`；复查 archived。归档前处理开放 PR 和自动化。
- 转移：核对目标所有者资格、同名冲突与邀请，查官方 transfer API；验证新 owner，不能把“转移申请”当成完成。
- 公开性：查 fork/网络和计划约束，明确可能暴露代码及历史，核对后使用当前 CLI/API 支持的确认参数。
- 删除：仅明确删除目标后操作，先完成请求范围内备份；不能从卸载技能、清理本地文件推导删除仓库。

官方：<https://cli.github.com/manual/gh_repo>、<https://cli.github.com/manual/gh_repo_edit>、<https://docs.github.com/en/rest/repos/repos>、<https://docs.github.com/en/rest/collaborators/collaborators>。
