import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# 配置页面 - CarPlay行业优化图标
st.set_page_config(
    page_title="CarPlay适配器B2B询盘助手", 
    page_icon="🚗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题区域
st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #1e88e5; margin-bottom: 10px;">🚗 CarPlay适配器B2B智能询盘助手</h1>
        <p style="color: #666; font-size: 1.1em;">专业的CarPlay适配器跨境B2B外贸询盘解决方案</p>
    </div>
    <hr style="border: 1px solid #e3f2fd;">
""", unsafe_allow_html=True)

# 大模型和MCP服务器配置
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

# 初始化大模型客户端
client = None
if QWEN_API_KEY:
    try:
        client = OpenAI(
            api_key=QWEN_API_KEY,
            base_url=QWEN_BASE_URL
        )
    except Exception as e:
        st.warning(f"大模型客户端初始化失败：{str(e)}")

# 系统Prompt
SYSTEM_PROMPT = """
你是专业的CarPlay适配器跨境B2B外贸询盘助手，必须严格遵守以下规则：
1. 所有涉及产品库存、报价、物流的业务数据，必须通过调用MCP工具查询，绝对不允许自己编造；
2. 严格按照工具的参数要求调用，参数不全时，先询问用户补充，再调用工具；
3. 回复必须专业、简洁，符合外贸邮件的规范，支持多语言回复；
4. 如果查询不到对应数据，直接告知用户，绝对不允许编造内容。

你可以调用的MCP工具：
1. get_product_stock：查询CarPlay适配器产品实时库存
2. calculate_quote：计算CarPlay适配器FOB报价
3. get_logistics_info：查询CarPlay适配器物流时效与运费
4. translate_text：CarPlay适配器业务多语言翻译

产品型号说明：
- CPA-W1：无线CarPlay适配器，支持有线/无线切换
- CPA-U2：有线CarPlay适配器，即插即用
- CPA-PRO：CarPlay+Android Auto双系统适配器
"""

def show_template_reply(stock_data, quote_data, logistics_data, target_lang):
    """显示模板化回复"""
    if target_lang == "中文":
        reply = """尊敬的客户，

感谢您对我们CarPlay适配器的询盘。

根据我们的查询：
"""
        if stock_data:
            reply += f"1. 库存情况：{stock_data.get('content', '')}\n"
        if quote_data:
            reply += f"2. FOB报价：{quote_data.get('content', '')}\n"
        if logistics_data:
            reply += f"3. 物流信息：{logistics_data.get('content', '')}\n"
        
        reply += """
如果您有任何其他问题，请随时告知我们。

此致，
您的CarPlay适配器外贸团队
        """
    else:
        reply = """Dear Customer,

Thank you for your inquiry about our CarPlay adapters.

According to our check:
"""
        if stock_data:
            reply += f"1. Stock Status: {stock_data.get('content', '')}\n"
        if quote_data:
            reply += f"2. FOB Quotation: {quote_data.get('content', '')}\n"
        if logistics_data:
            reply += f"3. Logistics Info: {logistics_data.get('content', '')}\n"
        
        reply += """
Please feel free to contact us if you have any other questions.

Best regards,
Your CarPlay Adapter Team
        """
    
    st.divider()
    st.subheader("✅ 询盘回复结果")
    st.markdown(reply)
    
    # 显示工具调用详情
    with st.expander("📊 MCP工具调用详情"):
        if stock_data:
            st.write("**库存查询：", stock_data)
        if quote_data:
            st.write("**报价查询：", quote_data)
        if logistics_data:
            st.write("**物流查询：", logistics_data)

def process_inquiry(inquiry_text, target_lang):
    """处理询盘的核心函数"""
    stock_data = None
    quote_data = None
    logistics_data = None
    
    try:
        # 查询库存
        try:
            stock_response = requests.post(f"{MCP_SERVER_URL}/call_tool", json={
                "name": "get_product_stock",
                "arguments": {"product_model": "CPA-W1"}
            }, timeout=10)
            if stock_response.status_code == 200:
                stock_data = stock_response.json()
        except Exception as e:
            st.warning(f"库存查询失败：{str(e)}")
        
        # 查询报价
        try:
            quote_response = requests.post(f"{MCP_SERVER_URL}/call_tool", json={
                "name": "calculate_quote",
                "arguments": {
                    "product_model": "CPA-W1",
                    "quantity": 2000,
                    "destination_port": "LOS ANGELES"
                }
            }, timeout=10)
            if quote_response.status_code == 200:
                quote_data = quote_response.json()
        except Exception as e:
            st.warning(f"报价查询失败：{str(e)}")
        
        # 查询物流
        try:
            logistics_response = requests.post(f"{MCP_SERVER_URL}/call_tool", json={
                "name": "get_logistics_info",
                "arguments": {
                    "destination_port": "LOS ANGELES",
                    "weight": 0.3,
                    "quantity": 2000
                }
            }, timeout=10)
            if logistics_response.status_code == 200:
                logistics_data = logistics_response.json()
        except Exception as e:
            st.warning(f"物流查询失败：{str(e)}")
        
        # 构建工具调用结果上下文
        tool_context = ""
        if stock_data:
            tool_context += f"\n库存查询结果：{stock_data.get('content', '')}"
        if quote_data:
            tool_context += f"\n报价查询结果：{quote_data.get('content', '')}"
        if logistics_data:
            tool_context += f"\n物流查询结果：{logistics_data.get('content', '')}"
        
        # 使用大模型生成回复
        if client:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"客户询盘内容：{inquiry_text}\n\n已通过MCP工具查询到的业务数据：{tool_context}\n\n请用{target_lang}生成专业的外贸回复"}
            ]
            
            try:
                response = client.chat.completions.create(
                    model="qwen-turbo",
                    messages=messages,
                    temperature=0.3,
                    stream=False
                )
                reply = response.choices[0].message.content
                
                st.divider()
                st.subheader("✅ 询盘回复结果")
                st.markdown(reply)
                
                # 显示工具调用详情
                with st.expander("📊 MCP工具调用详情"):
                    if stock_data:
                        st.write("**库存查询：", stock_data)
                    if quote_data:
                        st.write("**报价查询：", quote_data)
                    if logistics_data:
                        st.write("**物流查询：", logistics_data)
                        
            except Exception as llm_error:
                st.warning(f"大模型调用失败，使用模板回复：{str(llm_error)}")
                # 大模型失败时使用模板回复
                show_template_reply(stock_data, quote_data, logistics_data, target_lang)
        else:
            # 没有配置大模型API时使用模板回复
            show_template_reply(stock_data, quote_data, logistics_data, target_lang)
            
    except Exception as e:
        st.error(f"处理询盘时出错：{str(e)}")
        st.divider()
        st.subheader("✅ 询盘回复结果（模拟）")
        st.markdown("尊敬的客户，\n\n感谢您对我们CarPlay适配器的询盘。\n\n我们已收到您的请求，正在核实相关信息后会尽快给您详细回复。\n\n此致，\n您的CarPlay适配器外贸团队")

# 页面布局 - 优化的CarPlay行业界面
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">📱 产品信息</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    - **CPA-W1** 🔌
      - 单价：$28.5，单重：0.3kg
      - 支持有线/无线双模式
      - 兼容性：iOS 10+
    - **CPA-U2** 🎵
      - 单价：$19.8，单重：0.2kg
      - 即插即用，稳定可靠
    - **CPA-PRO** 🚀
      - 单价：$45.2，单重：0.35kg
      - 支持CarPlay+Android Auto
    """)
    
    st.divider()
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3 style="color: white; margin: 0;">📝 演示示例</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **询盘示例1（中文）：**
    我想采购CPA-W1型号的无线CarPlay适配器2000台，目的港洛杉矶，
    请问库存有多少，FOB报价是多少，海运运费和时效是多少？

    **询盘示例2（英文）：**
    I'm interested in purchasing 1000 units of CPA-PRO model CarPlay adapters.
    Can you provide stock info, FOB price for New York port and shipping details?

    **询盘示例3（西班牙语）：**
    Quiero comprar 500 unidades del modelo CPA-U2,
    ¿puedes decirme el stock y el precio FOB para el puerto de Barcelona?
    """)

with col1:
    # 输入区域美化
    st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h4 style="color: #333; margin-top: 0;">💬 请输入客户询盘内容</h4>
        </div>
    """, unsafe_allow_html=True)
    
    # 使用st.text_input，它默认就是Enter键直接提交！
    with st.form("inquiry_form"):
        inquiry_text = st.text_input(
            "（支持多语言，按Enter直接提交）", 
            placeholder="例如：我想采购CPA-W1型号的无线CarPlay适配器2000台，目的港洛杉矶，请问库存有多少，FOB报价是多少？"
        )
        
        target_lang = st.selectbox(
            "🌍 回复目标语言", 
            ["中文", "English", "Spanish", "French"], 
            index=1
        )
        
        # 提交按钮
        submit_btn = st.form_submit_button(
            "🚀 生成询盘回复", 
            type="primary", 
            use_container_width=True
        )
    
    # 检查是否提交
    if submit_btn:
        if inquiry_text and len(inquiry_text.strip()) > 0:
            with st.spinner("🚗 正在通过MCP工具查询业务数据，生成回复..."):
                process_inquiry(inquiry_text, target_lang)
        else:
            st.warning("请输入询盘内容！")

# 添加提示信息
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 20px;">
        💡 提示：在输入框中输入内容后，按 <strong>Enter</strong> 键或点击按钮即可提交
    </div>
""", unsafe_allow_html=True)
