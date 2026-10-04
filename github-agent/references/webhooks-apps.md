# Webhooks、GitHub Apps 与集成

## Webhook 生命周期

先查现有 hook，确认 URL 的所有权、HTTPS、订阅事件和目标作用域，避免把私库事件发到未知接收端。

| 任务 | 仓库 API |
| --- | --- |
| 列出/创建 | GET/POST repos/{owner}/{repo}/hooks |
| 读取/编辑/删除 | GET/PATCH/DELETE repos/{owner}/{repo}/hooks/{hook_id} |
| ping | POST repos/{owner}/{repo}/hooks/{hook_id}/pings |
| 投递记录 | GET repos/{owner}/{repo}/hooks/{hook_id}/deliveries |
| 重投递 | POST repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts |

创建或修改使用已审阅 JSON，保留其他事件和配置，不回显 secret。接收端使用原始请求体校验签名、限制重放并去重 delivery ID。成功 ping 只证明该次交互；核对真实事件的响应码与接收结果。重投递会重复产生业务副作用，先确认接收端幂等与授权。

hook secret、payload、headers 可能包含敏感信息；只摘录必要错误。删除 hook 不会撤销已泄露凭证。

## GitHub Apps 与 OAuth

区分 App 本身、installation、installation token、user access token 和 OAuth token。读取安装在哪个账号、允许哪些仓库、权限与订阅事件；安装不代表所有仓库可用。

按任务选择现有安装及最小权限。新建 App、改权限、增加仓库访问需对应授权并考虑组织审批。App 私钥签发 JWT、installation token 的过期与刷新在安全凭证系统处理，不把私钥/token 写进技能或日志；不要尝试从另一个用户会话提取凭证。

OAuth callback、state、PKCE（支持时）、撤销流程遵照当前官方文档。卸载 App、撤销 token、删除 webhook 是不同操作，按范围核对残余自动化。

## MCP、CLI 扩展与 Actions 集成

只用宿主暴露的实际工具；缺写接口时可在已有授权与可用凭证范围内用 gh/API，不编造“创建仓库”工具。安装第三方 MCP/CLI extension/Action 前检查来源、权限和执行内容；用户要求使用某工具不等于允许其下载后自动执行任意脚本。

排错按“目标主机→账号/installation→仓库可见性→权限→接口能力→限流/网络”定位。已提交远端对象后超时应先查询结果，避免重复调用。

官方：<https://docs.github.com/en/rest/repos/webhooks>、<https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries>、<https://docs.github.com/en/rest/apps/apps>、<https://docs.github.com/en/apps>。
