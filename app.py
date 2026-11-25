
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import secrets
import time
import hmac
from urllib.parse import urlencode

st.set_page_config(
    page_title="SocialBoost Bot",
    page_icon="🚀",
    layout="wide"
)

# TikTok configuration
REDIRECT_URI = (
    "https://socialboost-bot-ualbzdefhgy3zmhuy9hyg7.streamlit.app/"
)

AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/"
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
USER_INFO_URL = "https://open.tiktokapis.com/v2/user/info/"

# Shared temporary OAuth state storage
@st.cache_resource
def get_state_store():
    return {}

state_store = get_state_store()

st.title("🚀 SocialBoost Bot")
st.caption("TikTok Growth & Engagement Analytics")

# Load TikTok credentials from Streamlit Secrets
config = st.secrets.get("tiktok", {})
CLIENT_KEY = config.get("client_key", "")
CLIENT_SECRET = config.get("client_secret", "")

# Handle TikTok authorization callback
params = st.query_params

if "error" in params:
    st.error(
        "TikTok authorization failed: "
        + str(params.get("error_description", params.get("error")))
    )
    st.query_params.clear()

elif "code" in params:
    code = params.get("code")
    returned_state = params.get("state", "")

    issued_time = state_store.pop(returned_state, None)

    if not issued_time or time.time() - issued_time > 600:
        st.error("Login session expired or invalid. Please try again.")
        st.query_params.clear()

    elif not CLIENT_KEY or not CLIENT_SECRET:
        st.error("TikTok credentials are not configured.")
        st.query_params.clear()

    else:
        try:
            response = requests.post(
                TOKEN_URL,
                data={
                    "client_key": CLIENT_KEY,
                    "client_secret": CLIENT_SECRET,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": REDIRECT_URI
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                timeout=30
            )

            token_data = response.json()

            if response.status_code == 200 and token_data.get("access_token"):
                st.session_state["tiktok_access_token"] = (
                    token_data["access_token"]
                )
                st.session_state["tiktok_open_id"] = (
                    token_data.get("open_id", "")
                )
                st.session_state["tiktok_scopes"] = (
                    token_data.get("scope", "")
                )

                # Retrieve basic TikTok profile information
                profile_response = requests.get(
                    USER_INFO_URL,
                    params={
                        "fields": "open_id,display_name,avatar_url"
                    },
                    headers={
                        "Authorization": (
                            "Bearer " + token_data["access_token"]
                        )
                    },
                    timeout=30
                )

                profile_data = profile_response.json()

                if profile_response.status_code == 200:
                    user = profile_data.get("data", {}).get("user", {})
                    st.session_state["tiktok_profile"] = user
                else:
                    st.session_state["tiktok_profile"] = {}

                st.session_state["tiktok_connected"] = True
                st.query_params.clear()
                st.rerun()

            else:
                st.error(
                    "TikTok token exchange failed: "
                    + str(token_data.get("error_description",
                                         token_data.get("error", "Unknown error")))
                )
                st.query_params.clear()

        except requests.RequestException as error:
            st.error("Connection error: " + str(error))
            st.query_params.clear()

# TikTok account connection section
st.subheader("Connect your TikTok account")

if st.session_state.get("tiktok_connected"):
    profile = st.session_state.get("tiktok_profile", {})

    st.success("TikTok account connected successfully!")

    if profile.get("avatar_url"):
        st.image(profile["avatar_url"], width=100)

    st.write(
        "**Display name:**",
        profile.get("display_name", "Profile information unavailable")
    )

    st.write(
        "**TikTok Open ID:**",
        st.session_state.get("tiktok_open_id", "Unavailable")
    )

    st.caption(
        "Authorized scopes: "
        + st.session_state.get("tiktok_scopes", "")
    )

    if st.button("Disconnect TikTok"):
        for key in [
            "tiktok_access_token",
            "tiktok_open_id",
            "tiktok_scopes",
            "tiktok_profile",
            "tiktok_connected"
        ]:
            st.session_state.pop(key, None)

        st.rerun()

elif CLIENT_KEY and CLIENT_SECRET:

    if "oauth_state" not in st.session_state:
        st.session_state["oauth_state"] = None

    if st.button("Continue with TikTok", type="primary"):
        state = secrets.token_urlsafe(32)

        state_store[state] = time.time()
        st.session_state["oauth_state"] = state

        authorization_params = {
            "client_key": CLIENT_KEY,
            "response_type": "code",
            "scope": "user.info.basic",
            "redirect_uri": REDIRECT_URI,
            "state": state
        }

        authorization_url = (
            AUTH_URL + "?" + urlencode(authorization_params)
        )

        st.link_button(
            "Open TikTok authorization",
            authorization_url
        )

else:
    st.warning(
        "TikTok credentials are missing. "
        "Configure your Client Key and Client Secret first."
    )

st.divider()

# Dashboard
st.subheader("Dashboard")

st.caption(
    "The following figures are demonstration data, "
    "not live TikTok analytics."
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Followers", "12,450", "+8.2%")
col2.metric("Total Likes", "85,200", "+12.5%")
col3.metric("Video Views", "240,500", "+18.4%")
col4.metric("Engagement", "7.8%", "+2.1%")

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
