# 组织、团队、Enterprise 与账号设置

## 对象与访问审计

确认是个人、组织还是 Enterprise，读取实际角色；仓库管理员不等于组织所有者。区分成员、外部协作者、待接受邀请、团队成员和团队 maintainer。

| 查询 | REST 入口 |
| --- | --- |
| 组织信息/成员 | GET orgs/{org} / orgs/{org}/members |
| 外部协作者 | GET orgs/{org}/outside_collaborators |
| 邀请 | GET orgs/{org}/invitations |
| 团队列表 | GET orgs/{org}/teams |
| 团队成员/仓库 | GET orgs/{org}/teams/{team_slug}/members 或 /repos |
| 审计日志 | GET orgs/{org}/audit-log（依套餐和权限） |

完整分页，记录查询时间窗口；不要输出不相关邮箱和隐私字段。审计日志、公开事件和 Git 提交记录不是同一类证据。

## 成员、团队与仓库授权

邀请前核对用户身份、目标组织、角色和可能的席位费用；邀请已创建不等于成员已加入。更新团队先读 slug、父团队、隐私设置、维护者和继承关系。

按当前 Teams/Members API 创建团队、添加成员、授予仓库角色；使用最小满足需求的角色，操作后读取 membership/permission。批量修改先列清单和差异，不全量覆盖未知成员。移除成员可能移除多仓库访问、影响分配和自动化；核对外部协作者转换及尚未接受邀请。

组织级安全经理、自定义角色、Rulesets、Actions 策略、应用限制、默认仓库权限和 2FA 要求需要组织权限。变更不能隐含于单仓库修复中；按当前官方 schema 和具体范围处理。

## Enterprise、SSO 与身份管理

确认 Cloud/GHES、企业版本、托管用户和 IdP。SAML/SCIM/Enterprise Managed Users 的生命周期按组织既有流程处理，不使用普通邀请替代 IdP provisioning；SSO 授权 token 与增加 token scope 不同。

企业审计、runner groups、IP allowlist、许可/seat、迁移和策略分别查对应官方文档。API 不存在于目标 GHES 版本时说明差异，不能反复尝试 Cloud 路由。身份/安全登录设置或无接口的操作由官方界面与用户接管完成，不索取密码、恢复码和 MFA 验证码。

## 计费、配额和账号配置

先只读了解 Actions、Packages、Codespaces 等用量、预算和支出限制。升级计划、增加席位、赞助、购买资源或移除支出限制必须在用户已授权的具体对象/费用范围内进行；无法确认价格先查当前官方计费资料。

用户资料、邮箱、SSH/GPG key、通知偏好、token 撤销和账号删除分别核对身份与影响。部署公钥不应上传到个人账号冒充登录密钥。只报告必要状态，不展示秘密。

官方：<https://docs.github.com/en/rest/orgs/members>、<https://docs.github.com/en/rest/teams/teams>、<https://docs.github.com/en/rest/orgs/security-managers>、<https://docs.github.com/en/enterprise-cloud@latest/admin>、<https://docs.github.com/en/billing>。
