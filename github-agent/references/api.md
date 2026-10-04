# API、工具选择与版本适配

## 选择执行入口

先检查 `git --version`、`gh --version`、相关 `gh <命令> --help` 及现有连接器 schema。优先用已连接且满足任务的工具；本地代码用 Git，平台对象用 gh/MCP；专用命令不足才用 REST/GraphQL。工具缺失不等于 GitHub 不支持功能；没有接口或权限就记录限制，不能虚构端点。网页操作只在宿主允许且任务需要时使用。

本目录 PowerShell 示例中的 `$repo` 为 OWNER/REPO，`$githubHost` 为确认的主机；`$owner`、`$name` 等变量均需从实际对象获取。平台 CLI 的 `--repo` 在 Enterprise 应使用 HOST/OWNER/REPO；REST 路径仍只放 OWNER/REPO，主机传给 `--hostname`。未展示变量赋值的片段是模板，不能原样批量执行。表格中的方法和路径是 API 路由，不是 shell 命令。

## REST 读写模板

```powershell
$repo = 'OWNER/REPO'
$githubHost = 'github.com'
gh api --hostname $githubHost --method GET "repos/$repo"
gh api --hostname $githubHost --method GET --paginate "repos/$repo/issues?state=all&per_page=100"
# payloadPath 是已审阅的 UTF-8 JSON 文件，仅包含本次需修改的字段。
gh api --hostname $githubHost --method PATCH "repos/$repo" --input $payloadPath
```

加 `-f/-F` 可能改变默认方法；只读查询显式 GET。`-F` 进行类型转换，`-f` 为字符串；复杂数组、null、布尔值及正文统一用 JSON 文件。路径片段分别 URL 编码（特别是带斜杠的分支、环境名、包名），不能编码整条路由。需要 API 版本头时使用目标主机当前支持的版本，不盲用 Cloud 新版于旧 GHES。

写前读取并保留受影响的非敏感字段；有 ETag/SHA 前置条件时使用。Contents API 更新带当前文件 blob SHA，内容使用 Base64；多个文件优先 Git 提交或 Git Trees/Commits/Refs，使用现有 base tree 保留其他文件，只做非强制引用更新。空仓库先按当前官方文档建立首个提交，不能伪造 parent。

## GraphQL

```powershell
$query = @'
query($owner:String!, $name:String!, $endCursor:String) {
  repository(owner:$owner, name:$name) {
    issues(first:100, after:$endCursor) {
      nodes { number title url }
      pageInfo { hasNextPage endCursor }
    }
  }
}
'@
gh api --hostname $githubHost graphql --paginate -f query=$query -f owner=$owner -f name=$name
```

先查询实际 node ID，再构造 mutation；编号、REST 数字 ID、GraphQL node ID 不能混用。嵌套 connection 要分别分页，外层分页不会自动取完评论。HTTP 200 仍可能含 `errors` 或部分 `data`，必须检查。写操作先审阅变量文件，按 schema 的必需字段和 ID 类型执行，返回后再 query 验证对象。

## 分页、限流与重试

读取 Link/pageInfo；`--limit 100` 不等于“所有”。搜索存在索引延迟和结果上限，需要完整枚举时改列表接口或按时间/仓库分片。检查 rate limit、Retry-After、认证主机及权限，不通过盲目并发绕过限制。仅对可重试读请求按提示退避；创建 Issue、Release、部署等超时后先查现状再决定是否重试。

区分 401 认证、403 权限/SSO/限流/策略、404 不存在或不可见、409 冲突、422 参数/验证失败。出错先读必要响应，隐藏敏感字段，禁止 `GH_DEBUG=api` 日志外泄。不要自动扩大 token scope。

## 遇到未收录功能

1. 明确对象、主机、计划、角色和用户要完成的状态变化。
2. 查对应 CLI help、官方 REST 分类或 GraphQL schema；核对端点、token 类型和所需权限。
3. 先做最小只读探测；准备精确 payload 和成功判据，再在已有授权内执行。
4. 没有 API 的账号/付款操作走官方界面或用户接管；不可绕过认证和权限边界。
5. 记录实际能力及缺口，不声称调用 `gh api` 就覆盖了整个 GitHub。

官方：<https://cli.github.com/manual/gh_api>、<https://docs.github.com/en/rest>、<https://docs.github.com/en/graphql>。
