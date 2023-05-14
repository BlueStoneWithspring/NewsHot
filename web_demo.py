
from main import newsGenerator
import streamlit as st


st.set_page_config(
     page_title=":",
     page_icon=":robot_face:",
     layout="wide",
     initial_sidebar_state="expanded",
 )

st.title('大家好，欢迎收看《今日乐闻》！')


if st.button("查看", key="predict"):
    with st.spinner("正在生成，请稍等........"):
        # text generation   # 历史状态st.session_state["state"]
        st.write(newsGenerator())

