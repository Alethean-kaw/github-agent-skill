# 备份、迁移、导出与批量操作

## 先定义备份对象

| 对象 | 方法与遗漏 |
| --- | --- |
| Git 历史和引用 | mirror clone 或 bundle；不包含未提交工作树和平台对象 |
| LFS | 单独获取 LFS 实体，检查配额与下载结果 |
| 子模块 | 记录各 gitlink SHA，分别备份对应仓库 |
| Wiki | 单独备份 .wiki.git |
| Issue/PR/评论/项目 | API 分页导出，保留 ID、关系、时间与来源 |
| Release/Packages/Artifacts | 分别下载元数据及实体，验证文件大小/哈希与保留期 |
| 配置/权限/集成 | 导出非秘密配置；Secrets 明文不可通过 GitHub 读回 |

备份目录使用用户指定的访问控制，不公开私库数据。`git clone --mirror $url $backupPath` 仅对明确新目标执行；更新 mirror 可能同步删除引用，保留版本化快照。

## 恢复与迁移

先验证 bundle 或 clone 能读取预期历史，在隔离目录做恢复验证。不要为了测试恢复而覆盖线上仓库。还原内容与引用后核对 tags、默认分支、LFS 和子模块。

`git push --mirror` 可能覆盖/删除目标引用，必须预先比较源/目标 refs 和明确允许的删除范围；普通发布不用 mirror。平台导出的 JSON 并不保证可原样导回，编号、作者、时间、URL、权限和系统对象可能不能保留。迁移工具是否支持目标账号/计划/大小应查当前文档。

跨所有者迁移时核对许可证、组织政策、SSO、团队、Apps、Secrets、Pages、Packages、链接和 CI；源端只在目标验证完成且用户明确要求后处理。失败保留源与可恢复状态。

## 批量策略与报告

先只读产生精确对象清单、总数、筛选条件与目标变化。可恢复任务小批执行，记录每个对象的前后状态与错误；尊重 API 限流。超时先查询，重试仅覆盖未完成项。不在输出中展示私密数据或 token。

审计报告区分源对象数、导出数、成功恢复数、缺失/跳过及不可迁移项，不把“文件生成成功”当作完整备份成功。

官方：<https://git-scm.com/docs/git-bundle>、<https://git-scm.com/docs/git-clone>、<https://docs.github.com/en/rest/migrations>、<https://docs.github.com/en/repositories/archiving-a-github-repository/backing-up-a-repository>。
