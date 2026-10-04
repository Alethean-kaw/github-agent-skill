# GitHub Agent Skill

面向支持 `SKILL.md` 的 AI Agent 的通用 Git/GitHub 技能。提供中文工作流程、按任务加载的参考文档，以及可选的只读检查脚本。

A reusable Git/GitHub workflow skill for AI agents that support `SKILL.md`, with Chinese-first guidance and an optional read-only diagnostic script.

## 功能

当前提供 **24 份按需加载的参考文档**。AI 每次只需读取对应模块；入口保持简短，不把全部手册塞入每次对话。

| 领域 | 内容 |
| --- | --- |
| Git | 基本流程、worktree、stash、cherry-pick/revert/rebase、bisect、LFS、子模块、恢复与签名 |
| 仓库 | 创建、克隆、fork、元数据、文件、协作者、改名、转移、归档与删除 |
| PR / Review | 创建、编辑、状态、审查、行内评论、线程、更新分支、合并与队列 |
| Issues / 搜索 | 标签、里程碑、子项、依赖、批量处理、代码/提交/Issue/PR 搜索 |
| Projects | 项目、条目、字段、状态，以及视图和自动化的接口路径 |
| Actions / Release | CI 诊断、工作流、运行、缓存、产物、Runners、Tag、发布与资产 |
| 配置与部署 | Rulesets、保护规则、Secrets、Variables、Environments、Pages、域名与部署 |
| Packages / 安全 | GHCR、包版本、权限、Dependabot、代码/秘密扫描、安全公告、制品证明 |
| 组织与集成 | 组织、团队、成员、Enterprise、SSO/SCIM、Webhooks、Apps、OAuth、MCP |
| 社区与远程开发 | Discussions、Gists、Wiki、通知、Star/Watch、Codespaces、devcontainer、Agent 任务 |
| 迁移与 API | 分类备份、恢复、迁移、REST/GraphQL、分页、限流、重试、版本适配与工具降级 |

查看[功能覆盖与验证边界](github-agent/references/coverage.md)，区分有具体示例的流程、需要运行时查询 schema 的功能，以及仅提供官方入口的账号/计费等操作。

技能提供操作指引；实际执行依赖 Agent 的终端或 GitHub 连接器、账号权限及平台能力。没有真实工具时不会因为安装技能而获得 GitHub 操作权限。

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
- [`github-agent/references/`](github-agent/references/)：按任务加载的 24 份参考文档。
- [`github-agent/scripts/check_github.py`](github-agent/scripts/check_github.py)：只读检查脚本。
- [`github-agent/agents/openai.yaml`](github-agent/agents/openai.yaml)：兼容宿主的界面元数据。
- [`tools/validate_skill.py`](tools/validate_skill.py)：维护者使用的结构与链接检查。
- [`tests/test_check_github.py`](tests/test_check_github.py)：只读诊断的离线回归测试。
- [`.github/workflows/validate.yml`](.github/workflows/validate.yml)：Windows/Linux 自动检查配置。

## 验证与限制

- **本地已验证：**结构、入口路由、内部文件链接和 Python 语法；14 项离线回归测试通过，覆盖空仓库、暂存/未暂存内容保留、真实合并冲突、已解决但未提交的合并、sequencer、detached HEAD、无效路径/参数、缺工具、超时及凭证脱敏。
- **场景检查：**Projects 已有条目的状态更新，以及有旧 run、fork 代码和用户暂存修改的 CI 排查；检查操作次序和判断，不代表真实在线执行。
- **安装：**使用 Skills CLI 1.7.0 核对项目级与隔离用户主目录的全局安装。更新后应核对完整技能目录，不只替换 SKILL.md。
- **持续检查：**配置 Ubuntu/Windows × Python 3.9/3.13 矩阵。实际运行状态以 [Actions](https://github.com/Alethean-kaw/github-agent-skill/actions/workflows/validate.yml) 为准，配置存在不表示已经通过。
- **未验证范围：**没有为了测试而对真实账户执行组织权限、计费、部署、删除或所有 CLI/API 写操作；Windows 的 gh 在线认证和所有宿主加载行为未做端到端验证。

维护者在仓库根目录运行（无需第三方 Python 依赖）：

```sh
python tools/validate_skill.py
python -m unittest discover -s tests -v
```

官方文档核对基线为 2026-10-04；命令和接口运行时仍需检查当前 help、schema、主机版本及权限。本项目是独立通用技能，不是 GitHub 或 OpenAI 官方插件。

## 贡献与许可

欢迎通过 Issue 提交可复现问题，或通过 PR 改进流程与跨平台兼容性。请勿在报告中包含 token、私钥或私有仓库内容。

采用 [MIT License](LICENSE)。
