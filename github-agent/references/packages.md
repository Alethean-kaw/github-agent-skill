# Packages、GHCR 与制品

## 识别包和归属

区分 Release 资产、Actions artifact/cache 和 Packages；分别使用对应 API。确认包类型、用户/组织 namespace、关联仓库、可见性和版本 ID。列包通过 `/users/{username}/packages`、`/orgs/{org}/packages` 或当前用户路由，按官方文档给 package_type。

包名可能包含斜杠，路径编码；容器 tag 与 digest 不同，多个 tag 可以引用同一 digest。完整枚举版本并核对时间、标签、使用方和保留规则，不能仅凭 untagged 判定无用。

## 发布和拉取

使用生态原生工具（npm、Docker/Podman、Maven、NuGet 等），读取项目已有 registry 配置和发布工作流。先构建、检查包内容与版本，避免把 .env、测试凭证和私有配置打包。登录凭证来自安全输入/宿主秘密存储，不写 shell 历史；容器用 password-stdin 等受控通道。

发布授权要包含目标 registry、namespace、版本及可见性；工作流内按需使用 GITHUB_TOKEN 和包写权限，fork PR 不获得发布秘密。发布后从 registry 读取实际版本/digest，并在隔离环境验证拉取；构建成功不是发布成功。

## 删除、恢复、权限

按 Packages REST 删除具体版本前核对引用、下载方及恢复条件。包版本恢复窗口和公开包删除限制以当前官方文档为准，不承诺一定能恢复。批量保留策略先展示候选清单；不删除最新稳定 tag 或未知 digest。

仓库权限继承、独立包权限和 workflow 对包的访问可能不同；遇到 403 先查关联仓库/Actions access，而非自动申请更大 token。恢复或调整可见性后重新读元数据验证。

官方：<https://docs.github.com/en/rest/packages/packages>、<https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>。
