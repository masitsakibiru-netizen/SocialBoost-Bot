
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SocialBoost Bot",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 SocialBoost Bot")
st.caption("TikTok Growth & Engagement Analytics")

# Demo metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("Followers", "12,450", "+8.2%")
col2.metric("Total Likes", "85,200", "+12.5%")
col3.metric("Video Views", "240,500", "+18.4%")
col4.metric("Engagement", "7.8%", "+2.1%")

# Demo performance data
data = pd.DataFrame({
    "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "Views": [1200, 1800, 1500, 2400, 3200, 4100, 5000],
    "Likes": [100, 150, 130, 220, 300, 400, 510]
})

st.subheader("Weekly Performance")

fig = px.line(
    data,
    x="Day",
    y=["Views", "Likes"],
    markers=True,
    title="Views and Likes"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Growth Recommendations")

st.info("Post consistently and compare video performance.")
st.info("Identify videos with the highest engagement rates.")
st.info("Test different hashtags and posting times.")

st.success("SocialBoost dashboard is running!")
