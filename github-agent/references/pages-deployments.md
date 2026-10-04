# Pages、部署与网站发布

## Pages 检查与配置

先读 `GET repos/{owner}/{repo}/pages`，确认源为分支/目录还是 Actions，检查 Pages URL、build 状态、CNAME、自定义域和 HTTPS。404 可能未启用或无权访问；不能据此改成公开仓库。

通过 Pages API 创建/更新时先查当前 schema 的 source/build_type，核对目标分支和构建输出位置；按已有框架的构建方式准备工作流，不硬套静态根目录。选择 Actions 时使用官方 Pages upload/deploy action 并固定经核验的版本；只给所需 contents/pages/id-token 权限，设置对应 environment。

推代码可能触发上线；部署前核对公开产物中无秘密、源码映射/草稿是否符合要求。Pages 地址不要按 OWNER.github.io/REPO 猜；读 API 的实际 URL。

## 自定义域与验证

先确认用户控制域名，说明需要的 DNS 记录；DNS 变更只在已授权的域名系统操作。区分 Pages CNAME、DNS 指向、域名验证、证书签发和 HTTPS enforcement。避免残留 DNS 指向失效 Pages 造成域名接管风险，停站时协调 DNS 与仓库配置。

配置保存不等于部署成功。查看相应 workflow/run 或 Pages build，再请求实际 URL，核对状态、关键内容、静态资源与路径基址；证书/DNS 尚未生效时说明状态，不反复切配置。

## 通用 Deployments

`GET/POST repos/{owner}/{repo}/deployments` 与 `GET/POST .../deployments/{id}/statuses` 用于记录部署对象和状态。仅创建 deployment 记录不代表应用已部署；状态必须来自真实部署结果，不把失败改为 success。

上线明确目标环境、SHA、操作者、构建产物和验证方法；回滚按系统的发布机制选择既有稳定版本。重跑旧 Actions 不自动等于安全回滚，数据库/外部系统变化需要单独判断。第三方托管用其实际工具，GitHub 技能只处理 GitHub 部分。

官方：<https://docs.github.com/en/rest/pages/pages>、<https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages>、<https://docs.github.com/en/rest/deployments/deployments>。
