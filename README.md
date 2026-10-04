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

### 一条命令安装（推荐）

需要已安装 [Node.js](https://nodejs.org/)（包含 npm/npx）和 [Git](https://git-scm.com/downloads)，并能访问 npm 与 GitHub。当前验证的 Skills CLI 1.7.0 要求 Node.js 22.20.0 或更高版本。下面命令适用于 PowerShell、CMD、macOS 和 Linux 终端。

**安装到当前项目的 `.agents/skills`**

先在目标项目根目录打开终端，然后执行：

```sh
npx --yes skills@latest add Alethean-kaw/github-agent-skill --skill github-agent --agent universal --yes
```

**安装到当前用户全局的 `.agents/skills`**

在任意目录执行：

```sh
npx --yes skills@latest add Alethean-kaw/github-agent-skill --skill github-agent --agent universal --global --yes
```

| 安装范围 | 技能入口 |
| --- | --- |
| 当前项目 | `<项目根目录>/.agents/skills/github-agent/SKILL.md` |
| 全局（Windows） | `C:\Users\你的用户名\.agents\skills\github-agent\SKILL.md` |
| 全局（macOS / Linux） | `~/.agents/skills/github-agent/SKILL.md` |

- `--skill github-agent`：只安装本仓库的这个技能。
- `--agent universal`：明确选择共享的 `.agents/skills` 安装位置，不依赖自动检测宿主。
- `--global`：改为当前用户主目录下的全局安装；省略时安装到终端当前目录。
- 两处 `--yes` 分别跳过 npx 下载确认和技能安装确认。

安装器来自 [vercel-labs/skills](https://github.com/vercel-labs/skills)，会从本仓库读取技能，无需把本项目另外发布为 npm 包。这里的“全局”是当前用户级，不是系统所有用户；宿主仍需支持扫描该目录。

**更新：**重新执行对应范围的安装命令即可从仓库获取最新版本。安装器会替换同名技能目录；如果你修改过技能文件，请先备份。

### 确认安装与加载

在 PowerShell 中检查项目级安装：

```powershell
Test-Path .\.agents\skills\github-agent\SKILL.md
```

检查全局安装：

```powershell
Test-Path "$HOME\.agents\skills\github-agent\SKILL.md"
```

返回 `True` 表示入口文件存在。随后让 AI 工具重新加载技能，或重启并新建会话，通过宿主的技能列表或加载日志确认识别结果。不同 Agent 的搜索目录和刷新方式可能不同；本项目不保证所有 Harness 都会自动扫描 `.agents/skills`。支持显式读取文件的 Agent 也可以直接读取已安装的 `SKILL.md`。

### 手动下载（备用）

1. [下载 main 分支 ZIP](https://github.com/Alethean-kaw/github-agent-skill/archive/refs/heads/main.zip) 并解压；也可以在[仓库首页](https://github.com/Alethean-kaw/github-agent-skill)点击 **Code → Download ZIP**。
2. 打开解压后的 `github-agent-skill-main`，取出其中的 **`github-agent` 子文件夹**。
3. 将这个子文件夹放入项目的 `.agents/skills/` 或用户主目录的 `.agents/skills/`，最终入口路径应与上表一致。目标已存在时先备份再替换。

ZIP 是整个仓库的源码压缩包，不能把外层 `github-agent-skill-main` 文件夹直接当成技能安装。

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

已使用 Skills CLI 1.7.0 从本公开仓库验证项目级和全局安装（全局测试使用隔离的用户主目录），两种安装位置均为对应的 `.agents/skills/github-agent`，10 个技能文件与源文件完整一致。

当前验证环境为 Linux；尚未完成 Windows 实机和 gh 在线认证的端到端测试。技能指令不能替代宿主权限控制，也不能保证模型始终正确执行。

这是独立的通用技能项目，不是 GitHub 或 OpenAI 的官方插件。文档引用相关官方资料，具体命令以本机版本的帮助和官方文档为准。

## 贡献与许可

欢迎通过 Issue 提交可复现问题，或通过 PR 改进流程与跨平台兼容性。请勿在报告中包含 token、私钥或私有仓库内容。

采用 [MIT License](LICENSE)。
