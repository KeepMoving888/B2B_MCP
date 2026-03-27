# MCP服务启动文件 - 生产级HTTP版本
import http.server
import socketserver
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_server.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mcp_server")

# 工具定义
TOOLS = [
    {
        "name": "get_product_stock",
        "description": "查询CarPlay适配器产品实时库存，必填参数：product_model（产品型号）",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_model": {
                    "type": "string",
                    "description": "CarPlay适配器产品型号，例如：CPA-W1、CPA-U2"
                }
            },
            "required": ["product_model"]
        }
    },
    {
        "name": "calculate_quote",
        "description": "计算CarPlay适配器FOB报价，必填参数：product_model、quantity、destination_port",
        "inputSchema": {
            "type": "object",
            "properties": {
                "product_model": {"type": "string", "description": "CarPlay适配器产品型号"},
                "quantity": {"type": "integer", "description": "采购数量"},
                "destination_port": {"type": "string", "description": "目的港口，例如：LOS ANGELES"}
            },
            "required": ["product_model", "quantity", "destination_port"]
        }
    },
    {
        "name": "get_logistics_info",
        "description": "查询CarPlay适配器物流时效与运费，必填参数：destination_port、weight、quantity",
        "inputSchema": {
            "type": "object",
            "properties": {
                "destination_port": {"type": "string", "description": "目的港口"},
                "weight": {"type": "number", "description": "单产品重量(kg)"},
                "quantity": {"type": "integer", "description": "采购数量"}
            },
            "required": ["destination_port", "weight", "quantity"]
        }
    },
    {
        "name": "translate_text",
        "description": "CarPlay适配器业务多语言翻译，必填参数：text、target_language",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "待翻译文本"},
                "target_language": {"type": "string", "description": "目标语言，例如：en、es、fr"}
            },
            "required": ["text", "target_language"]
        }
    }
]

# 产品数据
PRODUCT_STOCK_DATA = {
    "CPA-W1": {"stock": 8500, "warehouse": "深圳龙华仓", "lead_time": "2天", "compatibility": "支持有线/无线CarPlay"},
    "CPA-U2": {"stock": 6200, "warehouse": "东莞虎门仓", "lead_time": "3天", "compatibility": "仅支持有线CarPlay"},
    "CPA-PRO": {"stock": 1200, "warehouse": "广州白云仓", "lead_time": "5天", "compatibility": "支持无线CarPlay+Android Auto"}
}

PRODUCT_PRICE_DATA = {
    "CPA-W1": 28.5,
    "CPA-U2": 19.8,
    "CPA-PRO": 45.2
}

PRODUCT_NAME_DATA = {
    "CPA-W1": "无线CarPlay适配器",
    "CPA-U2": "有线CarPlay适配器",
    "CPA-PRO": "CarPlay+Android Auto双系统适配器"
}

def call_tool(tool_name, args):
    """
    调用MCP工具处理业务逻辑
    
    Args:
        tool_name: 工具名称
        args: 工具参数
    
    Returns:
        dict: 包含content和isError的字典
    """
    logger.info(f"调用工具: {tool_name}, 参数: {args}")
    
    try:
        if tool_name == "get_product_stock":
            product_model = args.get("product_model")
            if not product_model:
                error_msg = "缺少必填参数：product_model"
                logger.error(error_msg)
                return {"content": error_msg, "isError": True}
            
            result = PRODUCT_STOCK_DATA.get(
                product_model, 
                {"error": "CarPlay适配器型号不存在，请确认型号是否正确：CPA-W1/CPA-U2/CPA-PRO"}
            )
            logger.info(f"库存查询结果: {result}")
            return {"content": str(result), "isError": False}

        elif tool_name == "calculate_quote":
            product_model = args.get("product_model")
            quantity = args.get("quantity")
            destination_port = args.get("destination_port")
            
            if not all([product_model, quantity, destination_port]):
                error_msg = "缺少必填参数，需要：product_model、quantity、destination_port"
                logger.error(error_msg)
                return {"content": error_msg, "isError": True}
            
            unit_price = PRODUCT_PRICE_DATA.get(product_model, 0)
            total_price = unit_price * quantity
            
            result = {
                "product_model": product_model,
                "product_name": PRODUCT_NAME_DATA.get(product_model, "CarPlay适配器"),
                "quantity": quantity,
                "unit_price": f"${unit_price}",
                "total_fob_price": f"${total_price}",
                "moq": "500台",
                "payment_term": "T/T 30%预付，70%见提单副本",
                "warranty": "12个月质保"
            }
            logger.info(f"报价计算结果: {result}")
            return {"content": str(result), "isError": False}

        elif tool_name == "get_logistics_info":
            destination_port = args.get("destination_port")
            weight = args.get("weight")
            quantity = args.get("quantity")
            
            if not all([destination_port, weight, quantity]):
                error_msg = "缺少必填参数，需要：destination_port、weight、quantity"
                logger.error(error_msg)
                return {"content": error_msg, "isError": True}
            
            total_weight = weight * quantity
            freight = total_weight * 3.5
            
            result = {
                "destination_port": destination_port,
                "total_weight": f"{total_weight}kg",
                "package_info": "每箱20台，纸箱包装",
                "sea_freight": f"${freight}",
                "air_freight": f"${freight * 6.5}",
                "shipping_time_sea": "22-28天",
                "shipping_time_air": "5-7天",
                "shipping_company": "马士基/中远海运"
            }
            logger.info(f"物流查询结果: {result}")
            return {"content": str(result), "isError": False}

        elif tool_name == "translate_text":
            text = args.get("text")
            target_lang = args.get("target_language")
            
            if not all([text, target_lang]):
                error_msg = "缺少必填参数，需要：text、target_language"
                logger.error(error_msg)
                return {"content": error_msg, "isError": True}
            
            # 模拟翻译，上线替换为阿里翻译API
            translate_result = f"【{target_lang}翻译结果】{text}"
            logger.info(f"翻译结果: {translate_result}")
            return {"content": translate_result, "isError": False}

        else:
            error_msg = f"未知工具：{tool_name}"
            logger.error(error_msg)
            return {"content": error_msg, "isError": True}
            
    except Exception as e:
        error_msg = f"工具调用异常: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {"content": error_msg, "isError": True}

class RequestHandler(http.server.BaseHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def log_message(self, format, *args):
        """重写日志方法，使用自定义日志记录器"""
        logger.info(f"{self.address_string()} - {format % args}")
    
    def do_POST(self):
        """处理POST请求"""
        start_time = datetime.now()
        logger.info(f"收到POST请求: {self.path}")
        
        try:
            # 读取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
            else:
                post_data = b'{}'
            
            # 解析JSON
            try:
                data = json.loads(post_data.decode('utf-8'))
            except json.JSONDecodeError as e:
                error_response = {"error": "Invalid JSON", "details": str(e)}
                self.send_error_response(400, error_response)
                return
            
            # 路由处理
            if self.path == '/process_inquiry':
                result = {"status": "processed", "data": data, "timestamp": datetime.now().isoformat()}
            elif self.path == '/validate_inquiry':
                result = {"valid": True, "message": "验证通过", "timestamp": datetime.now().isoformat()}
            elif self.path == '/list_tools':
                result = {"tools": TOOLS, "timestamp": datetime.now().isoformat()}
            elif self.path == '/call_tool':
                tool_name = data.get('name')
                args = data.get('arguments', {})
                result = call_tool(tool_name, args)
                result['timestamp'] = datetime.now().isoformat()
            else:
                self.send_error_response(404, {"error": "Not Found"})
                return
            
            # 发送成功响应
            self.send_success_response(result)
            
        except Exception as e:
            logger.error(f"处理请求时异常: {str(e)}", exc_info=True)
            self.send_error_response(500, {"error": "Internal Server Error", "message": str(e)})
        
        finally:
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(f"请求处理完成，耗时: {duration:.3f}秒")
    
    def do_GET(self):
        """处理GET请求"""
        if self.path == '/health':
            self.send_success_response({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "service": "CarPlay Adapter MCP Server"
            })
        elif self.path == '/metrics':
            # 简单的指标端点
            self.send_success_response({
                "uptime": "running",
                "tools_available": len(TOOLS)
            })
        else:
            self.send_error_response(404, {"error": "Not Found"})
    
    def send_success_response(self, data):
        """发送成功响应"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def send_error_response(self, status_code, data):
        """发送错误响应"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def main():
    """启动MCP服务器主函数"""
    PORT = int(os.getenv("PORT", 8000))
    HOST = os.getenv("HOST", "")
    
    logger.info("=" * 50)
    logger.info("CarPlay适配器MCP服务器启动中...")
    logger.info(f"监听地址: {HOST if HOST else '0.0.0.0'}:{PORT}")
    logger.info("=" * 50)
    
    try:
        # 创建TCPServer实例并设置地址重用
        httpd = socketserver.TCPServer((HOST, PORT), RequestHandler)
        httpd.allow_reuse_address = True
        httpd.allow_reuse_port = True
        
        logger.info(f"服务器启动成功！按 Ctrl+C 停止服务器")
        logger.info(f"健康检查: http://localhost:{PORT}/health")
        logger.info(f"工具列表: http://localhost:{PORT}/list_tools")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("\n收到停止信号，正在关闭服务器...")
        httpd.shutdown()
        httpd.server_close()
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
