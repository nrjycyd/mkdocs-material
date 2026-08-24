# 基础镜像版本由 VERSION 文件单一来源控制（workflow 通过 build-args 传入）
ARG MKMATERIAL_VERSION=9.7.7
FROM squidfunk/mkdocs-material:${MKMATERIAL_VERSION}

#### 安装额外插件
# macros              : Markdown 中使用 Jinja2 宏（变量、函数、模板语法）
# statistics          : 生成站点静态统计数据（页面数/字数/标签等）
# glightbox           : 图片/视频灯箱效果，点击放大、幻灯片播放
# table-reader        : 在 Markdown 中直接渲染 CSV/JSON/Excel 等表格数据
# markdown-exec       : 在文档中执行代码块并嵌入其输出（bash/python/...）
# markmap             : 将 Markdown 列表渲染为思维导图
# plantuml            : PlantUML 图表支持（通过 puml_url 远程服务渲染）
# literate-nav        : 基于文件系统自动生成导航
# mkdocstrings[python]: 从 Python  docstring 自动生成 API 文档（含 autorefs 依赖）
RUN pip install --no-cache-dir \
    mkdocs-macros-plugin==1.3.7 \
    mkdocs-statistics-plugin==0.1.5 \
    mkdocs-glightbox==0.4.0 \
    mkdocs-table-reader-plugin==3.1.0 \
    markdown-exec==1.12.3 \
    mkdocs-markmap==2.5.2 \
    mkdocs-plantuml==0.1.1 \
    mkdocs-literate-nav==0.6.3 \
    "mkdocstrings[python]==1.0.6"

WORKDIR /docs
EXPOSE 8000
