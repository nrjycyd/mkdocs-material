# mkdocs-material

基于官方 [`squidfunk/mkdocs-material`](https://hub.docker.com/r/squidfunk/mkdocs-material) 的预装插件镜像，开箱即用，省去每次本地 `pip install`。

镜像地址（GitHub Container Registry）：

```
ghcr.io/nrjycyd/mkdocs-material:latest
```

## 预装插件

以下 12 个插件均在 `requirements.in` 中声明，并通过 `requirements.txt` 固定直接依赖、传递依赖及下载文件哈希。`search` 由 MkDocs 自带。awesome-pages 和 RSS 未预装。

PlantUML 使用与下方 `plantuml` / `puml_url` 配置对应的 `mkdocs_puml`，替换原先提供 `plantuml-colocator` 的 `mkdocs-plantuml`。PyMdown 固定为 `11.0.2`，以兼容当前 `markdown-exec` 和 `mkdocstrings` 的渲染接口。

| 插件 | 用途 |
| --- | --- |
| mkdocs-macros-plugin | Markdown 中使用 Jinja2 宏（变量、函数、模板语法） |
| mkdocs-glightbox | 图片/视频灯箱效果，点击放大、幻灯片播放 |
| mkdocs-statistics-plugin | 生成站点静态统计数据（页面数/字数/标签等） |
| mkdocs-table-reader-plugin | 在 Markdown 中直接渲染 CSV/JSON/Excel 等表格数据 |
| markdown-exec | 在文档中执行代码块并嵌入其输出（bash/python/…） |
| mkdocs-markmap | 将 Markdown 列表渲染为思维导图 |
| mkdocs_puml | PlantUML 图表支持（通过 puml_url 远程服务渲染） |
| mkdocs-literate-nav | 使用 Markdown 导航文件管理导航 |
| mkdocstrings（python） | 从 Python docstring 自动生成 API 文档 |
| mkdocs-minify-plugin | 构建时压缩 HTML/JS/CSS |
| mkdocs-git-revision-date-localized-plugin | 显示页面最后更新时间 |
| mkdocs-git-committers-plugin-2 | 显示页面贡献者 |

## 使用

`latest` 适合跟随更新；需要固定环境时，使用发布后的修订标签（如 `v9.8.0-r1`）或 `sha-<完整提交 SHA>`。新标签会在工作流验证并发布成功后可用。

### Docker

```bash
# 本地预览（当前目录作为 /docs 挂载，端口 8000）
docker run --rm -it -p 8000:8000 \
  -v "$PWD":/docs \
  ghcr.io/nrjycyd/mkdocs-material:latest

# 构建静态站点到 ./site
docker run --rm -it \
  -v "$PWD":/docs \
  ghcr.io/nrjycyd/mkdocs-material:latest build
```

### Docker Compose

```yaml
# compose.yml
services:
  mkdocs:
    image: ghcr.io/nrjycyd/mkdocs-material:latest
    ports:
      - "8000:8000"
    volumes:
      - ./:/docs
    # 本地预览
    command: serve --dev-addr=0.0.0.0:8000
    # 构建静态站点时改为：command: build
```

```bash
docker compose up        # 预览，访问 http://localhost:8000
docker compose run --rm mkdocs build   # 构建静态站点到 ./site
```

## 启用插件

在站点 `mkdocs.yml` 中按需启用（插件均已预装）：

```yaml
site_name: My documentation
theme:
  name: material
plugins:
  - search
  - macros
  - glightbox
  - statistics
  - table-reader
  - markdown-exec
  - markmap
  - plantuml:
      puml_url: https://www.plantuml.com/plantuml/
  - literate-nav
  - mkdocstrings:
      handlers:
        python:
          options:
            show_source: false
            docstring_section_style: spacy
markdown_extensions:
  - pymdownx.superfences
```

显式声明 `plugins` 会覆盖 MkDocs 默认插件列表，因此要保留 `search`。`markdown-exec` 还需要启用 `pymdownx.superfences`，例如：

````markdown
```python exec="on"
print(6 * 7)
```
````

上述列表可按需删减；Git 日期和贡献者插件需要另外配置站点仓库，其中贡献者插件可能需要 GitHub API 令牌。

## 本地构建与验证

在本项目根目录执行；需要支持 BuildKit 的 Docker：

```bash
docker build --build-arg MKMATERIAL_VERSION="$(cat VERSION)" -t mkdocs-material:local .
```

PowerShell：

```powershell
$materialVersion = (Get-Content -Raw VERSION).Trim()
docker build --build-arg "MKMATERIAL_VERSION=$materialVersion" -t mkdocs-material:local .
```

构建会先安装锁定依赖，再执行 `pip check` 和 `mkdocs build --strict`。冒烟检查会验证全部预装插件可导入，并检查宏替换、Python 代码执行、CSV 表格、Python API 文档和搜索索引的实际输出。Git 插件仅检查导入；PlantUML 未发起远程渲染请求。

依赖安装使用 BuildKit 的 pip 缓存挂载，两种架构各用独立缓存；缓存不进入最终镜像。GitHub Actions 另用 GHA 缓存复用构建层，验证与发布可共享已完成的层。`.dockerignore` 仅允许依赖锁和冒烟检查进入构建上下文。

## 更新依赖与发布

### 直接在 GitHub 网页升级插件

无需在本地安装 Python 或执行命令：

1. 将本项目的完整内容上传到 GitHub 仓库根目录的 `main` 分支，保留 `.github/workflows` 目录。
2. 首次使用时，在仓库 **Settings → Actions → General → Workflow permissions** 中启用 **Allow GitHub Actions to create and approve pull requests**。组织策略可能限制此选项。
3. 打开 **Actions → Update Plugins → Run workflow**，选择 `main`，在 `plugin` 下拉框中选择插件，在 `version` 中填写比当前版本更高的目标版本号（不加 `v`）。
4. 工作流会修改插件版本、生成依赖锁、增加镜像修订号，并验证两个架构。通过后，它会创建升级 PR，链接显示在该次运行的 Summary 中。
5. 查看 PR；如果出现 **Approve workflows to run** 提示，先批准 PR 验证。合并 PR 到 `main` 后，**Docker Image** 工作流会再次验证并发布镜像。

升级工作流本身只创建 PR，不直接发布镜像。依赖解析或站点构建失败时不会提交升级。版本号相同、降级或非 `main` 分支不会执行升级。多份升级 PR 应依次处理：若已有另一份升级合并，请从最新 `main` 重新运行，避免重复使用镜像修订号。

仓库需要允许 Actions 使用工作流中声明的 `contents: write` 和 `pull-requests: write` 权限。设置说明见 [GitHub 官方文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository#preventing-github-actions-from-creating-or-approving-pull-requests)。

### 文件与本地维护方式

- `VERSION`：官方基础镜像版本，同时决定锁文件里的主题版本；Dockerfile 不再维护默认版本。
- `IMAGE_REVISION`：当前基础版本下的正整数修订号；插件、依赖锁或镜像行为变化时递增，切换基础版本时可重置为 `1`。
- `requirements.in`：人工维护的直接依赖。
- `requirements.txt`：自动生成的完整依赖锁，适用于 Python 3.11 及两个目标架构，不要手工修改。

安装锁文件工具并重新生成锁文件（更改 `VERSION` 后也需执行）：

```bash
python -m pip install uv==0.12.14
python tools/lock_requirements.py
python tools/lock_requirements.py --check
```

普通重新生成会尽量沿用已锁定版本；主动升级兼容的传递依赖时执行 `python tools/lock_requirements.py --upgrade`，并递增 `IMAGE_REVISION`。

工作流监听版本、Dockerfile、依赖、测试、工具和工作流自身的变化。PR 只验证，不登录或推送镜像；main 分支验证通过后发布 `linux/amd64`、`linux/arm64` 镜像，标签为：

```text
latest
v<基础版本>-r<修订号>  # 如 v9.8.0-r1
sha-<完整提交 SHA>
```

手动运行非 main 分支时也只验证。原来的 `v<基础版本>` 标签不再更新；固定版本的使用者应改用修订标签。

## 注意事项

- `markdown-exec` 会**真正执行**代码块：镜像基于 alpine，已含 python3；若用到 bash 等其它解释器需确保其存在于容器内。
- `plantuml` 通过远程 `puml_url` 渲染，无需本地 Java 环境。
