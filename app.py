
# ================= RED COSMIC THEME =================
import streamlit as st

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

:root {
    --red: #ff3155;
    --dark: #08070c;
    --panel: rgba(23, 15, 24, 0.82);
}

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* NỀN VŨ TRỤ */
.stApp {
    background:
        radial-gradient(ellipse at 15% 20%, rgba(150,0,40,.35), transparent 40%),
        radial-gradient(ellipse at 85% 75%, rgba(255,30,75,.16), transparent 35%),
        linear-gradient(135deg, #050509, #190711, #08070c);
    background-size: 200% 200%;
    animation: cosmicBackground 18s ease infinite;
}

@keyframes cosmicBackground {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* CÁC LỚP SAO */
.stars, .stars::before, .stars::after {
    position: fixed;
    inset: -100vh 0 0 0;
    content: "";
    pointer-events: none;
    z-index: 0;
    background-image:
        radial-gradient(2px 2px at 20% 30%, white 98%, transparent),
        radial-gradient(1px 1px at 40% 70%, #ff8da2 98%, transparent),
        radial-gradient(2px 2px at 70% 20%, white 98%, transparent),
        radial-gradient(1px 1px at 85% 65%, #ff3155 98%, transparent),
        radial-gradient(1px 1px at 55% 45%, white 98%, transparent),
        radial-gradient(2px 2px at 10% 85%, #ff9aab 98%, transparent);
    background-size: 350px 350px;
    animation: starMove 75s linear infinite,
               starTwinkle 4s ease-in-out infinite alternate;
}

.stars::before {
    opacity: .5;
    transform: scale(1.4);
    animation-duration: 110s, 6s;
}

.stars::after {
    opacity: .3;
    transform: scale(1.8);
    animation-duration: 150s, 8s;
}

@keyframes starMove {
    from { transform: translateY(0); }
    to { transform: translateY(100vh); }
}

@keyframes starTwinkle {
    from { opacity: .15; }
    to { opacity: .75; }
}

/* TINH VÂN ĐỎ */
.nebula {
    position: fixed;
    width: 500px;
    height: 500px;
    top: 15%;
    left: 30%;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(220,0,55,.20),
        rgba(120,0,35,.08) 40%,
        transparent 70%
    );
    filter: blur(35px);
    pointer-events: none;
    z-index: 0;
    animation: nebulaMove 25s ease-in-out infinite alternate;
}

@keyframes nebulaMove {
    0% { transform: translate(-150px, -80px) scale(.8); }
    50% { transform: translate(180px, 100px) scale(1.2); }
    100% { transform: translate(-50px, 200px) scale(.95); }
}

/* GIỮ NỘI DUNG Ở PHÍA TRƯỚC */
.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}

/* THANH MENU */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #100810, #200812);
    border-right: 1px solid rgba(255,50,85,.3);
}

/* TIÊU ĐỀ */
h1, h2, h3 {
    color: #ffffff !important;
}

/* KHUNG NỘI DUNG */
.cosmic-card {
    background: var(--panel);
    border: 1px solid rgba(255,60,90,.3);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 35px rgba(0,0,0,.35);
    transition: .3s ease;
}

.cosmic-card:hover {
    border-color: #ff3155;
    box-shadow: 0 0 25px rgba(255,30,75,.22);
    transform: translateY(-3px);
}

/* NÚT BẤM */
.stButton > button {
    background: linear-gradient(100deg, #8c0025, #ff3155, #a00030);
    background-size: 200% 100%;
    color: white !important;
    border: 1px solid rgba(255,120,140,.5);
    border-radius: 12px;
    font-weight: 700;
    transition: .3s ease;
}

.stButton > button:hover {
    background-position: 100% 0;
    box-shadow: 0 0 22px rgba(255,40,80,.5);
    transform: translateY(-2px);
}

/* Ô NHẬP LIỆU */
.stTextArea textarea,
.stTextInput input {
    background: rgba(10,8,15,.9) !important;
    color: white !important;
    border: 1px solid rgba(255,70,100,.35) !important;
    border-radius: 12px !important;
}

/* TAB */
.stTabs [aria-selected="true"] {
    color: #ff7189 !important;
    border-bottom-color: #ff3155 !important;
}

/* ĐƯỜNG PHÂN CÁCH */
hr {
    border-color: rgba(255,60,90,.25);
}

/* TÔN TRỌNG CÀI ĐẶT GIẢM CHUYỂN ĐỘNG */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
    }
}
</style>

<div class="stars"></div>
<div class="nebula"></div>
""", unsafe_allow_html=True)
