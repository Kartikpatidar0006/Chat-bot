import sys
sys.stdout.reconfigure(encoding='utf-8')

import streamlit as st
from AgentTool import Agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kartik's AI",
    page_icon="✦",
    layout="centered",
)

# ── Premium CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Syne:wght@700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Background ── */
.stApp {
    background: #080812;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(120, 60, 255, 0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(30, 120, 255, 0.12) 0%, transparent 60%);
    min-height: 100vh;
}

/* ── Sticky Header wrapper ── */
[data-testid="stAppViewContainer"] > section:first-child {
    position: sticky !important;
    top: 0 !important;
    z-index: 999 !important;
    background: #080812 !important;
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.04);
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 2rem 1rem 1rem;
    position: relative;
}
.app-header-logo {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5, #0ea5e9);
    font-size: 1.6rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 32px rgba(124, 58, 237, 0.4);
    animation: float 4s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-6px); }
}
.app-header h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 50%, #a5f3fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
}
.app-header-sub {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: #4b5563;
    font-size: 0.82rem;
    font-weight: 400;
    letter-spacing: 0.3px;
}
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.2);
    color: #4ade80;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 500;
}
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(34,197,94,0.5); }
    50%       { opacity: 0.7; box-shadow: 0 0 0 4px rgba(34,197,94,0); }
}
.sep { color: #1f2937; }

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent) !important;
    margin: 0.5rem 0 1rem !important;
}

/* ── Avatar icons ── */
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #6d28d9, #4f46e5) !important;
    border: none !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, #1e3a5f, #0f2744) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
}

/* ── User bubble ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) .stMarkdown {
    background: linear-gradient(135deg, #5b21b6 0%, #4338ca 100%) !important;
    border-radius: 20px 20px 4px 20px !important;
    padding: 0.8rem 1.2rem !important;
    color: #f0f0ff !important;
    max-width: 78%;
    margin-left: auto;
    box-shadow: 0 4px 24px rgba(91, 33, 182, 0.35);
}

/* ── AI bubble ── */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) .stMarkdown {
    background: rgba(15, 23, 42, 0.7) !important;
    border: 1px solid rgba(99, 179, 237, 0.1) !important;
    border-radius: 4px 20px 20px 20px !important;
    padding: 1rem 1.3rem !important;
    color: #cbd5e1 !important;
    max-width: 88%;
    backdrop-filter: blur(16px);
    box-shadow: 0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03);
}

/* ── Code blocks ── */
[data-testid="stChatMessage"] code {
    background: rgba(124,58,237,0.15) !important;
    border: 1px solid rgba(124,58,237,0.2) !important;
    border-radius: 5px;
    padding: 2px 6px;
    color: #c4b5fd !important;
    font-size: 0.88em !important;
}
[data-testid="stChatMessage"] pre {
    background: rgba(0,0,0,0.5) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 10px !important;
    padding: 1rem !important;
}

/* ── Tool badge — only for web search ── */
.tool-badge-search {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(56, 189, 248, 0.08);
    border: 1px solid rgba(56, 189, 248, 0.2);
    color: #7dd3fc;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    margin-bottom: 0.6rem;
    letter-spacing: 0.3px;
}
.tool-badge-calc {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(52, 211, 153, 0.08);
    border: 1px solid rgba(52, 211, 153, 0.2);
    color: #6ee7b7;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.72rem;
    font-weight: 500;
    margin-bottom: 0.6rem;
}

/* ── Input box ── */
[data-testid="stChatInput"] > div {
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(99, 179, 237, 0.15) !important;
    border-radius: 18px !important;
    backdrop-filter: blur(16px);
    box-shadow: 0 0 40px rgba(99, 102, 241, 0.08), inset 0 1px 0 rgba(255,255,255,0.04);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: rgba(139, 92, 246, 0.4) !important;
    box-shadow: 0 0 40px rgba(139, 92, 246, 0.12), inset 0 1px 0 rgba(255,255,255,0.05) !important;
}
[data-testid="stChatInput"] textarea {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #374151 !important;
}

/* ── Clear button ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #4b5563 !important;
    border-radius: 10px !important;
    font-size: 0.78rem !important;
    font-weight: 400 !important;
    padding: 0.3rem 0.9rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    border-color: rgba(239, 68, 68, 0.3) !important;
    color: #f87171 !important;
    background: rgba(239, 68, 68, 0.06) !important;
}

/* ── Spinner text ── */
[data-testid="stSpinner"] p {
    color: #4b5563 !important;
    font-size: 0.82rem !important;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-header-logo">✦</div>
    <h1>Kartik's AI</h1>
    <div class="app-header-sub">
        <span class="status-pill"><span class="status-dot"></span>Online</span>
        <span class="sep">·</span>
        <span>Powered by Mistral</span>
        <span class="sep">·</span>
        <span>Web Search &amp; Research</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Agent (singleton) ──────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

# ── Session messages ───────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "tool_used" not in st.session_state:
    st.session_state.tool_used = []

# ── Clear button ───────────────────────────────────────────────────────────────
_, col_btn = st.columns([6, 1])
with col_btn:
    if st.button("Clear"):
        st.session_state.messages = []
        st.session_state.tool_used = []
        import os, json
        mem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory.json")
        with open(mem_path, "w", encoding="utf-8") as f:
            json.dump([], f)
        st.rerun()

st.divider()

# ── Render chat history ────────────────────────────────────────────────────────
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            turn = i // 2
            if turn < len(st.session_state.tool_used):
                badge = st.session_state.tool_used[turn]
                if badge == "web_search":
                    st.markdown('<span class="tool-badge-search">🌐 Web Search</span>', unsafe_allow_html=True)
                elif badge == "calculator":
                    st.markdown('<span class="tool-badge-calc">🧮 Calculator</span>', unsafe_allow_html=True)
        st.markdown(msg["content"])

# ── Input ──────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Search anything...")

if user_input and user_input.strip():
    with st.chat_message("user"):
        st.markdown(user_input.strip())
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(user_input.strip())
                tool_was_used = False

                # ── Tool detection — ONLY from actual agent signals ──
                import json as _json
                try:
                    parsed = _json.loads(response)
                    if isinstance(parsed, dict) and "tool" in parsed:
                        tool_was_used = parsed["tool"]
                except Exception:
                    pass

                # Reliable heuristic: Sources section means web_search ran
                if not tool_was_used and ("## 📚 Sources" in response or "**Sources:**" in response):
                    tool_was_used = "web_search"

            except Exception as e:
                response = f"⚠️ Something went wrong: {e}"
                tool_was_used = False

        # Badge display
        if tool_was_used == "web_search":
            st.markdown('<span class="tool-badge-search">🌐 Web Search</span>', unsafe_allow_html=True)
        elif tool_was_used == "calculator":
            st.markdown('<span class="tool-badge-calc">🧮 Calculator</span>', unsafe_allow_html=True)

        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.tool_used.append(tool_was_used)
