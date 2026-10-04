# 分支保护、Rulesets 与权限

## 先看有效规则

检查仓库规则、组织继承规则、传统 branch protection、required checks、review、CODEOWNERS、签名、部署要求和 bypass actors。新增规则可能与现有规则叠加。

```powershell
gh ruleset list --repo $repo
gh ruleset view $rulesetId --repo $repo
gh ruleset check $branch --repo $repo
```

分支匹配规则、check 名称与来源 app ID 必须来自实际配置。pending 与缺失检查不是通过；管理员可能受规则约束，也可能有 bypass，不默认使用。

## 创建和更新

| 对象 | API 路由 |
| --- | --- |
| 仓库 rulesets | GET/POST repos/{owner}/{repo}/rulesets |
| 单个 ruleset | GET/PUT/DELETE repos/{owner}/{repo}/rulesets/{id} |
| 传统分支保护 | GET/PUT/DELETE repos/{owner}/{repo}/branches/{branch}/protection |
| 组织 rulesets | GET/POST orgs/{org}/rulesets |

先读当前对象及官方 schema，准备只含允许写入字段的 JSON，保留不相关规则；不要把 GET 原样 PUT（只读字段、null、遗漏字段可能改变行为）。比较旧/新 enforcement、条件、bypass 和 rules。需要渐进上线时检查计划是否支持 evaluate 模式；不假设所有账户可用。

传统保护的 PUT 可能替换整组设置，尤其 required_status_checks、reviews、restrictions；先完整保留预期配置，再定点修改。不要通过清空规则修 CI 或允许强推。

## 权限与验证

权限要区分读取内容、推分支、审核、合并、管理设置、组织所有者；不能把 repo write 当作 admin。优先读取 `/collaborators/{username}/permission` 或实际对象权限。对团队/自定义角色/Enterprise 策略查组织模块。

修改后读回规则，检查实际目标分支匹配及保护效果；无必要不创建破坏性试验提交。禁用规则、增加 bypass、删除保护需明确包含这些效果的授权。报告规则已保存与规则已生效的区别。

官方：<https://cli.github.com/manual/gh_ruleset>、<https://docs.github.com/en/rest/repos/rules>、<https://docs.github.com/en/rest/branches/branch-protection>、<https://docs.github.com/zh/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches>。
