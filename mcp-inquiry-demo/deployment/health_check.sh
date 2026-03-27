#!/bin/bash

# CarPlay适配器B2B询盘助手 - 健康检查脚本
# 用于检查服务状态

echo "========================================"
echo "CarPlay适配器B2B询盘助手 - 健康检查脚本"
echo "========================================"

# 检查服务状态
echo "检查Docker服务状态..."
docker-compose ps

echo ""
echo "检查MCP服务器健康状态..."
MCP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)

if [ "$MCP_STATUS" == "200" ]; then
    echo "✓ MCP服务器健康状态正常"
    echo "服务器响应："
    curl -s http://localhost:8000/health
    echo ""
else
    echo "✗ MCP服务器健康状态异常，HTTP状态码：$MCP_STATUS"
fi

echo ""
echo "检查前端界面状态..."
WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8501)

if [ "$WEB_STATUS" == "200" ]; then
    echo "✓ 前端界面状态正常"
else
    echo "✗ 前端界面状态异常，HTTP状态码：$WEB_STATUS"
fi

echo ""
echo "检查工具列表..."
TOOLS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:8000/list_tools -H "Content-Type: application/json" -d '{}')

if [ "$TOOLS_STATUS" == "200" ]; then
    echo "✓ 工具列表获取成功"
    echo "可用工具："
    curl -s -X POST http://localhost:8000/list_tools -H "Content-Type: application/json" -d '{}' | jq '.tools[].name'
else
    echo "✗ 工具列表获取失败，HTTP状态码：$TOOLS_STATUS"
fi

echo ""
echo "========================================"
echo "健康检查完成"
echo "========================================"
