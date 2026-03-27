# CarPlay适配器B2B询盘助手 - 交付清单

## 项目概述

基于MCP协议的跨境B2B智能询盘助手，专为CarPlay适配器行业打造，提供库存查询、报价计算、物流查询和多语言翻译等功能。

## 交付内容

### 核心文件

| 文件/目录 | 说明 | 位置 |
|----------|------|------|
| `mcp_server/` | MCP服务器核心代码 | `mcp_server/` |
| `web/` | 前端Web界面代码 | `web/` |
| `app/` | FastAPI应用（预留扩展） | `app/` |
| `Dockerfile` | Docker镜像构建文件 | 根目录 |
| `docker-compose.yml` | Docker Compose配置文件 | 根目录 |
| `requirements.txt` | Python依赖包配置 | 根目录 |
| `.env` | 环境变量配置文件 | 根目录 |
| `README.md` | 项目说明文档 | 根目录 |

### 部署脚本

| 脚本文件 | 功能 | 位置 |
|---------|------|------|
| `start.sh` | 启动服务脚本 | `deployment/` |
| `stop.sh` | 停止服务脚本 | `deployment/` |
| `health_check.sh` | 健康检查脚本 | `deployment/` |

### 配置文件

| 配置文件 | 说明 | 位置 |
|---------|------|------|
| `.env` | 环境变量配置 | 根目录 |
| `.env.example` | 环境变量示例模板 | 根目录 |

## 部署说明

### 环境要求

- Docker 20.10+
- Docker Compose 1.29+
- 服务器资源：至少 1GB RAM，1 CPU核心
- 网络：开放 8000 和 8501 端口

### 快速部署

1. **准备环境**：
   - 安装Docker和Docker Compose
   - 克隆项目代码

2. **配置环境变量**：
   - 编辑 `.env` 文件，填入Qwen API密钥
   - 调整其他配置参数（如端口、部署环境等）

3. **启动服务**：
   ```bash
   cd deployment
   ./start.sh
   ```

4. **验证部署**：
   - 访问健康检查端点：`http://服务器IP:8000/health`
   - 访问前端界面：`http://服务器IP:8501`

### 服务访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| MCP服务器 | http://localhost:8000 | 核心API服务 |
| 前端界面 | http://localhost:8501 | Web操作界面 |
| 健康检查 | http://localhost:8000/health | 服务健康状态 |
| 工具列表 | http://localhost:8000/list_tools | 可用工具查询 |

## 功能验证

### 工具调用测试

1. **库存查询**：
   ```bash
   curl -X POST http://localhost:8000/call_tool \
     -H "Content-Type: application/json" \
     -d '{"name": "get_product_stock", "arguments": {"product_model": "CPA-W1"}}'
   ```

2. **报价计算**：
   ```bash
   curl -X POST http://localhost:8000/call_tool \
     -H "Content-Type: application/json" \
     -d '{"name": "calculate_quote", "arguments": {"product_model": "CPA-W1", "quantity": 1000, "destination_port": "LOS ANGELES"}}'
   ```

3. **物流查询**：
   ```bash
   curl -X POST http://localhost:8000/call_tool \
     -H "Content-Type: application/json" \
     -d '{"name": "get_logistics_info", "arguments": {"destination_port": "LOS ANGELES", "weight": 0.3, "quantity": 1000}}'
   ```

4. **翻译功能**：
   ```bash
   curl -X POST http://localhost:8000/call_tool \
     -H "Content-Type: application/json" \
     -d '{"name": "translate_text", "arguments": {"text": "我想采购CarPlay适配器", "target_language": "en"}}'
   ```

## 监控与维护

### 日志管理

- **Docker日志**：
  ```bash
  docker-compose logs -f
  docker-compose logs mcp-server
  docker-compose logs web-ui
  ```

- **应用日志**：
  - MCP服务器日志：`logs/mcp_server.log`

### 常见问题处理

| 问题 | 解决方案 |
|------|----------|
| 端口被占用 | 修改 `.env` 文件中的 `PORT` 配置 |
| API调用失败 | 检查Qwen API密钥和网络连接 |
| 容器启动失败 | 查看容器日志：`docker-compose logs` |
| 前端无法连接后端 | 检查 `MCP_SERVER_URL` 配置 |

## 性能优化建议

1. **生产环境**：
   - 使用专用服务器或云服务
   - 配置合适的资源限制
   - 启用HTTPS

2. **扩展建议**：
   - 集成真实的ERP/物流API
   - 添加数据库存储
   - 实现用户认证系统
   - 集成监控系统

## 技术支持

- **文档**：参考 `README.md`
- **健康检查**：运行 `deployment/health_check.sh`
- **服务管理**：使用 `start.sh` 和 `stop.sh` 脚本

---

**交付完成！** 🚗
