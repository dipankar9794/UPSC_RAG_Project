import streamlit as st
import ollama
import os
import math


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="UPSC AI Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MODELS / DATA
# =========================================================

EMBEDDING_MODEL = "nomic-embed-text"
LANGUAGE_MODEL = "llama3"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "upsc.txt")


# =========================================================
# PROFESSIONAL CSS  (visual layer only — no logic here)
# =========================================================

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap" rel="stylesheet">

<style>

/* =====================================================
   KEYFRAME ANIMATIONS
   ===================================================== */

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

@keyframes floatY {
    0%, 100% { transform: translateY(0px); }
    50%      { transform: translateY(-8px); }
}

@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes auroraDrift {
    0%   { transform: translate(0px, 0px) scale(1); }
    50%  { transform: translate(20px, -15px) scale(1.05); }
    100% { transform: translate(0px, 0px) scale(1); }
}

@keyframes pulseGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(99,102,241,0.35); }
    50%      { box-shadow: 0 0 0 10px rgba(99,102,241,0); }
}

@keyframes dotBounce {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
    40%           { transform: scale(1); opacity: 1; }
}

@keyframes glowPulse {
    0%, 100% { box-shadow: 0 0 20px rgba(99,102,241,0.15), inset 0 0 0 rgba(99,102,241,0); }
    50%      { box-shadow: 0 0 34px rgba(99,102,241,0.30), inset 0 0 0 rgba(99,102,241,0); }
}


/* =====================================================
   GLOBAL
   ===================================================== */

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(79, 70, 229, 0.18), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(124, 58, 237, 0.14), transparent 28%),
        radial-gradient(circle at 50% 100%, rgba(56, 189, 248, 0.08), transparent 35%),
        #070B14;
    background-size: 200% 200%, 200% 200%, 200% 200%, auto;
    animation: gradientShift 22s ease-in-out infinite;
    color: #f8fafc;
}

.stApp::before {
    content: "";
    position: fixed;
    top: -10%;
    left: -10%;
    width: 40vw;
    height: 40vw;
    background: radial-gradient(circle, rgba(99,102,241,0.10), transparent 65%);
    border-radius: 50%;
    animation: auroraDrift 16s ease-in-out infinite;
    pointer-events: none;
    z-index: 0;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 5rem;
    position: relative;
    z-index: 1;
}

.block-container > div {
    animation: fadeIn 0.6s ease both;
}


/* =====================================================
   SIDEBAR
   ===================================================== */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c111d 0%, #0a0e18 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] h1 {
    font-family: 'Sora', sans-serif;
    font-size: 1.5rem !important;
    background: linear-gradient(90deg, #a5b4fc, #f8fafc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

section[data-testid="stSidebar"] .stCode {
    border-radius: 10px;
}

section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
    animation: fadeInUp 0.5s ease both;
}


/* =====================================================
   HEADINGS
   ===================================================== */

h1 {
    font-family: 'Sora', sans-serif;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.05em !important;
}

h2 {
    font-family: 'Sora', sans-serif;
    font-weight: 800 !important;
    letter-spacing: -0.035em !important;
}

h3 {
    font-family: 'Sora', sans-serif;
    font-weight: 750 !important;
}

p {
    line-height: 1.7;
}

.stCaption {
    color: #818ba1 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
}


/* =====================================================
   INPUT
   ===================================================== */

div[data-baseweb="input"] {
    background: #111827 !important;
    border: 1px solid #273449 !important;
    border-radius: 14px !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

div[data-baseweb="input"]:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.20) !important;
}

div[data-baseweb="input"] input {
    color: #f8fafc !important;
}


/* =====================================================
   BUTTON
   ===================================================== */

.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #303b52;
    background: #151c2b;
    color: #f8fafc;
    font-weight: 700;
    padding: 0.65rem 1rem;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton > button:hover {
    border-color: #6366f1;
    background: #1b2340;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.25);
}

.stButton > button:active {
    transform: translateY(0px) scale(0.98);
}


/* =====================================================
   DIVIDER
   ===================================================== */

hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin-top: 2rem !important;
    margin-bottom: 2rem !important;
}


/* =====================================================
   METRICS
   ===================================================== */

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #0F172A, #0d1422);
    border: 1px solid #273449;
    border-radius: 16px;
    padding: 1rem;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    animation: fadeInUp 0.5s ease both;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #6366f1;
    box-shadow: 0 12px 28px rgba(99,102,241,0.18);
}


/* =====================================================
   EXPANDER
   ===================================================== */

div[data-testid="stExpander"] {
    background: #0F172A;
    border: 1px solid #273449;
    border-radius: 14px;
    margin-bottom: 0.8rem;
    transition: border-color 0.25s ease, transform 0.25s ease;
    animation: fadeInUp 0.45s ease both;
}

div[data-testid="stExpander"]:hover {
    border-color: #46547a;
    transform: translateX(2px);
}


/* =====================================================
   INFO / SUCCESS / ERROR
   ===================================================== */

div[data-testid="stAlert"] {
    border-radius: 14px;
    animation: fadeInUp 0.4s ease both;
}


/* =====================================================
   HERO
   ===================================================== */

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(129,140,248,0.35);
    color: #c7d2fe;
    padding: 0.35rem 0.9rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    animation: pulseGlow 2.4s ease-in-out infinite;
}

.hero-title {
    font-family: 'Sora', sans-serif;
    font-size: 2.85rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1.15;
    margin: 1rem 0 0.8rem 0;
    background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 45%, #a5b4fc 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientShift 6s ease-in-out infinite;
}

.hero-subtext {
    color: #a8b1c4;
    font-size: 1.02rem;
    line-height: 1.75;
    max-width: 560px;
    margin-bottom: 1.2rem;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.4rem;
}

.pill {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    color: #cbd5e1;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 600;
    transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
    animation: fadeInUp 0.5s ease both;
}

.pill:hover {
    transform: translateY(-2px);
    border-color: #6366f1;
    background: rgba(99,102,241,0.10);
}


/* =====================================================
   CHAT PREVIEW CARD (hero right side)
   ===================================================== */

.chat-preview {
    background: linear-gradient(160deg, rgba(99,102,241,0.10), rgba(15,22,36,0.9));
    border: 1px solid rgba(129,140,248,0.22);
    border-radius: 20px;
    padding: 1.4rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.35);
    animation: glowPulse 5s ease-in-out infinite, fadeInUp 0.7s ease both;
    position: relative;
    overflow: hidden;
}

.chat-preview-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.chat-preview-title {
    font-weight: 750;
    color: #e2e8f0;
    font-size: 0.85rem;
    letter-spacing: 0.02em;
}

.chat-bubble {
    border-radius: 14px;
    padding: 0.75rem 0.95rem;
    margin-bottom: 0.65rem;
    font-size: 0.86rem;
    line-height: 1.55;
    animation: fadeInUp 0.5s ease both;
}

.chat-bubble-label {
    font-size: 0.62rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
    display: block;
}

.chat-bubble-user {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #cbd5e1;
}

.chat-bubble-user .chat-bubble-label { color: #94a3b8; }

.chat-bubble-ai {
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(129,140,248,0.28);
    color: #e2e8f0;
}

.chat-bubble-ai .chat-bubble-label { color: #a5b4fc; }


/* =====================================================
   PIPELINE CARDS
   ===================================================== */

.pipeline-card {
    background: linear-gradient(145deg, #0F172A, #0d1420);
    border: 1px solid #273449;
    border-radius: 16px;
    padding: 1.2rem 1rem 1rem 1rem;
    text-align: center;
    min-height: 135px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    transition: transform 0.3s cubic-bezier(0.4,0,0.2,1), border-color 0.3s ease, box-shadow 0.3s ease;
    animation: fadeInUp 0.55s ease both;
    position: relative;
}

.pipeline-card:hover {
    transform: translateY(-6px) scale(1.03);
    border-color: #6366f1;
    box-shadow: 0 16px 34px rgba(99,102,241,0.22);
}

.pipeline-step {
    position: absolute;
    top: 0.6rem;
    right: 0.8rem;
    font-size: 0.62rem;
    font-weight: 800;
    color: #4c5a7a;
    letter-spacing: 0.05em;
}

.pipeline-icon {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
    display: inline-block;
    animation: floatY 3.5s ease-in-out infinite;
}

.pipeline-name {
    font-weight: 750;
    color: #f8fafc;
}


/* =====================================================
   FEATURE CARDS
   ===================================================== */

.feature-card {
    background: #0F172A;
    border: 1px solid #273449;
    border-radius: 18px;
    padding: 1.5rem;
    min-height: 180px;
    transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
    animation: fadeInUp 0.55s ease both;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: #6366f1;
    box-shadow: 0 18px 36px rgba(99,102,241,0.18);
}

.feature-number {
    color: #818cf8;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.1em;
}

.feature-icon {
    font-size: 1.8rem;
    margin: 0.8rem 0;
}

.feature-title {
    font-family: 'Sora', sans-serif;
    font-size: 1.05rem;
    font-weight: 750;
}

.feature-text {
    color: #8d98aa;
    line-height: 1.6;
    margin-top: 0.5rem;
}


/* =====================================================
   AI ASSISTANT SECTION
   ===================================================== */

.assistant-card {
    background: linear-gradient(160deg, rgba(99,102,241,0.08), rgba(15,22,36,0.95));
    border: 1px solid rgba(129,140,248,0.22);
    border-radius: 22px;
    padding: 1.6rem 1.6rem 0.4rem 1.6rem;
    box-shadow: 0 20px 55px rgba(0,0,0,0.3);
    animation: fadeInUp 0.55s ease both;
    margin-bottom: 1rem;
}

.assistant-helper {
    color: #7d8aa3;
    font-size: 0.82rem;
    margin: 0.3rem 0 0.9rem 0;
}


/* =====================================================
   RESPONSE CARD
   ===================================================== */

.response-card {
    background: linear-gradient(145deg, rgba(99,102,241,0.10), rgba(15,22,36,0.95));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 15px 40px rgba(0,0,0,0.20);
    animation: fadeInUp 0.5s ease both;
    line-height: 1.75;
}


/* =====================================================
   TYPING / LOADING DOTS
   ===================================================== */

.typing-dots {
    display: inline-flex;
    gap: 5px;
    align-items: center;
    margin-left: 4px;
}

.typing-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #818cf8;
    animation: dotBounce 1.2s infinite ease-in-out;
}

.typing-dots span:nth-child(2) { animation-delay: 0.15s; }
.typing-dots span:nth-child(3) { animation-delay: 0.3s; }


/* =====================================================
   STATUS PILL (online/offline)
   ===================================================== */

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

.status-online {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.35);
    color: #86efac;
}

.status-online .status-dot {
    background: #22c55e;
    animation: pulseGlow 1.8s ease-in-out infinite;
}

.status-offline {
    background: rgba(239,68,68,0.12);
    border: 1px solid rgba(239,68,68,0.35);
    color: #fca5a5;
}

.status-offline .status-dot {
    background: #ef4444;
}


/* =====================================================
   SECTION LABEL
   ===================================================== */

.section-label {
    display: inline-block;
    color: #818cf8;
    font-weight: 800;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    background: rgba(99,102,241,0.10);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    margin-bottom: 0.6rem;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #667085;
    padding-top: 2rem;
    font-size: 0.85rem;
    animation: fadeIn 1s ease both;
}


/* =====================================================
   SCROLLBAR
   ===================================================== */

::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-track {
    background: #070B14;
}
::-webkit-scrollbar-thumb {
    background: #273449;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #3b4a6b;
}


/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 768px) {

    h1 {
        font-size: 2.2rem !important;
    }

    .hero-title {
        font-size: 2rem;
    }

    .chat-preview {
        margin-top: 1rem;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# CHUNKING   (unchanged — core RAG logic)
# =========================================================

def create_chunks(text, chunk_size=500):

    words = text.split()

    chunks = []

    current_chunk = []

    current_length = 0

    for word in words:

        current_chunk.append(word)

        current_length += len(word)

        if current_length >= chunk_size:

            chunks.append(
                " ".join(current_chunk)
            )

            current_chunk = []

            current_length = 0

    if current_chunk:

        chunks.append(
            " ".join(current_chunk)
        )

    return chunks


# =========================================================
# VECTOR DATABASE   (unchanged — core RAG logic)
# =========================================================

@st.cache_resource
def initialize_vector_db():

    if not os.path.exists(DATASET_PATH):

        return []

    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as file:

        text = file.read()

    dataset = create_chunks(text)

    vector_db = []

    for chunk in dataset:

        try:

            response = ollama.embed(
                model=EMBEDDING_MODEL,
                input=chunk
            )

            embedding = response.embeddings[0]

            vector_db.append(
                (
                    chunk,
                    embedding
                )
            )

        except Exception:

            return []

    return vector_db


# =========================================================
# LOAD KNOWLEDGE BASE
# =========================================================

with st.spinner("Initializing UPSC AI knowledge base..."):

    VECTOR_DB = initialize_vector_db()


# =========================================================
# COSINE SIMILARITY   (unchanged — core RAG logic)
# =========================================================

def cosine_similarity(a, b):

    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = math.sqrt(
        sum(
            x * x
            for x in a
        )
    )

    norm_b = math.sqrt(
        sum(
            y * y
            for y in b
        )
    )

    if norm_a == 0 or norm_b == 0:

        return 0

    return dot_product / (norm_a * norm_b)


# =========================================================
# RETRIEVAL   (unchanged — core RAG logic)
# =========================================================

def retrieve(query, top_n=3):

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=query
    )

    query_embedding = response.embeddings[0]

    similarities = []

    for chunk, embedding in VECTOR_DB:

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        similarities.append(
            (
                chunk,
                score
            )
        )

    similarities.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return similarities[:top_n]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📚 UPSC AI")

    st.caption(
        "Retrieval-Augmented Knowledge Assistant"
    )

    st.divider()

    st.subheader("⚡ System Status")

    if VECTOR_DB:

        st.success("RAG System Online")

        st.metric(
            "Knowledge Chunks",
            len(VECTOR_DB)
        )

    else:

        st.error(
            "Knowledge Base Unavailable"
        )

    st.divider()

    st.subheader("🤖 AI Models")

    st.caption("Language Model")

    st.code(
        LANGUAGE_MODEL
    )

    st.caption("Embedding Model")

    st.code(
        EMBEDDING_MODEL
    )

    st.divider()

    st.subheader("🔗 RAG Pipeline")

    st.write("📄 UPSC Knowledge Base")
    st.write("↓")
    st.write("✂️ Text Chunking")
    st.write("↓")
    st.write("🧠 Embeddings")
    st.write("↓")
    st.write("🔎 Cosine Similarity")
    st.write("↓")
    st.write("📚 Top 3 Contexts")
    st.write("↓")
    st.write("🤖 Llama 3")
    st.write("↓")
    st.write("💬 Final Answer")


# =========================================================
# TOP HEADER
# =========================================================

header_left, header_right = st.columns(
    [4, 1]
)

with header_left:

    st.title("📚 UPSC AI")

    st.caption(
        "Knowledge Assistant  •  Retrieval-Augmented Generation"
    )

with header_right:

    if VECTOR_DB:

        st.markdown(
            '<div class="status-pill status-online">'
            '<span class="status-dot"></span> SYSTEM ONLINE</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-pill status-offline">'
            '<span class="status-dot"></span> SYSTEM OFFLINE</div>',
            unsafe_allow_html=True
        )


# =========================================================
# HERO  (two-column: copy + chat preview)
# =========================================================

st.write("")

hero_left, hero_right = st.columns([3, 2])

with hero_left:

    st.markdown(
        """
        <span class="hero-badge">✦ AI-Powered UPSC Knowledge</span>
        <div class="hero-title">Prepare smarter.<br>Ask your knowledge base.</div>
        <div class="hero-subtext">
            A Retrieval-Augmented AI assistant that retrieves relevant UPSC
            knowledge before generating grounded answers &mdash; combining
            semantic embeddings, cosine similarity and a locally running LLM.
        </div>
        <div class="pill-row">
            <span class="pill">🧠 Semantic Search</span>
            <span class="pill">🔎 Top-K Retrieval</span>
            <span class="pill">🤖 Llama 3</span>
            <span class="pill">📚 Grounded Answers</span>
        </div>
        """,
        unsafe_allow_html=True
    )

with hero_right:

    st.markdown(
        """
        <div class="chat-preview">
            <div class="chat-preview-header">
                <span class="chat-preview-title">🤖 UPSC AI Assistant</span>
                <span class="status-pill status-online" style="font-size:0.65rem;">
                    <span class="status-dot"></span> Retrieval Ready
                </span>
            </div>
            <div class="chat-bubble chat-bubble-user">
                <span class="chat-bubble-label">USER</span>
                What is UPSC eligibility?
            </div>
            <div class="chat-bubble chat-bubble-ai">
                <span class="chat-bubble-label">AI ASSISTANT</span>
                The system retrieves relevant information from the knowledge
                base before generating this answer.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")

hero1, hero2, hero3, hero4 = st.columns(4)

with hero1:
    st.metric("🧠 Retrieval", "Semantic")

with hero2:
    st.metric("🔎 Search", "Top 3")

with hero3:
    st.metric("🤖 LLM", "Llama 3")

with hero4:
    st.metric("🔒 AI", "Local")


# =========================================================
# PIPELINE
# =========================================================

st.divider()

st.markdown('<span class="section-label">System Pipeline</span>', unsafe_allow_html=True)

st.header("From question to grounded answer")

st.write(
    "This is the actual retrieval-augmented generation workflow implemented in the application."
)

pipeline_items = [
    ("💬", "Question"),
    ("🧠", "Embedding"),
    ("🔎", "Similarity"),
    ("📚", "Context"),
    ("🤖", "Llama 3"),
    ("✨", "Answer")
]

pipeline_columns = st.columns(6)

for idx, (column, item) in enumerate(
    zip(pipeline_columns, pipeline_items)
):

    with column:

        icon, name = item

        st.markdown(
            f"""
            <div class="pipeline-card" style="animation-delay:{idx * 0.08}s">
                <div class="pipeline-step">{idx + 1:02d}</div>
                <div class="pipeline-icon" style="animation-delay:{idx * 0.3}s">{icon}</div>
                <div class="pipeline-name">{name}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# HOW IT WORKS
# =========================================================

st.divider()

st.markdown('<span class="section-label">How It Works</span>', unsafe_allow_html=True)

st.header("Built around retrieval")

st.write(
    "The application retrieves relevant information before generating the final answer."
)

how1, how2, how3 = st.columns(3)

with how1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-number">
        01
        </div>

        <div class="feature-icon">
        💬
        </div>

        <div class="feature-title">
        Ask
        </div>

        <div class="feature-text">
        User enters a UPSC question.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with how2:

    st.markdown(
        """
        <div class="feature-card" style="animation-delay:0.1s">

        <div class="feature-number">
        02
        </div>

        <div class="feature-icon">
        🔎
        </div>

        <div class="feature-title">
        Retrieve
        </div>

        <div class="feature-text">
        The question is converted into an embedding and
        compared with stored embeddings using cosine similarity.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with how3:

    st.markdown(
        """
        <div class="feature-card" style="animation-delay:0.2s">

        <div class="feature-number">
        03
        </div>

        <div class="feature-icon">
        🤖
        </div>

        <div class="feature-title">
        Generate
        </div>

        <div class="feature-text">
        The retrieved context is passed to Llama 3 through Ollama.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# AI ASSISTANT  (main interactive section)
# =========================================================

st.divider()

st.markdown('<span class="section-label">AI Assistant</span>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="assistant-card">
        <h2 style="margin-bottom:0;">🤖 UPSC AI Assistant</h2>
        <div class="assistant-helper">
            Retrieval-Augmented Question Answering &mdash; ask anything
            available in the UPSC knowledge base.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

input_query = st.text_input(
    "Your question",
    placeholder="Example: What is UPSC eligibility criteria?",
    key="upsc_question",
    label_visibility="collapsed"
)


# =========================================================
# PROCESS QUESTION
# =========================================================

if input_query:

    if not VECTOR_DB:

        st.error(
            "The knowledge base is unavailable. "
            "Make sure Ollama is running and upsc.txt exists."
        )

    else:

        # =================================================
        # RETRIEVAL
        # =================================================

        with st.spinner(
            "🔎 Searching the UPSC knowledge base..."
        ):

            try:

                retrieved_knowledge = retrieve(
                    input_query
                )

            except Exception as e:

                st.error(
                    f"Retrieval Error: {e}"
                )

                retrieved_knowledge = []


        # =================================================
        # RETRIEVED INFORMATION
        # =================================================

        if retrieved_knowledge:

            st.divider()

            st.markdown('<span class="section-label">Retrieved Context</span>', unsafe_allow_html=True)

            st.subheader("📚 Top 3 relevant knowledge chunks")

            for i, (chunk, similarity) in enumerate(
                retrieved_knowledge
            ):

                with st.expander(
                    f"📚 Source {i + 1:02d}   •   Similarity {similarity:.4f}"
                ):

                    metric1, metric2 = st.columns(2)

                    with metric1:

                        st.metric(
                            "Similarity Score",
                            f"{similarity:.4f}"
                        )

                    with metric2:

                        st.metric(
                            "Rank",
                            f"#{i + 1}"
                        )

                    st.progress(
                        min(max(similarity, 0.0), 1.0)
                    )

                    st.markdown("#### Relevant Context")

                    st.write(chunk)


        # =================================================
        # BUILD CONTEXT
        # =================================================

        context = "\n\n".join(
            [
                chunk
                for chunk, similarity
                in retrieved_knowledge
            ]
        )


        # =================================================
        # PROMPT
        # =================================================

        instruction_prompt = f"""

You are a UPSC Exam Assistant.

Answer the user only using the provided context.

Do not create or assume information.

If information is not available, reply:

"I don't have enough information in my knowledge base."


Context:

{context}

"""


        # =================================================
        # LLM RESPONSE
        # =================================================

        st.divider()

        st.markdown('<span class="section-label">AI Response</span>', unsafe_allow_html=True)

        st.subheader("🤖 AI Generated Answer")

        response_placeholder = st.empty()

        response_placeholder.markdown(
            '<div class="response-card">Thinking'
            '<span class="typing-dots"><span></span><span></span><span></span></span>'
            '</div>',
            unsafe_allow_html=True
        )

        full_response = ""

        try:

            with st.spinner(
                "🤖 Generating answer with Llama 3..."
            ):

                stream = ollama.chat(

                    model=LANGUAGE_MODEL,

                    messages=[

                        {
                            "role": "system",
                            "content": instruction_prompt
                        },

                        {
                            "role": "user",
                            "content": input_query
                        }

                    ],

                    stream=True

                )

                for chunk in stream:

                    token = chunk[
                        "message"
                    ][
                        "content"
                    ]

                    full_response += token

                    response_placeholder.markdown(
                        f'<div class="response-card">{full_response}▌</div>',
                        unsafe_allow_html=True
                    )

            response_placeholder.markdown(
                f'<div class="response-card">{full_response}</div>',
                unsafe_allow_html=True
            )

        except Exception as e:

            st.error(
                f"LLM Error: {e}"
            )


# =========================================================
# PROJECT INFORMATION
# =========================================================

st.divider()

st.markdown('<span class="section-label">Project</span>', unsafe_allow_html=True)

st.header("UPSC Retrieval-Augmented AI")

project1, project2, project3 = st.columns(3)

with project1:

    st.markdown(
        """
        <div class="feature-card">

        <div class="feature-icon">
        🧠
        </div>

        <div class="feature-title">
        Semantic Retrieval
        </div>

        <div class="feature-text">
        Questions and knowledge chunks are converted into
        embeddings and compared using cosine similarity.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with project2:

    st.markdown(
        """
        <div class="feature-card" style="animation-delay:0.1s">

        <div class="feature-icon">
        🔒
        </div>

        <div class="feature-title">
        Local AI
        </div>

        <div class="feature-text">
        The application uses Ollama locally with Llama 3
        for generation and nomic-embed-text for embeddings.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with project3:

    st.markdown(
        """
        <div class="feature-card" style="animation-delay:0.2s">

        <div class="feature-icon">
        ⚡
        </div>

        <div class="feature-title">
        Grounded Generation
        </div>

        <div class="feature-text">
        Retrieved context is passed to Llama 3 before
        generating the final, grounded answer.
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        📚 UPSC AI · Retrieval-Augmented Knowledge Assistant
        <br>
        Python · Streamlit · Ollama · Llama 3 · nomic-embed-text
    </div>
    """,
    unsafe_allow_html=True
)