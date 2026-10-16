
st.markdown("""
<style>
/* ===== SOFT PASTEL THEME ===== */
:root {
    --cream: #FFF8F3;
    --pink: #F4DDE2;
    --beige: #E8D2C0;
    --lavender: #D9C8E8;
    --rose: #B98286;
    --ink: #59464B;
}

/* Nền tổng thể */
.stApp {
    background: linear-gradient(
        135deg,
        #FFF8F3 0%,
        #FFF1F3 38%,
        #F7F0FA 72%,
        #F5E8DD 100%
    );
    color: var(--ink);
}

/* Các mảng màu chuyển động */
.stApp::before,
.stApp::after {
    content: "";
    position: fixed;
    width: 340px;
    height: 340px;
    border-radius: 50%;
    filter: blur(65px);
    opacity: 0.48;
    pointer-events: none;
    z-index: 0;
}

.stApp::before {
    background: #F2C9D4;
    top: 8%;
    left: -120px;
    animation: floatPink 18s ease-in-out infinite alternate;
}

.stApp::after {
    background: #D9C8E8;
    right: -120px;
    bottom: 5%;
    animation: floatLilac 22s ease-in-out infinite alternate;
}

/* Chuyển động nền */
@keyframes floatPink {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(100px, 80px) scale(1.15); }
    100% { transform: translate(35px, 180px) scale(0.95); }
}

@keyframes floatLilac {
    0%   { transform: translate(0, 0) scale(1); }
    50%  { transform: translate(-100px, -65px) scale(1.2); }
    100% { transform: translate(-30px, -150px) scale(0.9); }
}

/* Giữ nội dung nằm trên nền */
[data-testid="stAppViewContainer"] {
    background: transparent;
}

[data-testid="stMain"],
.main .block-container {
    position: relative;
    z-index: 1;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

/* Tiêu đề */
h1, h2, h3 {
    color: #79545D !important;
    letter-spacing: -0.4px;
}

p, label, li {
    color: #59464B;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #FFF8F3,
        #F8E8E9,
        #F0E6F4
    );
    border-right: 1px solid #EBD9DD;
}

[data-testid="stSidebar"] * {
    color: #654F55;
}

/* Nút bấm */
.stButton > button,
.stDownloadButton > button {
    border: 1px solid #E3C4CA;
    border-radius: 14px;
    background: linear-gradient(135deg, #EFCFD6, #E6D8EB);
    color: #65464F;
    font-weight: 600;
    transition: all 0.25s ease;
    box-shadow: 0 4px 14px rgba(185, 130, 134, 0.12);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-2px);
    border-color: #C99BA5;
    background: linear-gradient(135deg, #F5DDE2, #E8DDF2);
    box-shadow: 0 8px 20px rgba(185, 130, 134, 0.2);
}

/* Thẻ thống kê */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.76);
    border: 1px solid #EAD9D9;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 22px rgba(120, 80, 90, 0.06);
    transition: transform 0.25s ease,
                box-shadow 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 26px rgba(120, 80, 90, 0.11);
}

/* Khung nội dung, form và expander */
[data-testid="stForm"],
[data-testid="stExpander"],
[data-testid="stAlert"] {
    border-radius: 16px;
}

[data-testid="stForm"],
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.60);
    border: 1px solid #EAD9D9;
}

/* Ô nhập liệu */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: rgba(255, 255, 255, 0.88);
    color: #59464B;
    border: 1px solid #E5CDD1;
    border-radius: 12px;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #C99BA5;
    box-shadow: 0 0 0 2px rgba(201, 155, 165, 0.16);
}

/* Thanh trên cùng */
[data-testid="stHeader"] {
    background: rgba(255, 248, 243, 0.72);
}

/* Tôn trọng cài đặt giảm chuyển động */
@media (prefers-reduced-motion: reduce) {
    .stApp::before,
    .stApp::after {
        animation: none;
    }

    .stButton > button,
    [data-testid="stMetric"] {
        transition: none;
    }
}
</style>
""", unsafe_allow_html=True)

