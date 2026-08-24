# mkdocs-material

基于官方 [`squidfunk/mkdocs-material`](https://hub.docker.com/r/squidfunk/mkdocs-material) 的预装插件镜像，开箱即用，省去每次本地 `pip install`。

镜像地址（GitHub Container Registry）：

```
ghcr.io/nrjycyd/mkdocs-material:latest
```

## 预装插件

| 插件 | 用途 |
| --- | --- |
| mkdocs-awesome-pages-plugin | 灵活管理页面导航（自定义排序、隐藏页面、自定义导航标题） |
| mkdocs-macros-plugin | Markdown 中使用 Jinja2 宏（变量、函数、模板语法） |
| mkdocs-glightbox | 图片/视频灯箱效果，点击放大、幻灯片播放 |
| mkdocs-statistics-plugin | 生成站点静态统计数据（页面数/字数/标签等） |
| mkdocs-table-reader-plugin | 在 Markdown 中直接渲染 CSV/JSON/Excel 等表格数据 |
| mkdocs-markdown-exec | 在文档中执行代码块并嵌入其输出（bash/python/…） |
| mkdocs-markmap | 将 Markdown 列表渲染为思维导图 |
| mkdocs-plantuml | PlantUML 图表支持（通过 puml_url 远程服务渲染） |
| mkdocs-literate-nav | 基于文件系统自动生成导航 |
| mkdocstrings（python） | 从 Python docstring 自动生成 API 文档 |
| mkdocs-rss-plugin | 生成 RSS 订阅源 |
| mkdocs-minify-plugin | 构建时压缩 HTML/JS/CSS |
| mkdocs-git-revision-date-localized-plugin | 显示页面最后更新时间 |
| mkdocs-git-committers-plugin-2 | 显示页面贡献者 |

## 使用

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
plugins:
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
```

## 注意事项

- `markdown-exec` 会**真正执行**代码块：镜像基于 alpine，已含 python3；若用到 bash 等其它解释器需确保其存在于容器内。
- `plantuml` 通过远程 `puml_url` 渲染，无需本地 Java 环境。
