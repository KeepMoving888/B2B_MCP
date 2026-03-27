# Dockerfile - CarPlay适配器B2B询盘助手
# 多阶段构建，优化镜像大小
FROM python:3.11-slim as builder

# 维护者信息
LABEL maintainer="CarPlay B2B Inquiry Helper Team"
LABEL version="1.0.0"
LABEL description="CarPlay适配器B2B智能询盘助手"

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DEFAULT_TIMEOUT=100

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖到临时目录
RUN pip install --user -r requirements.txt

# 生产阶段
FROM python:3.11-slim

# 维护者信息
LABEL maintainer="CarPlay B2B Inquiry Helper Team"
LABEL version="1.0.0"
LABEL description="CarPlay适配器B2B智能询盘助手"

WORKDIR /app

# 创建非root用户
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH=/home/appuser/.local/bin:$PATH \
    TZ=Asia/Shanghai

# 安装必要的系统工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制Python依赖
COPY --from=builder /root/.local /home/appuser/.local

# 复制应用代码
COPY . .

# 创建日志目录并设置权限
RUN mkdir -p logs && chown -R appuser:appgroup /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8000 8501

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 默认启动MCP服务器
CMD ["python", "mcp_server/server.py"]
