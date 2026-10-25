# mkdocs-material

预装常用插件的 Material for MkDocs 镜像，可直接用于预览和构建文档站点，无需单独安装 Python 或插件。

镜像地址：

```text
ghcr.io/nrjycyd/mkdocs-material:latest
```

## 快速开始

准备好 Docker，在文档目录中创建以下文件：

```text
my-docs/
├── mkdocs.yml
└── docs/
    └── index.md
```

`mkdocs.yml`：

```yaml
site_name: My documentation
theme:
  name: material
plugins:
  - search
```

在 `docs/index.md` 中写入文档内容，然后在文档目录运行：

```bash
docker run --rm -p 8000:8000 \
  -v "${PWD}:/docs" \
  ghcr.io/nrjycyd/mkdocs-material:latest
```

PowerShell 使用以下单行命令：

```powershell
docker run --rm -p 8000:8000 -v "${PWD}:/docs" ghcr.io/nrjycyd/mkdocs-material:latest
```

访问 [http://localhost:8000](http://localhost:8000) 查看站点，修改文档后会自动重新构建。

## 构建静态站点

在文档目录运行：

```bash
docker run --rm \
  -v "${PWD}:/docs" \
  ghcr.io/nrjycyd/mkdocs-material:latest build --strict
```

生成的静态文件位于文档目录下的 `site/`，可上传到静态网站托管服务。`--strict` 会在构建出现警告时报告失败。

PowerShell 使用以下单行命令：

```powershell
docker run --rm -v "${PWD}:/docs" ghcr.io/nrjycyd/mkdocs-material:latest build --strict
```

## Docker Compose

在文档目录创建 `compose.yml`：

```yaml
services:
  mkdocs:
    image: ghcr.io/nrjycyd/mkdocs-material:latest
    ports:
      - "8000:8000"
    volumes:
      - ./:/docs
    command: serve --dev-addr=0.0.0.0:8000
```

预览站点：

```bash
docker compose up
```

构建静态站点：

```bash
docker compose run --rm mkdocs build --strict
```

## 预装插件

插件已安装，在 `mkdocs.yml` 中按需启用即可。`search` 搜索插件由 MkDocs 自带。

| 插件 | 配置名称 | 用途 |
| --- | --- | --- |
| mkdocs-macros-plugin | `macros` | 在 Markdown 中使用变量、宏和 Jinja2 模板 |
| mkdocs-glightbox | `glightbox` | 图片和视频灯箱 |
| mkdocs-statistics-plugin | `statistics` | 页面和字数等统计 |
| mkdocs-table-reader-plugin | `table-reader` | 读取 CSV、JSON、Excel 等表格 |
| markdown-exec | `markdown-exec` | 执行代码块并嵌入输出 |
| mkdocs-markmap | `markmap` | 将 Markdown 列表渲染为思维导图 |
| mkdocs_puml | `plantuml` | 通过 PlantUML 服务渲染图表 |
| mkdocs-literate-nav | `literate-nav` | 使用 Markdown 文件管理导航 |
| mkdocstrings（Python） | `mkdocstrings` | 从 Python docstring 生成 API 文档 |
| mkdocs-minify-plugin | `minify` | 压缩 HTML、JS 和 CSS |
| mkdocs-git-revision-date-localized-plugin | `git-revision-date-localized` | 显示页面更新时间 |
| mkdocs-git-committers-plugin-2 | `git-committers` | 显示页面贡献者 |

## 启用插件

在快速开始的 `mkdocs.yml` 中，按需扩展 `plugins` 和 `markdown_extensions`：

```yaml
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
  - minify:
      minify_html: true

markdown_extensions:
  - pymdownx.superfences
```

显式声明 `plugins` 会覆盖默认插件列表，需要保留 `search` 才能使用搜索。`markdown-exec` 需要同时启用 `pymdownx.superfences`。

例如，在 Markdown 中执行 Python 代码并显示结果：

````markdown
```python exec="on"
print(6 * 7)
```
````

Git 日期和贡献者插件需要另外配置站点仓库；贡献者插件可能还需要 GitHub API 令牌。

## 更新镜像

使用 Docker 时，先拉取新镜像，再重新运行预览或构建命令：

```bash
docker pull ghcr.io/nrjycyd/mkdocs-material:latest
```

使用 Docker Compose 时：

```bash
docker compose pull
docker compose up -d
```

`latest` 跟随镜像更新。需要固定版本时，将命令或 Compose 配置中的 `latest` 替换为已发布的版本标签，例如 `v9.8.0-r1`。

## 注意事项

- 运行命令时，当前目录应包含 `mkdocs.yml`；该目录会挂载为容器内的 `/docs`。
- `markdown-exec` 会真正执行代码，请只构建可信文档。镜像包含 Python；使用其他解释器前需要确认镜像中已安装。
- PlantUML 图表会发送到 `puml_url` 指定的服务；可将地址改为自己的 PlantUML 服务。
