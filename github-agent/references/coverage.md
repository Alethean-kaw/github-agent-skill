# 功能覆盖与验证边界

这是领域覆盖清单，不是 GitHub 全部端点清单。示例基于官方 CLI/API 文档核对；实际执行前仍查本机版本、主机、计划、工具权限。文档基线：2026-10-04。

## 覆盖层级

- **流程+示例**：有检查、执行入口/命令示例、验证与异常说明；不表示已对真实账号执行全部写操作。
- **流程+接口路径**：有操作顺序、API 路由或官方 schema 查找路径，运行时需按当前对象构造 payload。
- **导航/边界**：列出能力入口、前提与限制，通常依赖官方界面、计划或专门工具。

| 领域 | 层级 | 主要内容与边界 |
| --- | --- | --- |
| [环境与认证](setup.md) | 流程+示例 | 工具检测、认证、多账户、跨平台；不收集聊天中的 token |
| [Git 基本流程](git-workflow.md) | 流程+示例 | 分支、提交、fetch/pull/push、fork、冲突与恢复 |
| [Git 进阶](git-advanced.md) | 流程+示例 | worktree、stash、cherry-pick/revert/rebase、bisect、LFS、子模块、签名 |
| [仓库管理](repositories.md) | 流程+示例 | 初始化、配置、协作者、归档/删除、转移；高级设置按 schema |
| [PR 与 Review](pull-requests.md) | 流程+示例 | 创建/编辑/ready/关闭/重开、审查、行内评论、线程、合并 |
| [Issues](issues.md) | 流程+示例 | 生命周期、标签、里程碑、子项、依赖、批量；关系写入查 schema |
| [搜索](search.md) | 流程+示例 | 代码/仓库/提交/Issue/PR、分页、索引和活动范围 |
| [Projects](projects.md) | 流程+示例 | 项目/条目/字段；视图、自动化与权限按当前 GraphQL/界面 |
| [Actions](github-actions.md) | 流程+示例 | 诊断、dispatch、watch、取消、启停、下载、缓存；runner 按 API |
| [Release](releases.md) | 流程+示例 | Tag、草稿/正式/预发布、notes、资产、校验、immutable 限制 |
| [规则与权限](rules-permissions.md) | 流程+接口路径 | Rulesets、保护、权限、bypass、读回验证 |
| [秘密与环境](secrets-environments.md) | 流程+示例 | 不同范围 secret/variable、环境、轮换、审批；不读取 secret 明文 |
| [网站与部署](pages-deployments.md) | 流程+接口路径 | Pages、构建、域名/HTTPS、部署记录、上线/回滚 |
| [包与制品](packages.md) | 流程+接口路径 | 各生态原生发布、GHCR、版本/digest、权限、删除恢复 |
| [安全](security.md) | 流程+接口路径 | 依赖/代码/秘密扫描、公告、修复、状态、签名和证明 |
| [组织与企业](organizations-enterprise.md) | 流程+接口路径；部分导航/边界 | 团队/成员/审计；SSO/SCIM/计费/账号依权限及官方界面 |
| [集成](webhooks-apps.md) | 流程+接口路径 | Hook、投递、App 安装/权限、OAuth、工具集成 |
| [社区与互动](community.md) | 流程+示例；部分导航/边界 | Gists、Discussions、Wiki、通知、Star/Watch、社区资料 |
| [远程开发](codespaces.md) | 流程+示例；部分导航/边界 | 实例、端口、生命周期、devcontainer；远程 Agent 按现有能力 |
| [备份迁移](backup-migration.md) | 流程+接口路径 | Git/平台数据分类备份、恢复、迁移、批量与差异核对 |
| [API 与能力发现](api.md) | 流程+示例 | REST/GraphQL、ID、分页、重试、限流、文件与多文件提交 |
| [故障处理](troubleshooting.md) | 流程+示例 | 所有权、锁、认证、推送、网络、LFS、秘密泄露 |

## 低频功能与边界

组织自定义角色、企业策略、SCIM、许可和计费、Sponsors 支付、Marketplace、教育/账号申请、账号恢复或删除、GHES 运维、Copilot 管理等，不预置固定写入模板。读取组织/社区/远程开发/API 模块，核对当前官方能力；没有接口时使用获准的官方界面或明确交由用户完成。不能将列出名称视为这些功能已端到端实现。

## 验证分层

1. 结构检查验证 frontmatter、路由、内部链接和 Python 语法。
2. 自动测试验证本地诊断脚本的只读行为、状态识别、错误和脱敏，不连接真实 GitHub 账号。
3. 安装检查验证所选范围的 `.agents/skills/github-agent` 内容，不代表宿主一定自动加载。
4. 文档场景检查评估任务选路、操作次序与边界，不替代在线命令执行。
5. Windows/Linux CI 只有实际运行成功才能报告通过；配置存在不算通过。

远端写入、计费、部署、组织管理等需在用户真实任务授权中验证。不得为证明技能覆盖而自动创建资源、修改权限、发送评论或删除对象。
