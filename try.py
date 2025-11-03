import streamlit as st
from pathlib import Path
import base64
from textblob import TextBlob
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sentiment UI - Background Demo",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------- OPTIONAL ICON LOADER -----------------
def load_icon_base64(path="icon.png"):
    p = Path(path)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

icon_b64 = load_icon_base64("icon.png")

# ----------------- CSS -----------------
CSS = """
<style>
html, body, #root, .appview-container, .main, .stApp {
  height: 100% !important;
  background: linear-gradient(180deg,
    #4E56C0 0%,
    #9B5DE0 33%,
    #D78FEE 66%,
    #FDCFFA 100%) !important;
  background-attachment: fixed !important;
  overflow: hidden !important;
}
[data-testid="stAppViewContainer"] { background: transparent !important; }
header, [data-testid="stToolbar"] { visibility: hidden; height: 0; }

.blob-layer {
  position: fixed; inset: 0; z-index: 0;
  pointer-events: none; overflow: hidden;
}
.blob {
  position: absolute;
  width: 60vmax; height: 60vmax;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.55;
  mix-blend-mode: screen;
  animation: slowfloat 36s ease-in-out infinite;
}
.blob.b1 { background: radial-gradient(circle at 30% 30%, #4E56C0 0%, rgba(78,86,192,0.55) 35%, rgba(78,86,192,0) 100%); left:-18%; top:-22%; }
.blob.b2 { background: radial-gradient(circle at 70% 25%, #9B5DE0 0%, rgba(155,93,224,0.45) 35%, rgba(155,93,224,0) 100%); right:-20%; top:-8%; }
.blob.b3 { background: radial-gradient(circle at 35% 70%, #D78FEE 0%, rgba(215,143,238,0.42) 35%, rgba(215,143,238,0) 100%); left:-16%; bottom:-22%; }
.blob.b4 { background: radial-gradient(circle at 80% 75%, #FDCFFA 0%, rgba(253,207,250,0.45) 35%, rgba(253,207,250,0) 100%); right:-18%; bottom:-14%; }

@keyframes slowfloat {
  0% { transform: translate3d(0,0,0) scale(1); }
  25% { transform: translate3d(3vmin,-3vmin,0) scale(1.03); }
  50% { transform: translate3d(0,5vmin,0) scale(1); }
  75% { transform: translate3d(-3vmin,-2vmin,0) scale(0.98); }
  100% { transform: translate3d(0,0,0) scale(1); }
}

.ui-card-wrapper {
  position: relative; z-index: 5;
  display: flex; justify-content: center; align-items: start;
  min-height: 100vh; padding: 4rem 1rem; box-sizing: border-box;
}

.ui-card {
  width: 100%; max-width: 920px;
  background: rgba(255,255,255,0.9);
  border-radius: 28px;
  padding: 48px;
  box-shadow: 0 14px 40px rgba(14,14,24,0.12);
  text-align: center;
  margin-top: 8vh;
  opacity: 0; transform: scale(0.98);
  animation: fadeIn 0.5s forwards;
}

.fade-out { animation: fadeOut 0.5s forwards !important; }

@keyframes fadeIn { to { opacity: 1; transform: scale(1); } }
@keyframes fadeOut { to { opacity: 0; transform: scale(0.98); } }

.title {
  font-size: 38px; font-weight: 700; margin-bottom: 8px;
  background: linear-gradient(90deg, #4E56C0,#9B5DE0,#D78FEE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.subtitle { color: #333; margin-bottom: 18px; font-size: 15px; }

.chat-box {
  background: rgba(255,255,255,0.6);
  border-radius: 16px;
  padding: 20px;
  text-align: left;
  height: 280px;
  overflow-y: auto;
  margin: 25px 0 10px 0;
}

.chat-message {
  margin-bottom: 10px;
  line-height: 1.5;
}

.chat-user { color: #4E56C0; font-weight: 600; }
.chat-bot { color: #333; font-weight: 500; }

input[type="text"] {
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid #ccc;
  font-size: 15px;
  margin-top: 5px;
}

button[kind="secondary"] {
  margin-top: 10px;
  background: linear-gradient(90deg, #4E56C0, #9B5DE0, #D78FEE);
  color: white !important;
  font-weight: 600;
  border-radius: 12px !important;
  border: none !important;
  padding: 10px 20px !important;
}

@media (max-width: 720px) {
  .ui-card { padding: 28px; border-radius: 20px; }
  .title { font-size: 28px; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ----------------- Background & Footer -----------------
st.markdown("""
<div class="blob-layer" aria-hidden="true">
  <div class="blob b1"></div><div class="blob b2"></div>
  <div class="blob b3"></div><div class="blob b4"></div>
</div>
""", unsafe_allow_html=True)

# ----------------- State -----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "fade" not in st.session_state:
    st.session_state.fade = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------- HOME PAGE -----------------
if st.session_state.page == "home":
    fade_class = "fade-out" if st.session_state.fade else ""
    st.markdown(f"""
    <div class="ui-card-wrapper">
      <div class="ui-card {fade_class}">
        <div class="title">Greetings from Sentiment ChatBot!</div>
        <div class="subtitle">Discover what your customers feel with our AI-driven sentiment analysis.</div>
        <div style="margin-top: 24px;">
          <button id="begin-btn" style="
              display: inline-block;
              padding: 14px 34px;
              background: linear-gradient(90deg, #4E56C0, #9B5DE0, #D78FEE);
              color: white;
              text-decoration: none;
              font-weight: 600;
              border-radius: 12px;
              font-size: 16px;
              box-shadow: 0 6px 20px rgba(0,0,0,0.15);
              border: none;
              cursor: pointer;
              transition: 0.25s;
          ">Begin</button>
        </div>
      </div>
    </div>
    <script>
    const btn = window.parent.document.querySelector("#begin-btn");
    if (btn) {{
        btn.addEventListener("click", () => {{
            window.parent.postMessage({{"type": "beginClicked"}}, "*");
        }});
    }}
    </script>
    """, unsafe_allow_html=True)

# Transition logic
clicked = st.session_state.get("clicked", False)
if not clicked:
    st.session_state.clicked = True
    st.session_state.fade = True
    time.sleep(0.4)
    st.session_state.page = "chat"
    st.rerun()

# ----------------- CHAT PAGE (CARD RESTORED + SAME FONT) -----------------
elif st.session_state.page == "chat":
    html_code = """
    <div class="ui-card-wrapper" style="display:flex;justify-content:center;align-items:center;height:100%;font-family:'Source Sans Pro',sans-serif;">
      <div class="ui-card" style="
          width:580px;
          background:rgba(255,255,255,0.9);
          border-radius:20px;
          box-shadow:0 8px 30px rgba(0,0,0,0.15);
          padding:36px 32px;
          display:flex;
          flex-direction:column;
          justify-content:space-between;
          height:520px;
      ">
        <div>
          <div class="title" style="font-size:28px;font-weight:700;margin-bottom:6px;">💬 Sentiment ChatBot</div>
          <div class="subtitle" style="font-size:16px;color:#555;">Type a message or review below to analyze its sentiment.</div>

          <!-- CHAT AREA INSIDE CARD -->
          <div class="chat-box" style="
              flex-grow:1;
              overflow-y:auto;
              background:rgba(255,255,255,0.7);
              border-radius:14px;
              padding:16px;
              margin-top:20px;
              height:260px;
              text-align:left;
              font-size:15px;
          ">
            <p style="color:gray;">No messages yet. Start's your review!</p>
          </div>

          <!-- INPUT AREA INSIDE CARD -->
          <div style="margin-top:18px; display:flex; gap:10px; align-items:center;">
            <input type="text" placeholder="Enter your message here..." style="
                flex-grow:1;
                padding:10px;
                border-radius:10px;
                border:1px solid #ccc;
                font-size:15px;
                font-family:'Source Sans Pro',sans-serif;
            ">
            <button style="
                background:linear-gradient(90deg,#4E56C0,#9B5DE0,#D78FEE);
                border:none;
                color:white;
                font-weight:600;
                border-radius:10px;
                padding:10px 18px;
                cursor:pointer;
                font-family:'Source Sans Pro',sans-serif;
            ">Send</button>
          </div>

          <!-- BACK BUTTON -->
          <div style="margin-top:24px; text-align:center;">
            <button id="back-btn" style="
                padding:10px 24px;
                background:linear-gradient(90deg,#4E56C0,#9B5DE0,#D78FEE);
                color:white;
                font-weight:600;
                border-radius:12px;
                font-size:16px;
                border:none;
                cursor:pointer;
                font-family:'Source Sans Pro',sans-serif;
            ">← Back</button>
          </div>
        </div>
      </div>
    </div>

    <script>
    const backBtn = window.parent.document.querySelector("#back-btn");
    if (backBtn) {
        backBtn.addEventListener("click", () => {
            window.parent.postMessage({"type": "backClicked"}, "*");
        });
    }
    </script>
    """

    st.components.v1.html(html_code, height=700)


