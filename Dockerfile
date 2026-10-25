# syntax=docker/dockerfile:1
# VERSION 是基础版本的唯一来源，由 GitHub Actions 读取并传入此参数。
ARG MKMATERIAL_VERSION
FROM squidfunk/mkdocs-material:${MKMATERIAL_VERSION}

# 依赖锁包含基础主题及其 extras，避免插件安装时悄悄改变依赖版本。
# pip 缓存留在 BuildKit 中，不进入最终镜像；两种架构使用独立缓存。
ARG TARGETARCH
COPY requirements.txt /tmp/requirements.txt
RUN --mount=type=cache,id=mkdocs-pip-${TARGETARCH},target=/root/.cache/pip,sharing=locked \
    PIP_NO_CACHE_DIR=false python -m pip install --require-hashes -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# 每种目标架构均须通过验证，测试源码与生成站点不进入镜像。
RUN --mount=type=bind,source=tests/smoke,target=/tmp/mkdocs-smoke \
    python -m pip check \
    && python /tmp/mkdocs-smoke/check.py

WORKDIR /docs
EXPOSE 8000
