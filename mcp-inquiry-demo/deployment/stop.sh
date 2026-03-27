#!/bin/bash

# CarPlay适配器B2B询盘助手 - 停止脚本
# 用于停止MCP服务器和前端Web界面

echo "========================================"
echo "CarPlay适配器B2B询盘助手 - 停止脚本"
echo "========================================"

# 检查是否在正确的目录
if [ ! -f "docker-compose.yml" ]; then
    echo "错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查Docker是否安装
echo "检查Docker状态..."
if ! command -v docker &> /dev/null; then
    echo "错误：Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误：Docker Compose未安装"
    exit 1
fi

echo "Docker状态正常"

# 停止服务
echo "正在停止服务..."
docker-compose down

if [ $? -ne 0 ]; then
    echo "错误：服务停止失败"
    exit 1
fi

echo "服务停止成功！"

# 清理未使用的资源
echo "正在清理资源..."
docker system prune -f

echo ""
echo "========================================"
echo "服务已停止"
echo "========================================"
echo "停止完成！"
