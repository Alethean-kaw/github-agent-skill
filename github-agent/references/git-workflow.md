# Git 工作流

## 读取与保护

```powershell
git rev-parse --show-toplevel
git status --short --branch
git status --long
git branch --show-current
git branch -vv
git remote -v
git diff --stat
git diff --cached --stat
git log -5 --oneline
```

检查退出码；新空仓库没有 HEAD 是正常情况。用长状态和 git rev-parse --git-path 定位 MERGE_HEAD、rebase-merge、rebase-apply、CHERRY_PICK_HEAD、REVERT_HEAD、sequencer 等状态。短 status 没有 U 不代表没有进行中的操作；冲突已解决但未完成提交的 merge 仍会保留 MERGE_HEAD。不能接管用户已有 merge/rebase/cherry-pick。分支名为空时检查 detached HEAD。读取贡献规则和换行配置，不为警告全局修改 core.autocrlf。

修改前区分用户改动和任务改动，读取相关 diff 与未跟踪文件。需要新分支则从确认基线 `git switch -c $newBranch`；不要自动 stash、丢弃或将无关改动带进新分支。

## 提交

用户授权提交后，只暂存任务文件/补丁，不默认 add . 或 add -A。已有无关暂存内容时先使用隔离 worktree 或让用户处理，不清空暂存区、不一并提交。

```powershell
git add -- 'src/实际文件.ts'
git diff --cached --check
git diff --cached --stat
git diff --cached
git commit -m 'fix: describe the actual change'
git log -1 --format='%H %s'
git status --short --branch
```

每步成功再继续；提交前检查秘密和产物。遵循仓库提交风格。作者身份缺失用用户提供的姓名/邮箱，通常仓库级配置，不编造。hooks 失败排查原因，不自动 --no-verify。gitignore 不取消已有跟踪，也不清理历史秘密。

## 同步与推送

以下变量先赋已确认值。需要新鲜远端信息时 fetch，再分析关系：

```powershell
git fetch $remote
git rev-list --left-right --count 'HEAD...@{upstream}'
```

没有 upstream 就明确选择引用，不猜。更新默认考虑 `git pull --ff-only $remote $remoteBranch`；分叉时读取两侧提交，按规范 merge/rebase。不要裸 pull 后任由默认配置决定历史变化。

推送前核对 URL、当前分支、远端分支、所有待推提交和秘密。仅推任务分支，不用 --all/--mirror/顺手推所有 tags。

```powershell
git push -u $remote $branch
git rev-parse HEAD
git ls-remote --heads $remote "refs/heads/$branch"
```

以上仅适用于当前分支等于 $branch。比对本地 HEAD 和远端 SHA。非快进、保护规则、没权限、网络故障分开处理；推送失败不等于允许强制推送。

## Fork 与 upstream

核对 remote URL 和 `gh repo view $repo --json nameWithOwner,isFork,parent,defaultBranchRef`。origin=个人 fork、upstream=源仓库只是惯例。新增 remote 前检查同名，不擅自改已有地址。

同步先 fetch upstream，再按目标分支策略合并。不要用强制 sync 清掉 fork 的独有提交。PR 的 base 在接收方仓库，head 在贡献方分支。

## 冲突与恢复

用 status 和 `git diff --name-only --diff-filter=U` 定位，理解两侧意图后逐文件解决，不整仓 ours/theirs；rebase 时两侧语义与 merge 不同。定点 add、相关验证后用对应的 merge/rebase/cherry-pick --continue。

只在确认影响后 abort 本任务启动的操作，不中止用户已有操作。共享分支通常新增 revert 提交；合并提交的 -m 主线不能猜。找回提交先 reflog，再从 SHA 建恢复分支，不用 hard reset 覆盖。reflog 不能恢复从未被 Git 记录的普通未保存文件。

官方：<https://git-scm.com/docs/git-status>、<https://git-scm.com/docs/git-push>、<https://git-scm.com/docs/git-rebase>、<https://git-scm.com/docs/git-reflog>。
