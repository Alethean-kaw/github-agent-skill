# 搜索、读取与活动查询

## 明确查询范围

区分当前工作树搜索（rg）、提交历史（git log）、远端代码索引（gh search code）、Issue/PR 元数据和仓库搜索。先确定 owner/repo、分支、状态、时间区间与上限；用户输入作为独立参数，不 eval。

```powershell
gh search repos $query --owner $owner --limit 50
gh search code $query --repo $repo --limit 50
gh search issues $query --repo $repo --state open --limit 100
gh search prs $query --repo $repo --state open --limit 100
gh search commits $query --repo $repo --limit 50
```

先查对应 `--help` 的过滤器和 JSON 字段；网页代码搜索、CLI 与 REST 搜索语法及索引范围可能不同，不能将网页正则原样塞进 API。代码无命中不代表所有分支都不存在；必要时获取明确 ref 在本地 rg。

## 完整性与证据

结果报告查询条件、取回数、是否分页或截断、所用分支/commit。搜索接口有结果上限；需要完整清单时改对象列表接口或按时间分片并去重，不能无限增大 limit。引用源码时记录稳定 commit 和文件位置，进一步读上下文，不仅依赖搜索摘要。

活动事件、贡献图、搜索命中和 audit log 的范围不同；活动记录不是完整审计。仓库 traffic、clones、referrers 需要权限并有保留期，读取官方 traffic API 后注明时间窗口。不要由少量事件推断全部人员活动。

## 用户和通知

查用户/组织用官方 users/orgs API，准确区分登录名、显示名与邮箱。`GET notifications` 读取通知；标已读、取消订阅、订阅仓库是状态修改。通知 subject 的 API URL 与网页 URL 不同，不能拼造跳转链接。

官方：<https://cli.github.com/manual/gh_search_code>、<https://cli.github.com/manual/gh_search>、<https://docs.github.com/en/rest/search/search>、<https://docs.github.com/en/rest/metrics/traffic>、<https://docs.github.com/en/rest/activity/notifications>。
