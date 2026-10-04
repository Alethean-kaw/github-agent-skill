# Projects 看板与规划

使用当前 Projects（ProjectV2），不要照搬旧 Projects classic API。区分用户和组织所有者、项目数字编号、项目 node ID、条目 ID、Issue ID、字段 ID 与选项 ID。

## 查询、建项与关联

```powershell
gh project list --owner $owner --format json
gh project view $projectNumber --owner $owner --format json
gh project field-list $projectNumber --owner $owner --format json
gh project item-list $projectNumber --owner $owner --limit 100 --format json
gh project create --owner $owner --title $title --format json
gh project item-add $projectNumber --owner $owner --url $issueUrl --format json
```

项目存在时复用；添加 Issue/PR 前检查重复。list 的上限与嵌套字段分页需核对。新建草稿条目、关联仓库、复制、关闭、归档与删除分别用 project 子命令，先检查 help 和目标范围。

## 修改状态或自定义字段

先从 field-list 找实际字段及选项 ID，从 item-list 找条目 ID，不能把中文“进行中”硬编码成任意选项：

```powershell
gh project item-edit --project-id $projectId --id $itemId --field-id $fieldId --single-select-option-id $optionId
```

文本、数值、日期、iteration 按字段类型选择当前 CLI 支持的参数；不要把 iteration 标题当 ID。多个字段逐项修改并读取验证。项目状态不自动等同于 Issue open/closed；修改项目条目不表示改了 Issue 正文。

## 自动化、视图和权限

视图布局、筛选、工作流、批量导入/自动添加、项目角色等按当前 GraphQL schema 或官方界面处理；不能假定 CLI 有覆盖。读取项目访问权限和 token 支持情况，不自动申请更大 scope。删除条目与删除其关联 Issue 是不同操作，归档优先保留记录。完成后核对项目 ID、条目、字段值和 URL。

官方：<https://cli.github.com/manual/gh_project>、<https://cli.github.com/manual/gh_project_item-edit>、<https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects>。
