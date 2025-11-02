import streamlit as st
from pathlib import Path
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sentiment UI - Background Demo",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Change the URL hash name ---
st.query_params.update({"": "MCO2-Sentiment-ChatBot"})


# ----------------- OPTIONAL ICON LOADER -----------------
def load_icon_base64(path="icon.png"):
    p = Path(path)
    if p.exists():
        return base64.b64encode(p.read_bytes()).decode()
    return None

icon_b64 = load_icon_base64("icon.png")

# ----------------- CSS (force gradient + blobs + overrides) -----------------
CSS = f"""
<style>
/* --- Force base gradient everywhere (vertical) --- */
html, body, #root, .appview-container, .main, .stApp {{
  height: 100% !important;
  min-height: 100% !important;
  background: linear-gradient(180deg,
    #4E56C0 0%,
    #9B5DE0 33%,
    #D78FEE 66%,
    #FDCFFA 100%) !important;
  background-attachment: fixed !important;
  overflow: hidden !important;
}}

/* Prevent Streamlit from painting its own background on top */
[data-testid="stAppViewContainer"], .css-1outpf7, .css-1y4p8pa {{
  background: transparent !important;
}}

/* Hide Streamlit default header/menu (optional) */
header, .css-18e3th9, [data-testid="stToolbar"] {{
  visibility: hidden;
  height: 0;
  margin: 0;
  padding: 0;
}}

/* --- Blob layer (on top of gradient but below UI card) --- */
.blob-layer {{
  position: fixed;
  inset: 0;
  z-index: 0; /* behind card */
  pointer-events: none;
  overflow: hidden;
}}

.blob {{
  position: absolute;
  width: 60vmax;
  height: 60vmax;
  border-radius: 50%;
  filter: blur(120px);
  opacity: 0.55;
  mix-blend-mode: screen;
  transform: translate3d(0,0,0);
  will-change: transform;
  animation: slowfloat 36s ease-in-out infinite;
}}

/* Soft pastel color blobs using your palette (subtle) */
.blob.b1 {{ background: radial-gradient(circle at 30% 30%, #4E56C0 0%, rgba(78,86,192,0.55) 35%, rgba(78,86,192,0) 100%); left: -18%; top: -22%; animation-duration: 40s; }}
.blob.b2 {{ background: radial-gradient(circle at 70% 25%, #9B5DE0 0%, rgba(155,93,224,0.45) 35%, rgba(155,93,224,0) 100%); right: -20%; top: -8%; animation-duration: 44s; animation-delay: 2s; }}
.blob.b3 {{ background: radial-gradient(circle at 35% 70%, #D78FEE 0%, rgba(215,143,238,0.42) 35%, rgba(215,143,238,0) 100%); left: -16%; bottom: -22%; animation-duration: 42s; animation-delay: 1s; }}
.blob.b4 {{ background: radial-gradient(circle at 80% 75%, #FDCFFA 0%, rgba(253,207,250,0.45) 35%, rgba(253,207,250,0) 100%); right: -18%; bottom: -14%; animation-duration: 46s; animation-delay: 3s; }}

/* Very slow subtle floating movement */
@keyframes slowfloat {{
  0%   {{ transform: translate3d(0,0,0) scale(1); }}
  25%  {{ transform: translate3d(3vmin, -3vmin, 0) scale(1.03); }}
  50%  {{ transform: translate3d(0,5vmin,0) scale(1); }}
  75%  {{ transform: translate3d(-3vmin,-2vmin,0) scale(0.98); }}
  100% {{ transform: translate3d(0,0,0) scale(1); }}
}}

/* --- Centered UI card (above blobs) --- */
.ui-card-wrapper {{
  position: relative;
  z-index: 5; /* above blobs */
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: 100vh;
  padding: 4rem 1rem;
  box-sizing: border-box;
}}

.ui-card {{
  width: 100%;
  max-width: 920px;
  background: rgba(255,255,255,0.85); /* your chosen card opacity */
  border-radius: 28px;
  padding: 48px;
  box-shadow: 0 14px 40px rgba(14,14,24,0.12);
  text-align: center;
  margin-top: 8vh;
}}

.title {{
  font-size: 38px;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(90deg, #4E56C0,#9B5DE0,#D78FEE);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.subtitle {{
  color: #333;
  margin-bottom: 18px;
  font-size: 15px;
}}

/* small responsive tweak */
@media (max-width: 720px) {{
  .ui-card {{ padding: 28px; border-radius: 20px; }}
  .title {{ font-size: 28px; }}
  .blob {{ width: 80vmax; height: 80vmax; filter: blur(140px); }}
}}

</style>
"""

# Inject CSS early
st.markdown(CSS, unsafe_allow_html=True)

# ----------------- Blob DOM (rendered on top of gradient, behind card) -----------------
BLOBS = """
<div class="blob-layer" aria-hidden="true">
  <div class="blob b1"></div>
  <div class="blob b2"></div>
  <div class="blob b3"></div>
  <div class="blob b4"></div>
</div>
"""
st.markdown(BLOBS, unsafe_allow_html=True)

# ----------------- Footer -----------------
FOOTER = """
<style>
.footer-text {
    position: fixed;
    right: 18px;
    bottom: 12px;
    font-size: 14px;
    color: rgba(255,255,255,0.92);
    font-weight: 500;
    text-shadow: 0 2px 6px rgba(0,0,0,0.35);
    z-index: 10;
}
</style>

<div class="footer-text">
    Created by: <b>Yannah De Leon Gonzales</b>
</div>
"""

st.markdown(FOOTER, unsafe_allow_html=True)


# ----------------- Center Card Content -----------------
st.markdown(
    """
    <div class="ui-card-wrapper">
      <div class="ui-card">
        <div class="title">Greetings from Sentiment ChatBot!</div>
        <div class="subtitle">Discover what your customers feel with our AI-driven sentiment analysis.</div>
        <div style="margin-top: 24px;">
          <a href="#" id="start-btn" style="
            display: inline-block;
            padding: 14px 34px;
            background: linear-gradient(90deg, #4E56C0, #9B5DE0, #D78FEE);
            color: white;
            text-decoration: none;
            font-weight: 600;
            border-radius: 12px;
            font-size: 16px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
            transition: 0.25s;
          ">Begin</a>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
