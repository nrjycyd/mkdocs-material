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
    container_name: mkdocs-material
    restart: always
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

在站点 `mkdocs.yml` 中按需启用：

```yaml
plugins:
  - awesome-pages
  - macros
  - glightbox
  - statistics
```
