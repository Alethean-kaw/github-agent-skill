# 平台操作导航

先核对目标主机、账号、OWNER/REPO、默认分支与真实权限。不要把公开仓库可读当成有写权限。

按具体任务读取：

- 仓库创建、fork、元数据、协作者、文件与生命周期： [仓库管理](repositories.md)。
- Issue、标签、里程碑、子项与依赖： [Issues](issues.md)。
- REST、GraphQL、分页、限流、错误与工具降级： [API](api.md)。
- 其余领域从 SKILL.md 的路由表选择，不一次加载全部文件。

连接器只有只读能力时，检查现有 gh/API 是否可完成用户已授权的操作；没有可用写工具则准备具体修改内容，说明受限步骤。不要编造工具、请求聊天中的 token 或自动安装第三方扩展。

官方：<https://cli.github.com/manual>、<https://docs.github.com/en/rest>、<https://docs.github.com/en/graphql>。
