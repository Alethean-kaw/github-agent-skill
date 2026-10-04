# Git 进阶与历史维护

## 初始化、检查与取证

用户要求创建本地仓库且目录确认后，先查是否处于其他仓库内部，再 `git init -b $branch`；不要无意制造嵌套仓库。用 `git log --graph --oneline --decorate`、`git show $sha`、`git blame -- $file`、`git log -S $text -- $file` 追踪变更。单次提交包含多个作者改动时不要凭提交者猜责任。

## Worktree

```powershell
git worktree list --porcelain
git worktree add -b $taskBranch $newPath $baseRef
git -C $newPath status --short --branch
```

先 fetch 所需基线并记录 SHA；新 worktree 不会包含原目录未提交修改。同一分支不能随意同时检出到两个 worktree。结束前检查目标 worktree 的未提交/未跟踪文件，再 `git worktree remove $newPath`；不使用 --force 清理未知内容。

## Cherry-pick、revert 与 rebase

先核对目标分支、原提交范围、父提交和相关依赖，防止只挑一半修复。干净隔离目录中执行 `git cherry-pick $sha`；发布过的撤销优先 `git revert $sha`。合并提交需先解释 `-m` 主线选择。冲突时定位文件、测试、continue；abort 仅用于本任务启动的操作。

交互 rebase/squash/amend 会改变 SHA。共享历史要有明确授权和恢复引用，核对别人新提交，再精确 `--force-with-lease=<ref>:<expected-sha>`。不把修复提交说明默认变为重写远端历史。变基后重新检查全部差异和测试，签名可能需要重建。

## Stash 与选择性暂存

先读取 `git stash list`、`git diff`、`git diff --cached`。用户允许暂存工作区时，为本任务创建可识别消息并记录 stash 对象 ID；`stash push -u` 包括未跟踪但不含忽略文件，`-a` 可能收进秘密和大量产物。恢复先 apply 而非 pop，核对暂存状态与工作区，再决定是否 drop；不要清空用户 stash。

用路径或审阅后的补丁进行部分暂存；不要修改、取消或顺带提交用户已有无关暂存内容。无可靠隔离方式时说明具体冲突。

## Bisect

在隔离 worktree 中确认可重复的成功/失败版本与检测命令，再 `git bisect start $bad $good`。检测脚本退出 0=good，1–127（125 除外）=bad，125=skip；测试环境无法运行不等于代码 bad。`bisect run` 会执行历史代码，先检查依赖与脚本，结束执行 `git bisect reset` 并报告首个坏提交与证据。

## 大仓库、LFS 与子模块

- 浅克隆缺历史：先检查 `git rev-parse --is-shallow-repository`，按需 deepen/unshallow；部分克隆可选 `--filter=blob:none`，服务器能力先核对。
- 稀疏检出：先读取 `git sparse-checkout list`，用 set/add 配置所需目录；改变规则可能移除工作树路径，先保留本地改动。
- LFS：读 `.gitattributes`，核对 `git lfs version`、`git lfs ls-files`；按需 fetch/pull。新增 track 后提交属性文件。历史迁移会重写历史，单独处理。不要把 LFS 指针误当原始文件。
- 子模块：读 `.gitmodules`、`git submodule status`，核对来源再 init/update；递归操作会访问外部仓库。提交子模块变更需先推子仓库 commit，再提交父仓库 gitlink。

## 签名、清理与恢复

按项目要求设置仓库级 GPG/SSH 签名，验证 `git verify-commit` / `git verify-tag`；网页 Verified 与本机信任策略不同。`git clean -nd` 仅预览；执行删除、hard reset、清理历史需精确授权和恢复点。先 reflog、branch 恢复，再考虑 fsck；bundle 不包含工作树、LFS 实体和平台数据。不要自动 aggressive gc 或过期 reflog。

官方：<https://git-scm.com/docs/git-worktree>、<https://git-scm.com/docs/git-bisect>、<https://git-scm.com/docs/git-stash>、<https://git-scm.com/docs/git-sparse-checkout>、<https://git-scm.com/docs/git-submodule>、<https://git-lfs.com/>。
