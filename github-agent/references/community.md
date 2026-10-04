# Discussions、Gists、Wiki、社交与社区

## Discussions

先 `gh discussion --help` 检查本机是否支持；不可用则查 GraphQL。获取 repository ID、分类 ID、讨论 node ID 和评论连接；讨论编号不是 mutation ID。

读取分类及其格式后准备标题/正文；创建、编辑、评论、回复、标记答案、取消答案、锁定/解锁、置顶和删除各按具体授权执行。GraphQL 对应 mutation 与字段以当前 schema 为准，不能把 Issue comments API 用于 Discussion。写后查作者、正文、分类、URL 与答案状态，嵌套回复单独分页。

## Gists

```powershell
gh gist list --limit 100
gh gist view $gistId
gh gist create $filePath --desc $description
gh gist clone $gistId $localPath
```

创建前确认公开还是 secret；secret gist 只是未列出，不是访问控制，不可存凭证或私有资料。公开创建需显式使用 `--public` 并符合用户意图。编辑/增加文件、改名、删除先查 help，核对 gist ID 与文件名；修改后读取真实内容和 URL。不要把 gist 当完整仓库备份。

## Wiki 与社区文件

Wiki 通常是独立 Git 仓库，先核对页面启用与现有地址，再按正常 Git 流程克隆对应 `.wiki.git`；没有 Wiki 或权限不足时不自动创建替代网站。页面标题、链接和附件要在渲染端验证。

社区资料包括 README、贡献说明、行为准则、安全报告入口、许可证、CODEOWNERS、Issue Forms、PR 模板和 FUNDING。新增文件按项目实际流程，不虚构维护者、联系方式或许可授权。模板 YAML 与 Issue Forms 字段需按官方 schema 检查。

## 通知、Star、Watch、Follow 与互动

通知读写查 activity API；标全部已读需要明确全部范围。Star 是收藏关系，Watch 是订阅，不应为安装技能自动 star/follow。回应表情、评论、@提及、赞助和公布公告属于远端互动，须已获相应授权；不要把本地分析自动发给其他人。

赞助与付费支持走官方界面并核对金额/周期，不能从用户喜欢某项目推导支付意图。用户要求导出收藏时说明分页与时间点。

官方：<https://docs.github.com/en/graphql/guides/using-the-graphql-api-for-discussions>、<https://cli.github.com/manual/gh_gist>、<https://docs.github.com/en/communities/documenting-your-project-with-wikis>、<https://docs.github.com/en/rest/activity>。
