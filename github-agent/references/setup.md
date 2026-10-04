# 环境与 Windows

本地版本控制需要 Git；平台操作需要 gh 或现有连接器。Python 3.9+ 仅为可选脚本所需，不是阅读技能的依赖。宿主必须实际支持 SKILL.md；是否扫描 .agents/skills 以其技能列表或日志为准，不能保证所有 Harness 都支持。

在 PowerShell 逐行检查：

```powershell
git --version
gh --version
gh auth status --hostname github.com
```

本地 Git 任务不要求 gh。认证使用普通 auth status 的状态与退出码，不用 --show-token/gh auth token；不要仅依赖 auth status --json 的退出码。gh 认证与 Git 的 HTTPS/SSH 推送认证可能不同。

缺工具时提供官方来源 <https://git-scm.com/downloads>、<https://cli.github.com/>；不要自动运行下载脚本。用户要求安装且有 winget 时先核对 Git.Git / GitHub.cli 的包信息再安装，之后验证。

未登录让用户在自己的终端执行 `gh auth login --hostname github.com --web`；不要索要聊天中的 token。Enterprise 用已确认的主机。多账户先检查再按授权切换；公开仓库可读不代表可写。

## 可选检查脚本

```powershell
python "$HOME\.agents\skills\github-agent\scripts\check_github.py" --path 'D:\AI\你的项目'
python "$HOME\.agents\skills\github-agent\scripts\check_github.py" --path 'D:\AI\你的项目' --online --repo 'OWNER/REPO'
```

脚本输出 JSON；默认不联网、不 fetch、不写 config、不修复。--online 检查认证；指定 --repo 才检查仓库访问；--host 默认为 github.com。退出 0 表示已请求的关键检查通过，1 表示工具/仓库/认证/网络/超时等异常，2 表示参数无效。逐项看错误，不能一律解释成认证失败。

输出有基础脱敏但可能仍包含账号、文件名和私有项目名，分享前检查。没有 Python 可手动：

```powershell
Set-Location -LiteralPath 'D:\AI\你的项目'
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git diff --stat
git diff --cached --stat
git remote -v
```

复述 remote 输出前隐藏 URL 凭证。diff 不包含未跟踪文件内容，结合 status 读取相关文件。

## 正文、路径、退出码

Windows PowerShell 5.1 的 > 可能输出 UTF-16；用显式 UTF-8：

```powershell
$bodyPath = Join-Path ([IO.Path]::GetTempPath()) ('gh-body-' + [guid]::NewGuid().ToString('N') + '.md')
$body = @'
说明实际问题、改动和验证。

保留真正的换行。
'@
[IO.File]::WriteAllText($bodyPath, $body, [Text.UTF8Encoding]::new($false))
```

将 $bodyPath 传给已授权的命令 --body-file；完成后清理该临时文件。不要依赖字符串中的反斜杠 n 变成换行。

每次关键原生命令之后立即检查 $LASTEXITCODE，失败停止后续步骤。Windows PowerShell 5.1 的 ErrorActionPreference=Stop 不能可靠代替这一步。路径使用引号与 -LiteralPath，不复用 $HOME/$Host/$PROFILE 为任务变量。Git 的 '@{upstream}' 需要引用。

官方：<https://cli.github.com/manual/gh_auth_status>、<https://cli.github.com/manual/gh_auth_login>。
