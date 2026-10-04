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
gh pr list --repo $repo --state open --head $headBranch --base $base --json number,url,headRefName,headRepositoryOwner,headRepository
gh pr create --repo $repo --base $base --head $headSpec --draft --title $title --body-file $bodyPath
```

查重用纯分支名 $headBranch；gh pr list --head 不支持 USER:BRANCH。结合返回的 headRepositoryOwner/headRepository 精确核对 fork 来源，并处理分页。创建用 $headSpec，fork 通常为 USER:BRANCH；组织 fork 等 CLI 限制查当前帮助/API，不能改推到上游绕过。创建返回 URL 后读取核对，不凭退出码猜 URL。

正文说明问题、改动、验证与限制。Refs #N 只关联；Closes #N 可能在合并后关闭 Issue，只对确实解决且符合任务范围的 Issue 使用。编辑用 --body-file，保留他人内容。不自动 @ 人或分配 reviewer。

## Review 修复

按评论 ID/线程核对是否过时、是否成立及代码状态，再修改与验证；不机械接受意见。提交/推送、回复评论、resolve 线程是不同动作，按已有授权执行。无法解决则说明原因，不假称已解决。

## 合并

获得合并授权后，再查最新 head SHA、base、draft、required checks、review、保护规则和队列。UNKNOWN 要刷新，无检查不等于通过。遵循项目 merge/squash/rebase 策略；使用 --match-head-commit 防止合入被替换的 head，不用 --admin 绕过。

auto-merge 或入队不是已合并。读取 state,mergedAt,mergeCommit,url 验证。除非授权包括清理，否则不顺手 --delete-branch。

官方：<https://cli.github.com/manual/gh_pr_create>、<https://cli.github.com/manual/gh_pr_merge>、<https://docs.github.com/en/rest/pulls/comments>。

## 常用状态与参与者操作

先读最新 PR，以下命令按实际任务逐条选择，不能整块执行：

```powershell
gh pr edit $pr --repo $repo --title $title --body-file $bodyPath
gh pr edit $pr --repo $repo --add-reviewer $reviewer
gh pr ready $pr --repo $repo
gh pr close $pr --repo $repo
gh pr reopen $pr --repo $repo
gh pr comment $pr --repo $repo --body-file $bodyPath
gh pr review $pr --repo $repo --comment --body-file $bodyPath
gh pr merge $pr --repo $repo --squash --match-head-commit $expectedHeadSha
```

review 的 approve/request-changes 需明确用户要求及充分审查；不自我批准、不将回复普通评论当成提交 Review。改 base 先重新评估整份 diff 和关联提交。ready、draft、auto-merge、入队和 merged 分别验证，合并方式以上仅为示例，沿用项目策略。

更新 head 分支先确认当前 head SHA 和分支所有者，查 `gh pr update-branch --help` 的 expected head/策略参数；不要在作者仍修改时强行重写。checkout PR 优先隔离 worktree，检查来源后才运行测试。关闭 PR 不删分支；revert 合并 PR 会生成新变更，不能当成关闭操作。

## 行内评论与线程

常规 PR Conversation comment 使用 Issues comments API；行内 Review comment 使用 Pull requests comments API；提交一轮 Review 使用 reviews API；resolved 是 GraphQL review thread 的状态。它们的 ID 不互换。

从最新 diff 找有效文件、line、side、commit_id，查当前 Review API 创建位置字段，不沿用旧 diff 的 position。评论过时先查新 head，避免标错行。回复行内评论使用该评论的 replies endpoint，而非新建无关联的顶层评论。

```powershell
$query = @'
query($owner:String!, $name:String!, $number:Int!, $endCursor:String) {
  repository(owner:$owner, name:$name) {
    pullRequest(number:$number) {
      reviewThreads(first:100, after:$endCursor) {
        nodes { id isResolved isOutdated path }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
'@
gh api --hostname $githubHost graphql --paginate -f query=$query -f owner=$owner -f name=$name -F number=$pr
```

需要正文时另取每个 thread 的 comments 并分页。获准解决线程后，用 `resolveReviewThread`/`unresolveReviewThread` mutation，变量 `threadId` 取真实 node ID；检查 errors 并重新读取 isResolved。推送修复并不会自动证明所有讨论已解决。
