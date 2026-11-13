
import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

NAVY = "#00246B"
ICE = "#CADCFC"
WHITE = "#FFFFFF"
BLACK = "#000000"

# =====================================================
# 2. CSS - NAVY COSMIC INTERFACE
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

:root {
    --navy: #00246B;
    --ice: #CADCFC;
    --ink: #000000;
    --panel: #EAF1FF;
    --panel-strong: #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif !important;
}

/* NỀN TOÀN ỨNG DỤNG TỐI */
.stApp {
    background:
        radial-gradient(ellipse at 12% 18%, rgba(202,220,252,.16), transparent 34%),
        radial-gradient(ellipse at 88% 78%, rgba(80,130,220,.20), transparent 40%),
        linear-gradient(135deg, #00143D, #00246B, #000B27) !important;
    background-size: 200% 200%;
    animation: backgroundMove 18s ease infinite;
    color: #000000 !important;
}
@keyframes backgroundMove {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* VÙNG NỘI DUNG SÁNG ĐỂ CHỮ ĐEN DỄ ĐỌC */
section[data-testid="stMain"] > div,
.main .block-container {
    color: #000000 !important;
}
.main .block-container {
    background: rgba(234,241,255,.97) !important;
    border: 1px solid rgba(202,220,252,.8);
    border-radius: 22px;
    padding: 2rem 2.2rem !important;
    margin-top: 1.2rem;
    margin-bottom: 2rem;
    box-shadow: 0 14px 45px rgba(0,0,0,.22);
}

/* ÉP TOÀN BỘ VĂN BẢN THÀNH MÀU ĐEN */
.stApp p, .stApp span, .stApp label, .stApp li,
.stApp h1, .stApp h2, .stApp h3, .stApp h4,
.stApp h5, .stApp h6, .stApp strong, .stApp b,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stCaptionContainer"],
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricDelta"],
.stApp .stRadio, .stApp .stCheckbox,
.stApp [data-testid="stWidgetLabel"] {
    color: #000000 !important;
}

h1, h2, h3, h4, h5, h6 { color: #000000 !important; font-weight: 800 !important; }
.subtitle, .stCaption, [data-testid="stCaptionContainer"] { color: #000000 !important; }

/* HEADER VÀ SIDEBAR SÁNG */
header[data-testid="stHeader"] {
    background: #CADCFC !important;
    border-bottom: 1px solid #91B8F5;
}
header[data-testid="stHeader"] * { color: #000000 !important; }
[data-testid="stToolbar"] { background: transparent !important; }
[data-testid="stDecoration"] { background: #00246B !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF, #CADCFC) !important;
    border-right: 1px solid #91B8F5;
}
section[data-testid="stSidebar"] * { color: #000000 !important; }
section[data-testid="stSidebar"] [role="radiogroup"] label {
    color: #000000 !important;
    background: rgba(255,255,255,.55);
    border-radius: 10px;
    padding: 5px 8px;
}

/* KHUNG HERO VÀ CÁC THẺ ĐỀU SÁNG */
.hero, .glass-card {
    background: linear-gradient(135deg, #FFFFFF, #CADCFC) !important;
    color: #000000 !important;
    border: 1px solid #91B8F5 !important;
    border-radius: 20px;
    padding: 24px;
    margin: 12px 0 20px;
    box-shadow: 0 8px 28px rgba(0,20,61,.14);
    backdrop-filter: blur(10px);
    transition: all .3s ease;
}
.hero:hover, .glass-card:hover {
    border-color: #00246B !important;
    box-shadow: 0 12px 32px rgba(0,36,107,.2);
    transform: translateY(-2px);
}
.hero-title, .hero-description, .glass-card h3, .glass-card p,
.hero *, .glass-card * { color: #000000 !important; }
.hero-title { font-size: clamp(28px, 5vw, 46px); font-weight: 800; letter-spacing: 1px; }
.hero-description { font-size: 16px; line-height: 1.8; }

/* BUTTONS */
.stButton > button, .stDownloadButton > button {
    background: linear-gradient(135deg, #FFFFFF, #CADCFC) !important;
    color: #000000 !important;
    border: 1px solid #00246B !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    transition: all .25s ease;
}
.stButton > button *, .stDownloadButton > button * { color: #000000 !important; }
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #FFFFFF !important;
    box-shadow: 0 0 18px rgba(0,36,107,.25);
    transform: translateY(-2px);
}

/* Ô NHẬP LIỆU VÀ CÁC WIDGET CÓ NỀN SÁNG */
.stTextArea textarea, .stTextInput input,
.stNumberInput input, .stDateInput input {
    background: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #557DBB !important;
    border-radius: 12px !important;
    caret-color: #000000 !important;
}
.stTextArea textarea::placeholder, .stTextInput input::placeholder {
    color: #444444 !important; opacity: 1;
}
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #557DBB !important;
    color: #000000 !important;
}
.stSelectbox div[data-baseweb="select"] *,
.stMultiSelect div[data-baseweb="select"] * { color: #000000 !important; }
div[data-baseweb="popover"], div[data-baseweb="menu"], div[role="listbox"] {
    background: #FFFFFF !important;
}
div[role="option"] { color: #000000 !important; background: #FFFFFF !important; }
div[role="option"]:hover { background: #CADCFC !important; }
.stRadio label, .stCheckbox label { color: #000000 !important; }

/* METRICS, ALERTS, DATAFRAME, TABS */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #91B8F5 !important;
    padding: 18px;
    border-radius: 16px;
}
[data-testid="stMetricLabel"], [data-testid="stMetricValue"],
[data-testid="stMetricDelta"] { color: #000000 !important; }
div[data-testid="stAlert"] {
    background: #FFFFFF !important;
    border: 1px solid #91B8F5 !important;
    border-radius: 14px;
}
div[data-testid="stAlert"] * { color: #000000 !important; }
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: #FFFFFF !important;
    border: 1px solid #91B8F5 !important;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"], .stTabs [aria-selected="true"] {
    color: #000000 !important;
}
.stProgress > div > div > div > div { background-color: #00246B !important; }
a { color: #00246B !important; }
hr { border-color: #91B8F5 !important; }

/* HIỆU ỨNG SAO TRÊN NỀN TỐI */
.stApp::before {
    content: ""; position: fixed; inset: 0; pointer-events: none;
    z-index: 0; opacity: .35;
    background-image:
        radial-gradient(2px 2px at 10% 20%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 25% 75%, #FFFFFF 50%, transparent 100%),
        radial-gradient(1.5px 1.5px at 45% 35%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 70% 15%, #FFFFFF 50%, transparent 100%),
        radial-gradient(1.5px 1.5px at 85% 65%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 95% 35%, #FFFFFF 50%, transparent 100%);
    background-size: 350px 350px;
    animation: starsMove 35s linear infinite;
}
@keyframes starsMove { from { transform: translateY(0); } to { transform: translateY(-350px); } }
footer, #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION STATE
# =====================================================

defaults = {
    "records": [],
    "analysis_count": 0,
    "verified_count": 0,
    "reflection_count": 0,
    "scenario_done": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 4. BASIC ANALYSIS
# =====================================================

RISK_KEYWORDS = {
    "Ngôn ngữ giật gân": [
        "sốc", "kinh hoàng", "chấn động",
        "không thể tin", "bí mật động trời"
    ],
    "Thúc giục chia sẻ": [
        "chia sẻ ngay", "share ngay",
        "gửi cho mọi người", "đừng bỏ lỡ"
    ],
    "Thiếu nguồn rõ ràng": [
        "nghe nói", "người ta bảo",
        "theo nguồn tin", "một người bạn"
    ],
    "Khẳng định tuyệt đối": [
        "100%", "chắc chắn", "tất cả đều",
        "không bao giờ", "luôn luôn"
    ],
    "Tạo áp lực và sợ hãi": [
        "nguy hiểm", "khẩn cấp",
        "cảnh báo ngay", "nếu không sẽ"
    ]
}


def basic_analysis(content):
    found = []
    text = content.lower()

    for category, keywords in RISK_KEYWORDS.items():
        matched = [word for word in keywords if word in text]
        if matched:
            found.append({
                "category": category,
                "keywords": matched
            })

    score = min(len(found) * 20, 100)

    if score >= 60:
        level = "Cần kiểm chứng kỹ"
        advice = "Nội dung có nhiều dấu hiệu cần chú ý. Hãy kiểm tra nguồn và tìm thêm bằng chứng."
    elif score >= 20:
        level = "Cần thận trọng"
        advice = "Nội dung có một số dấu hiệu đáng chú ý. Nên đối chiếu với các nguồn độc lập."
    else:
        level = "Ít dấu hiệu cảnh báo"
        advice = "Chưa phát hiện nhiều dấu hiệu theo bộ từ khóa. Điều này không chứng minh nội dung là đúng."

    return score, level, found, advice


# =====================================================
# 5. GEMINI AI
# =====================================================

def gemini_analysis(content):
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        return None, "Chưa cấu hình Gemini API Key."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Bạn là trợ lý giáo dục của dự án Social Sandbox AI.

Hãy phân tích nội dung sau bằng tiếng Việt:

{content}

Trình bày:
1. Tóm tắt nội dung.
2. Dấu hiệu đáng chú ý.
3. Đánh giá nguồn thông tin.
4. Ba câu hỏi tư duy phản biện.
5. Khuyến nghị trước khi chia sẻ.

Không tự kết luận nội dung đúng hoặc sai khi chưa có bằng chứng.
Không bịa nguồn xác thực.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text, None

    except Exception as e:
        return None, str(e)


# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:18px 5px;">
        <div style="font-size:48px;">🌌</div>
        <div style="font-size:21px;font-weight:800;color:#FFFFFF;">
            SOCIAL SANDBOX
        </div>
        <div style="font-size:11px;color:#CADCFC;letter-spacing:2px;">
            DIGITAL LITERACY LAB
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    menu = st.radio(
        "ĐIỀU HƯỚNG",
        [
            "🏠 Tổng quan",
            "🔍 Phân tích thông tin bằng AI",
            "🛡️ Phòng kiểm chứng",
            "🎭 Mô phỏng mạng xã hội",
            "🧠 Phản hồi thích ứng",
            "📊 Thống kê nghiên cứu"
        ]
    )

    st.divider()

    st.markdown("""
    <div style="text-align:center;color:#CADCFC;font-size:12px;">
        <b>VERSION 2.2</b><br>
        Educational Research Project<br>
        Think Before You Share
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 7. OVERVIEW
# =====================================================

if menu == "🏠 Tổng quan":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">🌌 SOCIAL SANDBOX AI</div>
        <div class="hero-description">
            DIGITAL LITERACY LAB<br>
            Hệ thống mô phỏng và hỗ trợ học sinh trung học
            nhận diện dấu hiệu rủi ro trong thông tin số.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✦ Chào mừng đến với Social Sandbox AI")

    st.markdown("""
    <div class="glass-card">
        <h3>🎯 Mục tiêu dự án</h3>
        <p>
        Nghiên cứu hành vi xác thực thông tin số của học sinh trung học
        và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.
        </p>
        <p>
        Hệ thống giúp người dùng rèn luyện tư duy phản biện,
        nhận diện dấu hiệu đáng ngờ và hình thành thói quen
        kiểm chứng thông tin trước khi chia sẻ.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✦ Tổng quan hoạt động")

    a, b, c = st.columns(3)

    a.metric("Lượt phân tích", st.session_state.analysis_count)
    b.metric("Lượt kiểm chứng", st.session_state.verified_count)
    c.metric("Lượt phản hồi", st.session_state.reflection_count)

    st.markdown("## ✦ Các chức năng")

    features = [
        ("🔍", "Phân tích thông tin bằng AI", "Phân tích nội dung và nhận diện dấu hiệu rủi ro."),
        ("🛡️", "Phòng kiểm chứng", "Hướng dẫn các bước xác minh thông tin."),
        ("🎭", "Mô phỏng mạng xã hội", "Thực hành xử lý tình huống giả định."),
        ("🧠", "Phản hồi thích ứng", "Đưa ra gợi ý rèn luyện tư duy phản biện."),
        ("📊", "Thống kê nghiên cứu", "Theo dõi dữ liệu hoạt động.")
    ]

    for icon, title, description in features:
        st.markdown(f"""
        <div class="glass-card">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 Think Before You Share – Suy nghĩ trước khi chia sẻ.")


# =====================================================
# 8. AI ANALYSIS
# =====================================================

elif menu == "🔍 Phân tích thông tin bằng AI":

    st.markdown("# 🔍 Phân tích thông tin bằng AI")

    st.markdown(
        '<p class="subtitle">DIGITAL CONTENT RISK ANALYSIS</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>📡 Hệ thống phân tích nội dung</h3>
        <p>Nhập bài đăng, tin nhắn hoặc thông tin cần kiểm tra.</p>
    </div>
    """, unsafe_allow_html=True)

    content = st.text_area(
        "📄 Nội dung cần phân tích:",
        height=200,
        placeholder="Dán nội dung vào đây..."
    )

    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", use_container_width=True):

        if len(content.strip()) < 10:
            st.warning("Vui lòng nhập nội dung dài hơn.")
        else:

            with st.spinner("Đang phân tích..."):
                score, level, found, advice = basic_analysis(content)
                ai_result, error = gemini_analysis(content)

            st.session_state.analysis_count += 1

            st.session_state.records.append({
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Hoạt động": "Phân tích thông tin",
                "Điểm dấu hiệu": score,
                "Kết quả": level
            })

            st.markdown("---")
            st.markdown("## ✦ KẾT QUẢ")

            c1, c2 = st.columns(2)
            c1.metric("Điểm dấu hiệu", f"{score}/100")
            c2.metric("Mức đánh giá", level)

            st.caption("Điểm số là chỉ báo dựa trên nhóm từ khóa, không phải xác suất tin giả.")
            st.progress(score / 100)

            st.markdown("### 🧩 Dấu hiệu phát hiện")

            if found:
                for item in found:
                    st.warning(
                        f'**{item["category"]}**: '
                        + ", ".join(item["keywords"])
                    )
            else:
                st.success("Chưa phát hiện nhóm từ khóa cảnh báo.")

            st.markdown("### 💡 Khuyến nghị")
            st.info(advice)

            st.markdown("### 🤖 Kết quả Gemini AI")

            if ai_result:
                st.markdown(ai_result)
            else:
                st.warning(f"Gemini chưa hoạt động: {error}")

            st.caption("AI có thể mắc lỗi. Hãy kiểm chứng bằng nguồn độc lập.")


# =====================================================
# 9. VERIFICATION ROOM
# =====================================================

elif menu == "🛡️ Phòng kiểm chứng":

    st.markdown("# 🛡️ Phòng kiểm chứng")

    st.markdown("""
    <div class="glass-card">
        <h3>🔎 QUY TRÌNH 5 BƯỚC</h3>
        <p>Thực hiện các bước sau trước khi tin tưởng hoặc chia sẻ thông tin.</p>
    </div>
    """, unsafe_allow_html=True)

    checklist = [
        "Kiểm tra người đăng và nguồn thông tin.",
        "Kiểm tra thời gian và bối cảnh.",
        "Đối chiếu với các nguồn độc lập.",
        "Kiểm tra hình ảnh, video và bằng chứng.",
        "Đánh giá lại trước khi chia sẻ."
    ]

    checked = []

    for i, item in enumerate(checklist):
        checked.append(
            st.checkbox(f"BƯỚC {i+1}: {item}", key=f"check_{i}")
        )

    completed = sum(checked)

    st.progress(completed / 5)
    st.write(f"Tiến độ: {completed}/5")

    if completed == 5:
        st.success("🎉 Đã hoàn thành quy trình!")

    if st.button("GHI NHẬN KẾT QUẢ"):
        if completed == 5:
            st.session_state.verified_count += 1

            st.session_state.records.append({
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Hoạt động": "Kiểm chứng",
                "Điểm dấu hiệu": 0,
                "Kết quả": "Hoàn thành"
            })

            st.success("Đã ghi nhận!")
        else:
            st.warning("Hãy hoàn thành đủ 5 bước.")

    st.markdown("---")
    st.markdown("### 🌐 Nguồn tham khảo")

    st.markdown("""
    - [Google Fact Check Explorer](https://toolbox.google.com/factcheck/explorer)
    - [WHO](https://www.who.int/)
    - [UNESCO](https://www.unesco.org/)
    """)


# =====================================================
# 10. SOCIAL MEDIA SIMULATION
# =====================================================

elif menu == "🎭 Mô phỏng mạng xã hội":

    st.markdown("# 🎭 Mô phỏng mạng xã hội")

    scenarios = [
        {
            "title": "Tin nhắn khẩn cấp",
            "content": "Một bài đăng nói rằng một sự kiện nguy hiểm sắp xảy ra và yêu cầu chia sẻ ngay. Bài đăng không có nguồn cụ thể.",
            "question": "Em sẽ làm gì?",
            "options": [
                "Chia sẻ ngay.",
                "Kiểm tra nguồn và thông tin chính thức.",
                "Tin vì có nhiều lượt chia sẻ."
            ],
            "correct": 1,
            "explanation": "Cần kiểm tra nguồn và đối chiếu thông tin từ cơ quan đáng tin cậy."
        },
        {
            "title": "Hình ảnh gây tranh cãi",
            "content": "Một hình ảnh được lan truyền với chú thích gây sốc nhưng không có nguồn gốc.",
            "question": "Em nên làm gì?",
            "options": [
                "Tin chú thích.",
                "Chia sẻ ngay.",
                "Tìm nguồn gốc và kiểm tra bối cảnh."
            ],
            "correct": 2,
            "explanation": "Hình ảnh có thể bị sử dụng sai bối cảnh."
        },
        {
            "title": "Thông tin từ người nổi tiếng",
            "content": "Một tài khoản có nhiều người theo dõi đăng thông tin nhưng không đưa bằng chứng.",
            "question": "Lượt theo dõi cao có chứng minh thông tin đúng không?",
            "options": [
                "Có.",
                "Không, cần kiểm tra bằng chứng.",
                "Có nếu nhiều người đồng ý."
            ],
            "correct": 1,
            "explanation": "Độ nổi tiếng không thay thế bằng chứng xác thực."
        }
    ]

    selected = st.selectbox(
        "Chọn tình huống:",
        [s["title"] for s in scenarios]
    )

    scenario = next(s for s in scenarios if s["title"] == selected)

    st.markdown(f"""
    <div class="glass-card">
        <h3>📢 {scenario["title"]}</h3>
        <p>{scenario["content"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### ❓ {scenario['question']}")

    answer = st.radio(
        "Lựa chọn của em:",
        scenario["options"],
        key=f"answer_{selected}"
    )

    if st.button("GỬI LỰA CHỌN"):

        index = scenario["options"].index(answer)
        correct = index == scenario["correct"]

        if correct:
            st.success("🎉 Chính xác!")
        else:
            st.warning("Chưa chính xác, hãy thử suy nghĩ lại.")

        st.info(scenario["explanation"])

        st.session_state.scenario_done += 1

        st.session_state.records.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Hoạt động": "Mô phỏng",
            "Điểm dấu hiệu": 100 if correct else 0,
            "Kết quả": "Đúng" if correct else "Cần cải thiện"
        })


# =====================================================
# 11. ADAPTIVE FEEDBACK
# =====================================================

elif menu == "🧠 Phản hồi thích ứng":

    st.markdown("# 🧠 Phản hồi thích ứng")

    st.markdown("""
    <div class="glass-card">
        <h3>💭 ADAPTIVE FEEDBACK ENGINE</h3>
        <p>
        Đánh giá thói quen tiếp nhận thông tin và nhận phản hồi
        nhằm rèn luyện tư duy phản biện.
        </p>
    </div>
    """, unsafe_allow_html=True)

    q1 = st.radio(
        "1. Khi gặp thông tin gây sốc, em thường:",
        [
            "Chia sẻ ngay",
            "Đọc bình luận",
            "Kiểm tra nguồn trước khi tin"
        ]
    )

    q2 = st.radio(
        "2. Khi một thông tin được nhiều người chia sẻ:",
        [
            "Chắc chắn là đúng",
            "Cần kiểm chứng thêm",
            "Không cần quan tâm nguồn"
        ]
    )

    q3 = st.radio(
        "3. Nếu phát hiện đã chia sẻ thông tin chưa chính xác:",
        [
            "Bỏ qua",
            "Đính chính thông tin",
            "Tiếp tục chia sẻ"
        ]
    )

    if st.button("📩 NHẬN PHẢN HỒI", use_container_width=True):

        score = sum([
            q1 == "Kiểm tra nguồn trước khi tin",
            q2 == "Cần kiểm chứng thêm",
            q3 == "Đính chính thông tin"
        ])

        st.session_state.reflection_count += 1

        st.session_state.records.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Hoạt động": "Tự đánh giá",
            "Điểm dấu hiệu": score,
            "Kết quả": f"{score}/3"
        })

        st.metric("Số lựa chọn phù hợp", f"{score}/3")

        if score == 3:
            st.success("🌟 Rất tốt! Em đã có thói quen tiếp nhận thông tin có trách nhiệm.")
        elif score == 2:
            st.info("💡 Em đã có nền tảng tốt. Hãy tiếp tục kiểm chứng nguồn.")
        else:
            st.warning("🔎 Em nên rèn luyện thêm kỹ năng kiểm chứng.")

        st.markdown("### 💬 Câu hỏi suy ngẫm")

        st.write(
            "Nếu một thông tin khiến em tức giận hoặc lo lắng, "
            "em có nên chia sẻ ngay không? Vì sao?"
        )


# =====================================================
# 12. RESEARCH STATISTICS
# =====================================================

elif menu == "📊 Thống kê nghiên cứu":

    st.markdown("# 📊 Thống kê nghiên cứu")

    st.markdown("""
    <div class="glass-card">
        <h3>📈 RESEARCH DATA ANALYTICS</h3>
        <p>Theo dõi hoạt động của hệ thống trong phiên sử dụng hiện tại.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c, d = st.columns(4)

    a.metric("Phân tích", st.session_state.analysis_count)
    b.metric("Kiểm chứng", st.session_state.verified_count)
    c.metric("Phản hồi", st.session_state.reflection_count)
    d.metric("Mô phỏng", st.session_state.scenario_done)

    st.markdown("---")
    st.markdown("## ✦ Dữ liệu hoạt động")

    if st.session_state.records:

        df = pd.DataFrame(st.session_state.records)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("## ✦ Biểu đồ hoạt động")

        chart = df["Hoạt động"].value_counts()
        st.bar_chart(chart)

        csv = df.to_csv(index=False, encoding="utf-8-sig")

        st.download_button(
            "⬇️ TẢI DỮ LIỆU CSV",
            data=csv,
            file_name="social_sandbox_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("Chưa có dữ liệu. Hãy trải nghiệm các chức năng trước nhé.")

    st.caption(
        "Dữ liệu hiện chỉ lưu trong phiên sử dụng, "
        "chưa được lưu trữ lâu dài."
    )


# =====================================================
# 13. FOOTER
# =====================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    padding:25px;
    color:#CADCFC;
    font-size:12px;
">
    <div style="font-size:28px;">🌌</div>
    <b style="color:#FFFFFF;">SOCIAL SANDBOX AI</b><br>
    DIGITAL LITERACY LAB<br><br>
    THINK BEFORE YOU SHARE<br>
    EDUCATIONAL RESEARCH PROJECT • VERSION 2.2
</div>
""", unsafe_allow_html=True)
