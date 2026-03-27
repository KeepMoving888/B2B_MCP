#!/bin/bash

# CarPlay适配器B2B询盘助手 - 启动脚本
# 用于启动MCP服务器和前端Web界面

echo "========================================"
echo "CarPlay适配器B2B询盘助手 - 启动脚本"
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

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "警告：.env文件不存在，使用默认配置"
    if [ -f ".env.example" ]; then
        echo "正在从.env.example复制..."
        cp .env.example .env
    else
        echo "错误：.env.example文件也不存在"
        exit 1
    fi
fi

echo "环境变量配置就绪"

# 构建和启动服务
echo "正在构建和启动服务..."
docker-compose up -d --build

if [ $? -ne 0 ]; then
    echo "错误：服务启动失败"
    exit 1
fi

echo "服务启动成功！"

# 检查服务状态
echo "正在检查服务状态..."
sleep 5
docker-compose ps

echo ""
echo "========================================"
echo "服务访问地址："
echo "MCP服务器：http://localhost:8000"
echo "前端界面：http://localhost:8501"
echo "健康检查：http://localhost:8000/health"
echo "========================================"
echo "启动完成！"
