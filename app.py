import json
import os
import time
import uuid
from pathlib import Path

import streamlit as st
from openai import OpenAI

# --- one-time dark theme file (applies after you restart the app once) -------
try:
    _cfg = Path.cwd() / ".streamlit" / "config.toml"
    if not _cfg.exists():
        _cfg.parent.mkdir(exist_ok=True)
        _cfg.write_text(
            '[theme]\nbase = "dark"\nprimaryColor = "#FF5A36"\n'
            'backgroundColor = "#150F23"\nsecondaryBackgroundColor = "#1F1733"\n'
            'textColor = "#F4EFFA"\n'
        )
except Exception:
    pass

st.set_page_config(page_title="Crucible", layout="centered")

# ---------------------------------------------------------------- styling ---
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Instrument+Sans:wght@400;500;600&display=swap');

:root {
    --bg: #150F23;
    --surface: #1F1733;
    --surface-2: #2A2045;
    --line: #3D3060;
    --text: #F4EFFA;
    --muted: #C3B7DB;
    --ember: #FF5A36;
    --violet: #7C5CFF;
}

/* ---------- page ---------- */
.stApp {
    background:
        radial-gradient(900px 520px at 88% -8%, rgba(255, 90, 54, .24), transparent 60%),
        radial-gradient(760px 520px at -8% 6%, rgba(124, 92, 255, .26), transparent 60%),
        var(--bg);
    color: var(--text);
    font-family: 'Instrument Sans', sans-serif;
    color-scheme: dark;
}
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 780px; padding-top: 3.5rem; padding-bottom: 7rem; }

/* ---------- hero ---------- */
.hero h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800;
    font-size: clamp(2.6rem, 7.5vw, 4.5rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: var(--text);
    margin: 0 0 1rem 0;
    padding: 0;
}
.hero p {
    color: var(--muted);
    font-size: 1.15rem;
    line-height: 1.55;
    max-width: 34rem;
    margin: 0 0 2rem 0;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: .5rem;
    border: 1px solid var(--line); background: rgba(31, 23, 51, .7);
    color: var(--muted); font-size: .85rem;
    padding: .35rem .8rem; border-radius: 999px; margin-bottom: 1.4rem;
}
.hero-badge i {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--ember); box-shadow: 0 0 10px var(--ember);
    display: inline-block;
}
@media (prefers-reduced-motion: no-preference) {
    .hero-badge i { animation: pulse 2.2s ease-in-out infinite; }
    @keyframes pulse { 50% { opacity: .35; } }
}

/* ---------- chat messages (no avatars) ---------- */
[data-testid="stChatMessageAvatarAssistant"],
[data-testid="stChatMessageAvatarUser"],
[data-testid^="stChatMessageAvatar"] { display: none !important; }

[data-testid="stChatMessage"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-left: 3px solid var(--ember);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    margin-bottom: .9rem;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--surface-2);
    border-left: 3px solid var(--violet);
}
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li { color: var(--text); line-height: 1.65; }
[data-testid="stChatMessage"] h1,
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    font-family: 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.01em;
    color: var(--text);
}
[data-testid="stChatMessage"] h3 { font-size: 1.25rem; margin-top: 1rem; }
[data-testid="stChatMessage"] strong { color: #fff; }

/* ---------- buttons ---------- */
.stButton > button {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: .65rem 1rem;
    height: auto;
    min-height: 3rem;
    font-family: 'Instrument Sans', sans-serif;
    font-weight: 500;
    transition: border-color .15s ease, background .15s ease;
}
.stButton > button p { white-space: normal; color: var(--text); }
.stButton > button:hover {
    border-color: var(--ember);
    background: rgba(255, 90, 54, .10);
    color: var(--text);
}
.stButton > button:focus-visible { outline: 2px solid var(--violet); outline-offset: 2px; }

.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"] {
    background: rgba(255, 90, 54, .16) !important;
    border: 1px solid var(--ember) !important;
    color: var(--text) !important;
}

/* ---------- chat input ---------- */
[data-testid="stChatInput"],
[data-testid="stChatInput"] > div,
[data-testid="stChatInput"] div[data-baseweb="textarea"],
[data-testid="stChatInput"] div[data-baseweb="base-input"] {
    background: var(--surface) !important;
    border-radius: 28px;
}
[data-testid="stChatInput"] { border: 1px solid var(--line); }
[data-testid="stChatInput"]:focus-within { border-color: var(--ember); }
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: var(--muted) !important; opacity: 1; }
[data-testid="stChatInput"] button { background: var(--surface-2) !important; }
[data-testid="stChatInput"] button svg { color: var(--text) !important; fill: var(--text) !important; }
[data-testid="stBottom"] > div { background: transparent; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: #100A1C;
    border-right: 1px solid var(--line);
    color-scheme: dark;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.01em;
    color: var(--text) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: var(--text) !important;
    font-weight: 600;
    font-size: .95rem;
}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color: var(--muted) !important; }
[data-testid="stSidebar"] [data-testid="stTooltipIcon"] svg { color: var(--muted) !important; }
[data-testid="stSidebar"] [data-testid="stTickBarMin"],
[data-testid="stSidebar"] [data-testid="stTickBarMax"] { color: var(--muted) !important; font-weight: 500; }

[data-testid="stSidebar"] .stButton > button { justify-content: flex-start; text-align: left; }
[data-testid="stSidebar"] .stButton > button p { text-align: left; font-size: .92rem; }

[data-testid="stSidebar"] [data-testid="stExpander"] details {
    border: 1px solid var(--line);
    border-radius: 14px;
    background: transparent;
}
[data-testid="stSidebar"] [data-testid="stExpander"] summary p { color: var(--text) !important; font-weight: 600; }

[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="input"] *,
[data-testid="stSidebar"] [data-baseweb="base-input"],
[data-testid="stSidebar"] [data-baseweb="base-input"] *,
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"],
[data-testid="stSidebar"] [data-testid="stTextInputRootElement"] *,
[data-testid="stSidebar"] [data-baseweb="select"],
[data-testid="stSidebar"] [data-baseweb="select"] * {
    background-color: #241A3D !important;
    color: var(--text) !important;
    -webkit-text-fill-color: var(--text) !important;
    fill: var(--text) !important;
}
[data-testid="stSidebar"] [data-baseweb="input"],
[data-testid="stSidebar"] [data-baseweb="base-input"],
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
}
[data-testid="stSidebar"] input::placeholder { color: var(--muted) !important; }

div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li {
    background: var(--surface) !important;
    color: var(--text) !important;
}
div[data-baseweb="popover"] li:hover { background: var(--surface-2) !important; }

a { color: var(--ember) !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------ data ----
NEBIUS_URL = "https://api.tokenfactory.nebius.com/v1/"
KEY_URL = "https://tokenfactory.nebius.com/project/api-keys"
HISTORY_FILE = Path(__file__).with_name("chat_history.json")

# Used if the live model list can't be loaded
FALLBACK_MODELS = ["nvidia/nemotron-3-super-120b-a12b"]

GREETING = (
    "Hello. I'm the person your investors will be on a bad day.\n\n"
    "Tell me what you're building, who it's for, and why anyone would pay for it. "
    "I'll find the holes before the market does, then ask you three questions you "
    "need good answers to."
)

STARTERS = {
    "Mentor matching app": (
        "I'm building an app that matches college students with working professionals "
        "in their city for 30-minute monthly mentoring calls. Free for students, "
        "mentors volunteer, and we plan to earn from college partnerships."
    ),
    "Electricity bill explainer": (
        "I want to build an AI tool that reads a household's electricity bill, "
        "explains each charge in simple language, and suggests ways to cut usage. "
        "Target market is middle-class families in India."
    ),
    "Local snack box": (
        "My idea is a monthly subscription box of regional snacks from small "
        "producers across Tamil Nadu, shipped across India at around 499 rupees a month."
    ),
}

HARSHNESS = {
    "Firm": "Be direct and fair. Acknowledge real strengths briefly, then focus on the flaws.",
    "Ruthless": "Be unsparing. Assume the founder is overestimating demand and underestimating competition.",
    "Brutal": "Be as harsh as a failed-founder-turned-investor. Assume the idea is weak until proven otherwise. No softening.",
}

BASE_PROMPT = """
You are a highly analytical, professional venture capitalist.
Your job is to stress-test the user's startup or product idea.
Identify logical gaps, market risks, and structural flaws.
Keep a sharp, clinical, professional tone. No emojis, corporate fluff, or generic buzzwords.

On the first analysis, use these markdown sections: Verdict, Market Risk, Business Model,
Execution Risk, Competition. Keep each to 2 to 4 tight bullet points.
End with exactly 3 targeted questions the founder must answer to defend the concept.

On later turns, respond to the founder's defence directly. Say which points now hold up,
which are still weak, and ask at most 2 follow-up questions.
"""


def build_system_prompt(level: str) -> str:
    return f"{BASE_PROMPT}\nTone setting: {HARSHNESS[level]}"


# ------------------------------------------------------- history storage ----
def load_chats() -> dict:
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_chats() -> None:
    try:
        HISTORY_FILE.write_text(
            json.dumps(st.session_state.chats, ensure_ascii=False, indent=1),
            encoding="utf-8",
        )
    except Exception:
        pass


def new_chat() -> None:
    st.session_state.current = None


def open_chat(cid: str) -> None:
    st.session_state.current = cid


def delete_chat(cid: str) -> None:
    st.session_state.chats.pop(cid, None)
    st.session_state.current = None
    save_chats()


def make_title(text: str) -> str:
    first = text.strip().splitlines()[0] if text.strip() else "Untitled pitch"
    return first if len(first) <= 34 else first[:33].rstrip() + "…"


# ---------------------------------------------------------------- models ----
@st.cache_data(ttl=600, show_spinner=False)
def fetch_models(key: str) -> list:
    """Ask Nebius which Nemotron models this API key can use right now."""
    try:
        client = OpenAI(base_url=NEBIUS_URL, api_key=key)
        ids = [m.id for m in client.models.list().data]
    except Exception:
        return []
    return [i for i in ids if "nemotron" in i.lower()]


def order_models(live: list) -> list:
    if not live:
        return FALLBACK_MODELS
    # Prefer the Super model, then the rest alphabetically
    return sorted(live, key=lambda m: (0 if "super" in m.lower() else 1, m))


def visible_tokens(stream):
    """Yield reply text and drop any <think>...</think> reasoning blocks."""
    buf, in_think = "", False
    for chunk in stream:
        if not chunk.choices:
            continue
        text = chunk.choices[0].delta.content
        if not text:
            continue
        buf += text
        while True:
            if in_think:
                end = buf.find("</think>")
                if end == -1:
                    buf = buf[-8:]
                    break
                buf = buf[end + 8:].lstrip()
                in_think = False
            else:
                start = buf.find("<think>")
                if start == -1:
                    safe = len(buf) - 6  # keep a tail in case a tag is split
                    if safe > 0:
                        yield buf[:safe]
                        buf = buf[safe:]
                    break
                if start > 0:
                    yield buf[:start]
                buf = buf[start + 7:]
                in_think = True
    if not in_think and buf:
        yield buf


# ----------------------------------------------------------------- state ----
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()
if "current" not in st.session_state:
    st.session_state.current = None
if "pending" not in st.session_state:
    st.session_state.pending = None
    st.session_state.pending_title = None

chats = st.session_state.chats

# --------------------------------------------------------------- sidebar ----
with st.sidebar:
    history_box = st.container()  # filled at the bottom of the script

    default_key = os.environ.get("NEBIUS_API_KEY", "")
    try:
        default_key = default_key or st.secrets.get("NEBIUS_API_KEY", "")
    except Exception:
        pass

    with st.expander("Settings", expanded=not default_key):
        api_key = st.text_input(
            "Nebius API key",
            type="password",
            value=default_key,
            help="Create a key in the Nebius Token Factory console. Never commit your key to GitHub.",
        )
        st.markdown(f"[Get a Nebius key]({KEY_URL})")

        level = st.select_slider("How harsh?", options=list(HARSHNESS.keys()), value="Ruthless")

        live_models = fetch_models(api_key) if api_key else []
        model = st.selectbox(
            "Model",
            order_models(live_models),
            help="NVIDIA Nemotron models available on your Nebius account.",
        )

# ------------------------------------------------------------------ main ----
current_id = st.session_state.current if st.session_state.current in chats else None
messages = chats[current_id]["messages"] if current_id else []

if not messages:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge"><i></i>Crucible</div>
            <h1>Pitch it. We'll try to break it.</h1>
            <p>Get the investor critique before you get the investor meeting.
            Flaws, risks and the questions you'll be asked.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.chat_message("assistant"):
    st.markdown(GREETING)

if not messages:
    st.caption("Not sure where to start? Try one of these.")
    cols = st.columns(len(STARTERS))
    for col, (label, full_pitch) in zip(cols, STARTERS.items()):
        if col.button(label, use_container_width=True, key=f"starter_{label}"):
            st.session_state.pending = full_pitch
            st.session_state.pending_title = label
            st.rerun()

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

typed = st.chat_input("Describe your idea, or defend it here")
prompt = typed or st.session_state.pending
title_hint = st.session_state.pending_title if (not typed and st.session_state.pending) else None
st.session_state.pending = None
st.session_state.pending_title = None

if prompt and not api_key:
    st.error("Add your Nebius API key in the sidebar Settings first.")

elif prompt:
    if current_id is None:
        current_id = uuid.uuid4().hex[:8]
        chats[current_id] = {
            "title": title_hint or make_title(prompt),
            "messages": [],
            "updated": time.time(),
        }
        st.session_state.current = current_id
    messages = chats[current_id]["messages"]

    messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client = OpenAI(base_url=NEBIUS_URL, api_key=api_key)
    payload = [{"role": "system", "content": build_system_prompt(level)}] + messages

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=payload,
                temperature=0.6,
                stream=True,
            )
            reply = st.write_stream(visible_tokens(stream))
            messages.append({"role": "assistant", "content": reply})
            chats[current_id]["updated"] = time.time()
            save_chats()

        except Exception as e:
            messages.pop()
            if not messages:
                chats.pop(current_id, None)
                st.session_state.current = None
            err = str(e)
            low = err.lower()
            if "401" in err or "invalid" in low and "key" in low:
                st.error("That Nebius API key was rejected. Check it in Settings and try again.")
            elif "404" in err or "model" in low and "not" in low:
                st.error("That model isn't available on your Nebius account. Pick another in Settings and send again.")
            elif "429" in err:
                st.error("Rate limit hit. Wait a few seconds and send it again.")
            else:
                st.error(f"Something went wrong: {err}")

# ------------------------------------------- chat history (top of sidebar) --
with history_box:
    st.markdown("### Chats")
    st.button("New pitch", on_click=new_chat, use_container_width=True, key="new_pitch")

    ordered = sorted(chats.items(), key=lambda kv: kv[1].get("updated", 0), reverse=True)
    if not ordered:
        st.caption("Your past pitches will show up here.")
    for cid, chat in ordered[:25]:
        st.button(
            chat["title"],
            key=f"chat_{cid}",
            on_click=open_chat,
            args=(cid,),
            use_container_width=True,
            type="primary" if cid == st.session_state.current else "secondary",
        )

    if st.session_state.current in chats:
        st.button(
            "Delete this chat",
            key="delete_chat",
            on_click=delete_chat,
            args=(st.session_state.current,),
            use_container_width=True,
        )
