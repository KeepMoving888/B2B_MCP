# CarPlay适配器B2B智能询盘助手

基于MCP协议的跨境B2B智能询盘助手，专为CarPlay适配器行业打造。

## 项目概述

本项目是一个生产级别的CarPlay适配器跨境B2B外贸询盘解决方案，通过MCP（Model Context Protocol）协议实现智能工具调用，为外贸业务员提供高效、专业的询盘处理能力。

## 核心功能

### 1. MCP工具服务
- **库存查询**：实时查询CarPlay适配器产品库存信息
- **报价计算**：智能计算FOB报价，包含MOQ、付款条款等
- **物流查询**：查询海运/空运运费及时效
- **多语言翻译**：支持多语言业务文本翻译

### 2. 智能大模型集成
- 集成Qwen大模型API
- 智能识别询盘意图
- 自动调用相关MCP工具
- 生成专业外贸回复

### 3. 生产级特性
- 完整的日志记录系统
- 错误处理和异常恢复
- 健康检查端点
- Docker容器化部署
- 资源限制和健康监控
- 非root用户运行，提升安全性
- 结构化日志和监控

## 产品型号

| 型号 | 产品名称 | 单价 | 特性 |
|------|---------|------|------|
| CPA-W1 | 无线CarPlay适配器 | $28.5 | 支持有线/无线双模式，iOS 10+ |
| CPA-U2 | 有线CarPlay适配器 | $19.8 | 即插即用，稳定可靠 |
| CPA-PRO | 双系统适配器 | $45.2 | 支持CarPlay+Android Auto |

## 快速开始

### 环境要求

- Python 3.11+
- Git
- Docker（推荐，用于容器化部署）
- Docker Compose（推荐）

### 本地部署

#### 1. 克隆项目

```bash
git clone <repository-url>
cd mcp-inquiry-demo
```

#### 2. 配置环境变量

编辑 `.env` 文件，填入你的API密钥：

```bash
# 编辑 .env 文件
```

详细的环境变量配置说明见文件内注释。

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 启动MCP服务器

```bash
python mcp_server/server.py
```

服务器将在 `http://localhost:8000` 启动。

#### 5. 启动前端界面

在新的终端窗口中：

```bash
streamlit run web/demo_page.py
```

前端界面将在 `http://localhost:8501` 打开。

### Docker部署（推荐）

#### 使用Docker Compose

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看MCP服务器日志
docker-compose logs mcp-server

# 查看前端日志
docker-compose logs web-ui
```

#### 单独构建和运行

```bash
# 构建镜像
docker build -t carplay-inquiry-helper .

# 运行MCP服务器
docker run -d -p 8000:8000 --env-file .env carplay-inquiry-helper

# 运行前端界面
docker run -d -p 8501:8501 --env-file .env \
  -e MCP_SERVER_URL=http://host.docker.internal:8000 \
  carplay-inquiry-helper \
  streamlit run web/demo_page.py --server.port 8501 --server.address 0.0.0.0
```

## 部署指南

### 生产环境部署

1. **配置环境变量**：
   - 修改 `.env` 文件中的 API 密钥和配置
   - 设置 `DEPLOYMENT_ENV=production`

2. **使用Docker Compose部署**：
   ```bash
   docker-compose up -d
   ```

3. **配置反向代理**（可选）：
   - 使用 Nginx 或 Traefik 作为反向代理
   - 配置 HTTPS 证书

4. **监控和日志**：
   - 查看容器日志：`docker-compose logs -f`
   - 检查服务状态：`docker-compose ps`
   - 访问健康检查端点：`http://your-server:8000/health`

### 开发环境部署

1. **配置环境变量**：
   - 设置 `DEPLOYMENT_ENV=development`
   - 启用详细日志

2. **本地运行**：
   ```bash
   # 启动MCP服务器
   python mcp_server/server.py
   
   # 启动前端（新终端）
   streamlit run web/demo_page.py
   ```

## API端点

### MCP服务器端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/metrics` | GET | 简单指标 |
| `/list_tools` | POST | 获取可用工具列表 |
| `/call_tool` | POST | 调用MCP工具 |
| `/process_inquiry` | POST | 处理询盘（预留） |
| `/validate_inquiry` | POST | 验证询盘（预留） |

### 调用工具示例

```bash
# 查询库存
curl -X POST http://localhost:8000/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_product_stock",
    "arguments": {"product_model": "CPA-W1"}
  }'

# 计算报价
curl -X POST http://localhost:8000/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "calculate_quote",
    "arguments": {
      "product_model": "CPA-W1",
      "quantity": 2000,
      "destination_port": "LOS ANGELES"
    }
  }'

# 查询物流
curl -X POST http://localhost:8000/call_tool \
  -H "Content-Type: application/json" \
  -d '{
    "name": "get_logistics_info",
    "arguments": {
      "destination_port": "LOS ANGELES",
      "weight": 0.3,
      "quantity": 2000
    }
  }'
```

## 使用指南

### 前端界面使用

1. 打开浏览器访问 `http://localhost:8501`
2. 在文本框中输入客户询盘内容
3. 选择回复目标语言
4. 点击"生成询盘回复"按钮
5. 查看生成的回复和MCP工具调用详情

### 询盘示例

**中文示例：**
```
我想采购CPA-W1型号的无线CarPlay适配器2000台，目的港洛杉矶，
请问库存有多少，FOB报价是多少，海运运费和时效是多少？
```

**英文示例：**
```
I'm interested in purchasing 1000 units of CPA-PRO model CarPlay adapters.
Can you provide stock info, FOB price for New York port and shipping details?
```

## 项目结构

```
mcp-inquiry-demo/
├── app/                      # FastAPI应用（预留扩展）
│   ├── __init__.py
│   ├── api.py               # API接口
│   └── llm_client.py        # 大模型客户端
├── mcp_server/              # MCP服务器
│   ├── __init__.py
│   ├── server.py            # HTTP服务器（生产级）
│   └── tools.py             # 工具封装
├── web/                      # 前端界面
│   └── demo_page.py         # Streamlit前端
├── logs/                     # 日志目录
├── .env                      # 环境变量配置
├── .env.example              # 环境变量示例（模板）
├── .gitignore               # Git忽略文件
├── Dockerfile               # Docker镜像构建
├── docker-compose.yml       # Docker Compose配置
├── requirements.txt         # Python依赖
├── deployment/              # 部署脚本
│   ├── start.sh             # 启动脚本
│   ├── stop.sh              # 停止脚本
│   └── health_check.sh      # 健康检查脚本
└── README.md               # 项目说明文档
```

## 生产级优化

### 1. 日志和监控

- **日志系统**：
  - 结构化日志输出到文件
  - Docker日志驱动配置
  - 支持集成ELK Stack或云日志服务

- **监控**：
  - 健康检查端点
  - 资源使用监控
  - 可选：Prometheus集成

### 2. 性能优化

- **响应速度**：
  - 工具调用优化
  - 可选：Redis缓存

- **资源管理**：
  - Docker资源限制
  - 请求超时设置

### 3. 安全加固

- **容器安全**：
  - 非root用户运行
  - 最小化镜像
  - 网络隔离

- **API安全**：
  - CORS配置
  - 可选：API密钥认证
  - 可选：HTTPS

### 4. 高可用部署

- **容器编排**：
  - 支持Kubernetes部署
  - 多副本配置
  - 负载均衡

- **故障恢复**：
  - 自动重启策略
  - 健康检查机制

## 扩展开发

### 添加新的MCP工具

1. 在 `mcp_server/server.py` 的 `TOOLS` 列表中添加工具定义
2. 在 `call_tool` 函数中添加工具处理逻辑
3. 重启MCP服务器

### 集成真实的ERP/物流API

修改 `call_tool` 函数中的对应工具处理逻辑，替换模拟数据为真实API调用：

```python
elif tool_name == "get_product_stock":
    # 替换为真实的ERP API调用
    response = requests.get(f"https://erp-api.example.com/stock/{product_model}")
    return {"content": response.text, "isError": False}
```

## 常见问题

### Q: 大模型调用失败怎么办？

A: 系统会自动降级到模板回复。请检查：
1. `.env` 文件中的 `QWEN_API_KEY` 是否正确
2. 网络连接是否正常
3. API额度是否充足

### Q: 如何修改产品数据？

A: 编辑 `mcp_server/server.py` 中的以下数据字典：
- `PRODUCT_STOCK_DATA`：库存数据
- `PRODUCT_PRICE_DATA`：价格数据
- `PRODUCT_NAME_DATA`：产品名称数据

### Q: 端口被占用怎么办？

A:
1. 修改 `.env` 文件中的 `PORT` 配置
2. 或使用 `docker-compose.yml` 修改端口映射
3. 或终止占用端口的进程

### Q: Docker容器启动失败怎么办？

A:
1. 查看容器日志：`docker-compose logs`
2. 检查环境变量配置
3. 确保端口未被占用
4. 检查文件权限

## 技术栈

- **后端**：Python 3.11, HTTP服务器
- **前端**：Streamlit
- **大模型**：Qwen API (OpenAI兼容接口)
- **容器化**：Docker, Docker Compose
- **配置管理**：python-dotenv
- **监控**：健康检查端点

## 许可证

本项目仅供学习和演示使用。

## 联系方式

如有问题或建议，欢迎提交Issue。

---

**永远相信美好的事即将发生！** 🚗
