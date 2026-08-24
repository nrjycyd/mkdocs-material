# 基础镜像版本由 VERSION 文件单一来源控制（workflow 通过 build-args 传入）
ARG MKMATERIAL_VERSION=9.7.7
FROM squidfunk/mkdocs-material:${MKMATERIAL_VERSION}

#### 安装额外插件
# mkdocs-awesome-pages-plugin：灵活管理页面导航（自定义排序、隐藏页面、自定义导航标题）
# mkdocs-macros-plugin：Markdown 中使用 Jinja2 宏（变量、函数、模板语法）
# mkdocs-glightbox：图片/视频灯箱效果，点击放大、幻灯片播放
# mkdocs-statistics-plugin：生成站点静态统计数据（页面数/字数/标签等）
RUN pip install --no-cache-dir \
    mkdocs-awesome-pages-plugin==2.9.3 \
    mkdocs-macros-plugin==1.3.7 \
    mkdocs-glightbox==0.4.0 \
    mkdocs-statistics-plugin==0.1.5

WORKDIR /docs
EXPOSE 8000
