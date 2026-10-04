# 安全告警、依赖与供应链

## 读取告警

先确定仓库和扫描权限，避免将敏感告警正文复制到公开 Issue。按需读取：

| 类型 | REST 入口 |
| --- | --- |
| Dependabot | GET repos/{owner}/{repo}/dependabot/alerts |
| Code scanning | GET repos/{owner}/{repo}/code-scanning/alerts |
| Secret scanning | GET repos/{owner}/{repo}/secret-scanning/alerts |
| 仓库安全公告 | GET repos/{owner}/{repo}/security-advisories |

无结果可能为未启用、无扫描、无权限或真的无告警；不能报告绝对安全。记录 alert ID、规则、受影响版本/位置、状态、扫描 ref 和最新结果。secret scanning 响应可能包含秘密值，使用白名单字段输出并脱敏。

## 修复与验证

Dependabot 先读依赖清单/锁文件和上游修复范围，最小升级并做兼容性测试；不删除锁文件掩盖漏洞。CodeQL/code scanning 阅读真实数据流与路径，核对误报依据和扫描 SHA；本地通过后仍等待新扫描结果。

secret 泄漏先撤销/轮换并确认使用方，随后清理当前代码；删除文件不代表凭证安全。历史清理另按明确授权和协作计划执行，不能顺手 force push。

dismiss/reopen 使用对应 PATCH schema，reason/comment 反映事实。修改告警状态不等于修复漏洞；批准风险接受需要相应授权。涉及未公开漏洞时准备私有安全公告，不在公开 PR 泄露利用细节。

## 启用和维护扫描

检查 `.github/dependabot.yml`、CodeQL workflow、默认 setup、分支和语言支持，按套餐与仓库权限选择可用机制。配置更新走正常 diff/测试/提交流程；扫描会运行代码和消耗额度，按任务范围执行。

## 制品证明与签名

发布前核验构建来源和 digest；有 attestation 时按当前 `gh attestation verify --help` 指定预期 repo/owner 和文件。校验和只能证明文件一致性，不能单独证明可信来源。签名、证明身份、构建工作流和被验证文件需对应；不因“Verified”忽略权限和构建输入。

官方：<https://docs.github.com/en/rest/dependabot/alerts>、<https://docs.github.com/en/rest/code-scanning/code-scanning>、<https://docs.github.com/en/rest/secret-scanning/secret-scanning>、<https://docs.github.com/en/rest/security-advisories/repository-advisories>、<https://cli.github.com/manual/gh_attestation_verify>。
