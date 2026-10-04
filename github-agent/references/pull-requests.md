# PR 与 Review

$repo 使用明确 OWNER/REPO 或 HOST/OWNER/REPO；$pr 为编号。每次写前再次确认目标。

## 读取

```powershell
gh pr list --repo $repo --state open --limit 30
gh pr view $pr --repo $repo --json number,url,title,body,baseRefName,headRefName,headRefOid,isCrossRepository,state,isDraft,mergeable,reviewDecision,statusCheckRollup
gh pr diff $pr --repo $repo
gh pr checks $pr --repo $repo
gh pr view $pr --repo $repo --comments
```

审查阅读源码上下文与当前 head，区分证实缺陷、风险和建议，指出位置、触发条件、影响。只读审查不切换脏工作区、不发评论或批准。

--comments 不能当作全部行内审查。补充读取：

```powershell
$apiRepo = 'OWNER/REPO'
$githubHost = 'github.com'
gh api --hostname $githubHost --method GET --paginate "repos/$apiRepo/pulls/$pr/comments"
gh api --hostname $githubHost --method GET --paginate "repos/$apiRepo/pulls/$pr/reviews"
```

Enterprise 主机和 REST 的 OWNER/REPO 分开；不要把 HOST 放进 REST 路径。线程 resolved 状态需要 GraphQL reviewThreads 与分页 pageInfo；不能凭评论位置为空推断已解决。

## 创建或编辑

核对 head/base、全部提交和差异、模板、验证结果，先查是否已有相同 PR。默认草稿，用户明确正式 PR 则遵从。创建 PR 授权通常包含必要的分支推送，提前明确推送到哪个仓库，避免交互提示意外创建 fork。

```powershell
gh pr list --repo $repo --state open --head $head --base $base
gh pr create --repo $repo --base $base --head $head --draft --title $title --body-file $bodyPath
```

fork 的 head 通常为 USER:BRANCH；组织 fork 等 CLI 限制查当前帮助/API，不能改推到上游绕过。创建返回 URL 后读取核对，不凭退出码猜 URL。

正文说明问题、改动、验证与限制。Refs #N 只关联；Closes #N 可能在合并后关闭 Issue，只对确实解决且符合任务范围的 Issue 使用。编辑用 --body-file，保留他人内容。不自动 @ 人或分配 reviewer。

## Review 修复

按评论 ID/线程核对是否过时、是否成立及代码状态，再修改与验证；不机械接受意见。提交/推送、回复评论、resolve 线程是不同动作，按已有授权执行。无法解决则说明原因，不假称已解决。

## 合并

获得合并授权后，再查最新 head SHA、base、draft、required checks、review、保护规则和队列。UNKNOWN 要刷新，无检查不等于通过。遵循项目 merge/squash/rebase 策略；使用 --match-head-commit 防止合入被替换的 head，不用 --admin 绕过。

auto-merge 或入队不是已合并。读取 state,mergedAt,mergeCommit,url 验证。除非授权包括清理，否则不顺手 --delete-branch。

官方：<https://cli.github.com/manual/gh_pr_create>、<https://cli.github.com/manual/gh_pr_merge>、<https://docs.github.com/en/rest/pulls/comments>。
