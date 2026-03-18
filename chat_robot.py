import streamlit as st
from openai import OpenAI

# 初始化客户端
client = OpenAI(base_url="http://localhost:23333/v1/", api_key="suibianxie")

# 设置页面标题
st.title("项目一效果演示")

# 初始化session状态（仅用于显示历史）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 获取用户输入
if prompt := st.chat_input("请输入您的问题，或输入exit退出"):
    # 处理退出命令
    if prompt.lower() == "exit":
        st.info("退出对话。")
        st.stop()
    
    # 添加用户消息到显示历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # 发起API请求（每次只发送当前消息）
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],  # 每次只发送当前问题
            model="/home/cw/llms/Qwen/Qwen1.5-1.8B-Chat-merged"
        )
        
        # 获取模型回复
        model_response = response.choices[0].message.content
        
        # 添加AI回复到显示历史
        st.session_state.messages.append({"role": "assistant", "content": model_response})
        with st.chat_message("assistant"):
            st.markdown(model_response)

    except Exception as e:
        st.error(f"发生错误：{e}")