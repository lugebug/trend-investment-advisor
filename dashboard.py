import json
import streamlit as st

DATA_FILE = "trend_recommendations.json"

st.set_page_config(page_title="趋势驱动投资推荐", layout="wide")
st.title("趋势驱动投资推荐 Dashboard")

try:
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    st.error("数据文件不存在，请先运行数据管道。")
    st.stop()

for cluster in data:
    st.subheader(" / ".join(cluster.get("keywords", [])))
    col1, col2, col3 = st.columns(3)
    col1.metric("趋势评分", f"{cluster.get('trend_score', 0):.1f}")
    bp = "是" if cluster.get("breakpoint_detected") else "否"
    col2.metric("是否拐点", bp)
    rec = ", ".join(cluster.get("recommendation", [])) or "暂无"
    col3.metric("投资标的", rec)
    st.markdown("---")
