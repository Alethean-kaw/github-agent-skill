# Issues、标签、里程碑与依赖

## 查询与基本流程

先确认仓库和 Issue 编号，读取正文、状态、作者、评论和相关 PR，排除重复。仅提供查询结果不自动发评论。正文通过 UTF-8 文件提交。

```powershell
gh issue list --repo $repo --state all --limit 100
gh issue view $issue --repo $repo --comments
gh issue create --repo $repo --title $title --body-file $bodyPath
gh issue edit $issue --repo $repo --add-label $label --add-assignee $username
gh issue comment $issue --repo $repo --body-file $bodyPath
gh issue close $issue --repo $repo --reason completed
gh issue reopen $issue --repo $repo
```

以上写操作分别需要对应任务授权；不能整块执行。关闭原因 completed/not planned 按实际结论；重复关闭保留重复对象链接。正文替换前读取最新内容并保留他人信息。`Closes #N` 在 PR 合并后可能关闭 Issue，跨仓库写完整引用。

## 标签与里程碑

```powershell
gh label list --repo $repo --limit 100
gh label create $label --repo $repo --color $hexColor --description $description
gh issue edit $issue --repo $repo --milestone $milestoneTitle
```

修改/删除标签先查使用情况，不用强制覆盖同名标签。颜色使用合法六位十六进制。里程碑通过 `GET/POST repos/{owner}/{repo}/milestones`、`PATCH/DELETE .../milestones/{number}` 管理；日期明确时区和 ISO 8601。Issue API 设置 milestone 使用数字编号，而 CLI 可用标题，不能混用。

## 子 Issue 与依赖

| 任务 | REST 路由 |
| --- | --- |
| 列出子项 | GET repos/{owner}/{repo}/issues/{number}/sub_issues |
| 添加子项 | POST repos/{owner}/{repo}/issues/{number}/sub_issues |
| 移除子项关系 | DELETE repos/{owner}/{repo}/issues/{number}/sub_issue |
| 查看阻塞本项的 Issue | GET repos/{owner}/{repo}/issues/{number}/dependencies/blocked_by |
| 添加阻塞来源 | POST repos/{owner}/{repo}/issues/{number}/dependencies/blocked_by |
| 移除阻塞关系 | DELETE repos/{owner}/{repo}/issues/{number}/dependencies/blocked_by/{issue_id} |

先读取双方对象；添加子项/依赖的 payload 使用 issue_id，移除子项关系的 payload 使用 sub_issue_id；这些值都是 REST 数据库 ID，不是显示编号。明确 A 被 B 阻塞的方向，检查循环、跨仓库访问和已有父项。不要默认替换父项；移除关系不会删除 Issue。排序、父项查询和 issue type 依照当前官方 schema。操作后重新读取关系验证。

## 转移、锁定、置顶与批量处理

通过当前 `gh issue transfer/lock/unlock/pin/unpin/delete --help` 获取参数。转移后核对新仓库、编号和链接；锁定不等于关闭；删除不同于关闭，必须明确授权。

批量操作先生成对象清单和匹配依据，核对范围与数量，再逐项记录结果。部分成功时仅处理失败项；不能因为列表截断而声称全部完成。标签与 assignee 的增删优先使用增量接口，避免覆盖其他人设置。

官方：<https://cli.github.com/manual/gh_issue_edit>、<https://docs.github.com/en/rest/issues/sub-issues>、<https://docs.github.com/en/rest/issues/issue-dependencies>、<https://docs.github.com/en/rest/issues/milestones>。
