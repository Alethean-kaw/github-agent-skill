# 故障处理

## dubious ownership

表示运行 Git 的账户与仓库所有者不同，不代表损坏。确认是用户信任并要求修复的确切路径后，仅对该目录设例外，例如：

```powershell
git config --global --add safe.directory 'D:/Projects/my-project'
git -C 'D:/Projects/my-project' status --short --branch
```

示例路径必须换成实际报错路径。这修改当前账户 Git 信任配置，不改变 NTFS 所有者。不添加 '*' 或父目录通配符。路径来源不明先澄清，不能自动信任所有内容。

## origin 已存在

先 remote -v；正确就不重复 add。需要更改且获授权时 remote set-url，再核对，不先 remove。URL 不放 token。

## non-fast-forward

fetch 后读取两侧差异，保留需要的提交，按规范 merge/rebase。失败不等于 force 授权；重写需明确范围、恢复点和精确远端 SHA 的 force-with-lease。

## 认证 403/404

分别检查主机、OWNER/REPO、gh 账号、Git HTTPS/SSH 凭证、SSO、权限与速率限制。私库 404 可能没权限。不自动扩大 scope、切账户、删凭证管理器记录。错误摘录要脱敏。

## index.lock

先确认没有 Git/IDE/Agent 正在写仓库。用 `git rev-parse --git-path index.lock` 找实际路径，worktree 的 .git 可能是文件。仅凭年龄不能认定失效。只有确认遗留且允许修复时删除确切锁，不删 .git 或整目录。

## 网络、代理、TLS

区分 DNS、连接、TLS、代理与权限；仅检查必要配置并脱敏，不输出完整环境或 config --list。不清全局代理，不设置 http.sslVerify=false。网络失败不等于仓库不存在。

## 大文件/LFS/子模块

区分 Git 对象、LFS 指针、submodule 引用；clone 成功不保证资产下载。先读 .gitattributes/.gitmodules 和错误，不自动迁移历史、递归下载所有外部项目或删除子模块。

## 秘密泄露

停止扩散且不打印秘密，说明需撤销/轮换。删除当前文件不能恢复已泄露凭证的安全。历史清理需要具体授权与协作者协调，不顺手 force。扫描无命中不能保证绝无秘密。

官方：<https://git-scm.com/docs/git-config#Documentation/git-config.txt-safedirectory>、<https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository>。
