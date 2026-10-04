# GitHub Agent Skill

面向支持 `SKILL.md` 的 AI Agent 的通用 Git/GitHub 技能。提供中文工作流程、按任务加载的参考文档，以及可选的只读检查脚本。

A reusable Git/GitHub workflow skill for AI agents that support `SKILL.md`, with Chinese-first guidance and an optional read-only diagnostic script.

## 功能

| 领域 | 内容 |
| --- | --- |
| Git | 仓库检查、分支、提交、同步、推送、fork/upstream、冲突与恢复 |
| Pull Request | 创建与更新、Review 分析与修复、合并前检查 |
| Issue | 查询、去重、创建、更新及状态管理 |
| Actions / CI | 定位运行、分析日志、最小复现、按授权重跑 |
| Release | Tag、发布草稿、正式发布与资产核对 |
| 故障处理 | dubious ownership、认证、锁文件、非快进推送、代理、LFS |
| 工作保护 | 保留已有修改和暂存内容、核对远端目标、保护凭证 |

技能提供操作指引；实际操作需要 Agent 的终端工具或 GitHub 连接器。它不会自行提供 GitHub 账号、访问凭证或 MCP 服务。

## 安装

### 下载后复制

1. 在本仓库选择 **Code → Download ZIP** 并解压。
2. 将仓库中的整个 **`github-agent` 文件夹**复制到你的 Agent 支持的技能目录。
3. 若宿主支持用户级 `.agents/skills`，Windows 下的结构应为：

```text
C:\Users\你的用户名\.agents\skills\github-agent\SKILL.md
```

macOS/Linux 对应 `~/.agents/skills/github-agent/SKILL.md`。不要把仓库外层 `github-agent-skill-main` 当成技能文件夹。

### Git 下载（PowerShell）

```powershell
git clone https://github.com/Alethean-kaw/github-agent-skill.git
```

克隆成功后，在包含 `github-agent-skill` 的目录执行：

```powershell
$source = Join-Path (Get-Location) 'github-agent-skill\github-agent'
$skillsDir = Join-Path $HOME '.agents\skills'
$destination = Join-Path $skillsDir 'github-agent'
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) {
    throw '没有找到源技能，请确认当前目录和 git clone 的结果。'
}
if (Test-Path -LiteralPath $destination) {
    throw '目标技能已存在，请先备份并检查差异，再决定如何更新。'
}
New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
Copy-Item -LiteralPath $source -Destination $destination -Recurse
```

请通过宿主的技能列表或加载日志确认识别结果。不同 Agent 的搜索目录和刷新方式可能不同；本项目不保证所有 Harness 都会自动扫描 `.agents/skills`。支持显式读取文件的 Agent 也可以直接读取 `github-agent/SKILL.md`。

## 使用示例

```text
使用 github-agent 技能，只读检查当前仓库的分支、远端、未提交修改和认证状态。
```

```text
使用 github-agent 技能分析这个 PR 的 CI 失败原因，先给出证据与修复方案。
```

```text
使用 github-agent 技能，把本次修复提交并推送到我的 fork，再向上游创建草稿 PR。
保留其他未提交和已暂存内容。
```

## 依赖

- **Git**：本地版本控制需要。
- **GitHub CLI `gh` 或 GitHub 连接器/MCP**：GitHub 平台操作需要相应工具、认证与权限。
- **Python 3.9+**：仅运行可选检查脚本时需要；无需第三方 Python 包。

官方工具下载：[Git](https://git-scm.com/downloads)、[GitHub CLI](https://cli.github.com/)。

## 可选只读检查

```powershell
python "$HOME\.agents\skills\github-agent\scripts\check_github.py" --path 'D:\Projects\my-project'
```

默认只检查本地仓库。需要认证与指定仓库访问检查时显式启用在线模式：

```powershell
python "$HOME\.agents\skills\github-agent\scripts\check_github.py" --path 'D:\Projects\my-project' --online --repo 'OWNER/REPO'
```

脚本输出 JSON，不自动修复、不 fetch、不写配置、不提交或推送。退出码：`0` 表示请求的关键检查通过；`1` 表示存在工具、路径、仓库或在线检查问题；`2` 表示参数错误。`--help` 查看全部参数。

输出会做基础脱敏，但仍可能包含私有项目名、文件名和账号信息；分享前应检查。退出码为零仅表示诊断完成，不表示允许后续写入。

## 文件组织

- [`github-agent/SKILL.md`](github-agent/SKILL.md)：入口与核心工作流程。
- [`github-agent/references/`](github-agent/references/)：按任务加载的 7 份参考文档。
- [`github-agent/scripts/check_github.py`](github-agent/scripts/check_github.py)：只读检查脚本。
- [`github-agent/agents/openai.yaml`](github-agent/agents/openai.yaml)：兼容宿主的界面元数据。

## 验证与限制

已完成技能结构、内部链接与脚本本地行为检查，包括空仓库、无仓库、无效路径、暂存/未暂存内容保留、合并状态标记、缺少 gh、参数错误及常见凭证 URL 脱敏。

当前验证环境为 Linux；尚未完成 Windows 实机和 gh 在线认证的端到端测试。技能指令不能替代宿主权限控制，也不能保证模型始终正确执行。

这是独立的通用技能项目，不是 GitHub 或 OpenAI 的官方插件。文档引用相关官方资料，具体命令以本机版本的帮助和官方文档为准。

## 贡献与许可

欢迎通过 Issue 提交可复现问题，或通过 PR 改进流程与跨平台兼容性。请勿在报告中包含 token、私钥或私有仓库内容。

采用 [MIT License](LICENSE)。
