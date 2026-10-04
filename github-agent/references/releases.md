# Tag 与 Release

区分本地 tag、远端 tag、Release 草稿、正式发布。创建草稿是远端写入，推 tag 可能触发部署，需要相应授权。

确认仓库、版本、完整目标 SHA、是否预发布、资产、授权范围。核对现有 tag/release 和 CI，不默认当前 HEAD 或默认分支最新提交。已有同名 tag 指向别处时不覆盖。

```powershell
gh release list --repo $repo --limit 20
git tag --list
git ls-remote --tags $remote
git rev-parse "$tag^{commit}"
```

不存在的 tag 解析失败是预期分支。需要创建且有授权时 `git tag -a $tag $targetSha -m $tagMessage`，核对后仅 `git push $remote "refs/tags/$tag"`。按项目要求签名，缺密钥不自动取消。

远端 tag 已存在且 SHA 正确后：

```powershell
gh release create $tag --repo $repo --verify-tag --draft --title $title --notes-file $notesPath
gh release view $tag --repo $repo --json url,tagName,isDraft,isPrerelease,assets
```

--verify-tag 防止 gh 自动从错误基线建 tag。用户明确正式发布时完成检查后移除 --draft 或编辑已有草稿，并核对 isDraft=false；需要预发布则 --prerelease。不把草稿报告成正式发布。

资产核对名称、架构、版本、构建来源和校验和。不上传 .env 或整个工作区，不自动 --clobber 覆盖。发布、替换资产、删除 release、删 tag 各有不同影响。

官方：<https://cli.github.com/manual/gh_release_create>、<https://cli.github.com/manual/gh_release_upload>、<https://git-scm.com/docs/git-tag>。

## 资产、下载与版本维护

```powershell
gh release upload $tag $artifactPath --repo $repo
gh release download $tag --repo $repo --pattern $assetPattern --dir $newDownloadDir
gh release edit $tag --repo $repo --notes-file $notesPath
gh release edit $tag --repo $repo --draft=false
```

发布已有草稿前复查 tag SHA、资产、notes、CI 和预发布标志。自动生成 notes 时检查比较起点和包含的 PR，人工核对破坏性变更，不能把生成文字当完整事实。

上传先检查文件内容、平台架构、版本和校验和；重名先读取旧资产元数据，不自动 `--clobber`。覆盖应明确获准，并保留用户需要的旧文件。下载 pattern 可能匹配多个文件，完成后逐个验证。默认源代码 ZIP/TAR 不等于用户上传的构建产物。

删除 asset、Release 和远端 tag 是不同动作；删除 Release 不自动删除 tag。查 `gh release delete-asset/delete --help`，只删除指定对象，不顺手 --cleanup-tag。latest、prerelease 与 draft 语义不同，按用户需求更新并读回。

启用了 immutable releases 的仓库先查限制，不承诺可编辑或覆盖资产。签名/attestation 核验见安全模块；版本回滚不能靠改名旧资产伪装新版本。
