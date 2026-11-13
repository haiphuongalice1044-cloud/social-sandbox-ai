
import streamlit as st
import pandas as pd
import re
import random
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH ỨNG DỤNG
# =========================================================

st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY = "#00246B"
SECONDARY = "#CADCFC"

# =========================================================
# 2. CSS - GIAO DIỆN XANH NAVY VŨ TRỤ
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #00246B;
    --secondary: #CADCFC;
    --white: #FFFFFF;
}

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

/* NỀN CHÍNH */
.stApp {
    background:
        radial-gradient(ellipse at 15% 20%, rgba(202,220,252,.17), transparent 35%),
        radial-gradient(ellipse at 85% 75%, rgba(80,130,220,.20), transparent 40%),
        linear-gradient(135deg, #00246B, #00143D, #00246B);
    background-size: 200% 200%;
    animation: backgroundMove 18s ease infinite;
    color: white;
}

@keyframes backgroundMove {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* ẨN HEADER */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent;
}

/* THANH SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #00143D, #00246B);
    border-right: 1px solid rgba(202,220,252,.35);
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

/* TIÊU ĐỀ */
h1, h2, h3 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

p, label, li {
    color: #EAF1FF;
}

/* TIÊU ĐỀ PHỤ */
.subtitle {
    color: #CADCFC;
    font-size: 15px;
    letter-spacing: 1px;
}

/* THẺ KÍNH */
.glass-card {
    background: rgba(202,220,252,.09);
    border: 1px solid rgba(202,220,252,.30);
    border-radius: 18px;
    padding: 22px;
    margin: 10px 0;
    box-shadow: 0 8px 30px rgba(0,0,0,.15);
    backdrop-filter: blur(12px);
    transition: all .3s ease;
}

.glass-card:hover {
    border-color: #CADCFC;
    box-shadow: 0 0 22px rgba(202,220,252,.20);
    transform: translateY(-3px);
}

/* HERO */
.hero {
    padding: 35px 28px;
    border-radius: 24px;
    border: 1px solid rgba(202,220,252,.45);
    background:
        linear-gradient(120deg,
        rgba(202,220,252,.16),
        rgba(0,36,107,.25));
    box-shadow: 0 10px 40px rgba(0,0,0,.20);
    margin-bottom: 25px;
}

.hero-title {
    font-size: clamp(28px, 5vw, 46px);
    font-weight: 800;
    color: white;
    letter-spacing: 1px;
}

.hero-description {
    color: #CADCFC;
    font-size: 16px;
    line-height: 1.8;
}

/* NÚT BẤM */
.stButton > button {
    background: linear-gradient(135deg, #CADCFC, #91B8F5);
    color: #00246B !important;
    border: 1px solid #CADCFC;
    border-radius: 12px;
    font-weight: 700;
    padding: 10px 20px;
    transition: all .25s ease;
}

.stButton > button:hover {
    background: #FFFFFF;
    color: #00246B !important;
    box-shadow: 0 0 20px rgba(202,220,252,.55);
    transform: translateY(-2px);
}

/* Ô NHẬP LIỆU */
.stTextArea textarea,
.stTextInput input {
    background: rgba(202,220,252,.10) !important;
    color: white !important;
    border: 1px solid rgba(202,220,252,.50) !important;
    border-radius: 12px !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #CADCFC !important;
}

/* SELECTBOX */
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(202,220,252,.12);
    border-color: rgba(202,220,252,.45);
    color: white;
}

/* RADIO */
.stRadio label {
    color: #FFFFFF !important;
}

/* METRIC */
[data-testid="stMetric"] {
    background: rgba(202,220,252,.10);
    border: 1px solid rgba(202,220,252,.30);
    padding: 18px;
    border-radius: 16px;
}

[data-testid="stMetricLabel"] {
    color: #CADCFC !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
}

/* THANH TIẾN TRÌNH */
.stProgress > div > div > div > div {
    background-color: #CADCFC;
}

/* ĐƯỜNG KẺ */
hr {
    border-color: rgba(202,220,252,.30);
}

/* HIỆU ỨNG SAO */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    opacity: .45;
    background-image:
        radial-gradient(2px 2px at 10% 20%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 25% 75%, #FFFFFF 50%, transparent 100%),
        radial-gradient(1.5px 1.5px at 45% 35%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 70% 15%, #FFFFFF 50%, transparent 100%),
        radial-gradient(1.5px 1.5px at 85% 65%, #CADCFC 50%, transparent 100%),
        radial-gradient(2px 2px at 95% 35%, #FFFFFF 50%, transparent 100%),
        radial-gradient(1px 1px at 55% 85%, #CADCFC 50%, transparent 100%);
    background-size: 350px 350px;
    animation: starsMove 35s linear infinite;
}

@keyframes starsMove {
    from { transform: translateY(0); }
    to { transform: translateY(-350px); }
}

/* THÔNG BÁO */
div[data-testid="stAlert"] {
    border-radius: 14px;
}

/* LINK */
a {
    color: #CADCFC !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. KHỞI TẠO DỮ LIỆU
# =========================================================

if "records" not in st.session_state:
    st.session_state.records = []

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

if "verified_count" not in st.session_state:
    st.session_state.verified_count = 0

if "reflection_count" not in st.session_state:
    st.session_state.reflection_count = 0

if "scenario_done" not in st.session_state:
    st.session_state.scenario_done = 0

if "pre_score" not in st.session_state:
    st.session_state.pre_score = None

if "post_score" not in st.session_state:
    st.session_state.post_score = None


# =========================================================
# 4. HÀM PHÂN TÍCH CƠ BẢN
# =========================================================

RISK_KEYWORDS = {
    "Ngôn ngữ giật gân": [
        "sốc", "kinh hoàng", "chấn động", "không thể tin",
        "bí mật động trời", "gây sốc"
    ],
    "Thúc giục chia sẻ": [
        "chia sẻ ngay", "share ngay", "gửi cho mọi người",
        "lan truyền", "đừng bỏ lỡ"
    ],
    "Thiếu nguồn rõ ràng": [
        "nghe nói", "người ta bảo", "theo nguồn tin",
        "một người bạn", "tin nội bộ"
    ],
    "Khẳng định tuyệt đối": [
        "100%", "chắc chắn", "tất cả đều", "không bao giờ",
        "luôn luôn", "hoàn toàn đúng"
    ],
    "Tạo áp lực và sợ hãi": [
        "nguy hiểm", "khẩn cấp", "sắp bị", "cảnh báo ngay",
        "nếu không sẽ", "hãy cẩn thận"
    ]
}


def basic_analysis(content):
    found_categories = []

    text = content.lower()

    for category, keywords in RISK_KEYWORDS.items():
        matched = [word for word in keywords if word in text]
        if matched:
            found_categories.append({
                "category": category,
                "keywords": matched
            })

    score = min(len(found_categories) * 20, 100)

    if score >= 60:
        level = "Cần kiểm chứng kỹ"
        advice = "Nội dung có nhiều dấu hiệu cần chú ý. Em nên kiểm tra nguồn và tìm thêm thông tin trước khi chia sẻ."
    elif score >= 20:
        level = "Cần thận trọng"
        advice = "Nội dung có một số dấu hiệu đáng chú ý. Hãy kiểm tra nguồn và đối chiếu với thông tin đáng tin cậy."
    else:
        level = "Ít dấu hiệu cảnh báo"
        advice = "Chưa phát hiện nhiều dấu hiệu rủi ro theo bộ từ khóa cơ bản. Điều này không đồng nghĩa nội dung chắc chắn đúng."

    return {
        "score": score,
        "level": level,
        "categories": found_categories,
        "advice": advice
    }


# =========================================================
# 5. HÀM PHÂN TÍCH GEMINI
# =========================================================

def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def gemini_analysis(content):
    api_key = get_api_key()

    if not api_key:
        return None, "Chưa cấu hình Gemini API Key."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Bạn là trợ lý giáo dục trong dự án Social Sandbox AI,
giúp học sinh trung học rèn luyện kỹ năng xác thực thông tin số.

Hãy phân tích nội dung dưới đây bằng tiếng Việt.

NỘI DUNG:
{content}

Trình bày theo các mục:

1. TÓM TẮT:
Nội dung đang muốn truyền tải điều gì?

2. DẤU HIỆU ĐÁNG CHÚ Ý:
Có ngôn ngữ giật gân, thúc giục chia sẻ,
thiếu nguồn, khẳng định tuyệt đối hay tạo áp lực không?

3. NGUỒN THÔNG TIN:
Nội dung có cung cấp nguồn cụ thể không?
Cần kiểm tra những thông tin nào?

4. CÂU HỎI TƯ DUY:
Đưa ra 3 câu hỏi giúp học sinh suy nghĩ phản biện.

5. KHUYẾN NGHỊ:
Nên làm gì trước khi tin hoặc chia sẻ?

LƯU Ý:
Không tự khẳng định nội dung là thật hoặc giả nếu chưa có bằng chứng.
Không bịa nguồn kiểm chứng.
Đây là phân tích dấu hiệu, không phải kết luận xác thực sự thật.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text, None

    except Exception as e:
        return None, f"Không thể kết nối Gemini: {str(e)}"


# =========================================================
# 6. THANH ĐIỀU HƯỚNG
# =========================================================

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:15px 5px;">
        <div style="font-size:48px;">🌌</div>
        <div style="font-size:22px; font-weight:800; color:#FFFFFF;">
            SOCIAL SANDBOX
        </div>
        <div style="font-size:11px; color:#CADCFC; letter-spacing:2px;">
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
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("""
    <div style="text-align:center; color:#CADCFC; font-size:12px;">
        <b>PHIÊN BẢN 2.0</b><br>
        Educational Research Project<br>
        Think Before You Share
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 7. TRANG TỔNG QUAN
# =========================================================

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

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Lượt phân tích",
            st.session_state.analysis_count
        )

    with col2:
        st.metric(
            "Lượt kiểm chứng",
            st.session_state.verified_count
        )

    with col3:
        st.metric(
            "Lượt phản hồi",
            st.session_state.reflection_count
        )

    st.markdown("## ✦ Sáu khu vực chức năng")

    features = [
        ("🔍", "Phân tích thông tin bằng AI",
         "Phân tích nội dung và nhận diện các dấu hiệu rủi ro."),
        ("🛡️", "Phòng kiểm chứng",
         "Hướng dẫn các bước kiểm tra thông tin."),
        ("🎭", "Mô phỏng mạng xã hội",
         "Thực hành xử lý các tình huống thông tin giả định."),
        ("🧠", "Phản hồi thích ứng",
         "Đưa ra câu hỏi và gợi ý cải thiện tư duy phản biện."),
        ("📊", "Thống kê nghiên cứu",
         "Theo dõi số lượt hoạt động và kết quả khảo sát.")
    ]

    for icon, title, description in features:
        st.markdown(f"""
        <div class="glass-card">
            <h3>{icon} {title}</h3>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 Hãy luôn suy nghĩ và kiểm chứng trước khi chia sẻ bất kỳ thông tin nào.")


# =========================================================
# 8. PHÂN TÍCH THÔNG TIN BẰNG AI
# =========================================================

elif menu == "🔍 Phân tích thông tin bằng AI":

    st.markdown("# 🔍 Phân tích thông tin bằng AI")
    st.markdown(
        '<p class="subtitle">PHÂN TÍCH DẤU HIỆU RỦI RO TRONG NỘI DUNG SỐ</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>📡 Hệ thống phân tích</h3>
        <p>
        Nhập một bài đăng, tin nhắn hoặc nội dung bất kỳ.
        Hệ thống sẽ phân tích các dấu hiệu đáng chú ý
        và đưa ra gợi ý kiểm chứng.
        </p>
    </div>
    """, unsafe_allow_html=True)

    content = st.text_area(
        "📄 Nhập nội dung cần phân tích:",
        height=200,
        placeholder="Dán nội dung bài đăng hoặc tin nhắn vào đây..."
    )

    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", use_container_width=True):

        if len(content.strip()) < 10:
            st.warning("Em hãy nhập nội dung dài hơn để hệ thống phân tích nhé.")
        else:
            with st.spinner("Đang phân tích nội dung..."):

                result = basic_analysis(content)
                ai_result, error = gemini_analysis(content)

                st.session_state.analysis_count += 1

                st.session_state.records.append({
                    "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Loại hoạt động": "Phân tích thông tin",
                    "Điểm dấu hiệu": result["score"],
                    "Mức đánh giá": result["level"]
                })

            st.markdown("---")
            st.markdown("## ✦ KẾT QUẢ PHÂN TÍCH")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Điểm dấu hiệu rủi ro", f'{result["score"]}/100')

            with col2:
                st.metric("Mức đánh giá", result["level"])

            st.caption(
                "Điểm này phản ánh số nhóm dấu hiệu được phát hiện "
                "bởi bộ từ khóa cơ bản, không phải xác suất thông tin giả."
            )

            st.progress(result["score"] / 100)

            st.markdown("### 🧩 Dấu hiệu được phát hiện")

            if result["categories"]:
                for item in result["categories"]:
                    st.warning(
                        f'**{item["category"]}** — Từ khóa: '
                        + ", ".join(item["keywords"])
                    )
            else:
                st.success(
                    "Chưa phát hiện nhóm từ khóa cảnh báo trong nội dung."
                )

            st.markdown("### 💡 Khuyến nghị cơ bản")
            st.info(result["advice"])

            st.markdown("---")
            st.markdown("### 🤖 Phân tích từ Gemini AI")

            if ai_result:
                st.markdown(ai_result)
            else:
                st.warning(error)
                st.caption(
                    "Em vẫn có thể sử dụng kết quả phân tích cơ bản ở phía trên."
                )

            st.caption(
                "Lưu ý: AI có thể mắc lỗi. Cần kiểm chứng bằng nguồn độc lập "
                "trước khi kết luận thông tin đúng hay sai."
            )


# =========================================================
# 9. PHÒNG KIỂM CHỨNG
# =========================================================

elif menu == "🛡️ Phòng kiểm chứng":

    st.markdown("# 🛡️ Phòng kiểm chứng thông tin")
    st.markdown(
        '<p class="subtitle">FIVE STEPS TO VERIFY INFORMATION</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>🔎 Quy trình 5 bước</h3>
        <p>
        Trước khi tin tưởng hoặc chia sẻ một thông tin,
        hãy thực hiện lần lượt các bước dưới đây.
        </p>
    </div>
    """, unsafe_allow_html=True)

    checklist = [
        "Kiểm tra người đăng và nguồn thông tin.",
        "Xem thời gian đăng tải và bối cảnh của thông tin.",
        "Tìm kiếm thông tin tương tự từ các nguồn độc lập.",
        "Kiểm tra hình ảnh, video và bằng chứng đi kèm.",
        "Đánh giá lại nội dung trước khi chia sẻ."
    ]

    st.markdown("## ✦ Danh sách kiểm chứng")

    checked = []

    for i, item in enumerate(checklist):
        value = st.checkbox(
            f"BƯỚC {i + 1}: {item}",
            key=f"verify_{i}"
        )
        checked.append(value)

    completed = sum(checked)
    st.progress(completed / len(checklist))

    st.write(f"**Tiến độ hoàn thành: {completed}/5 bước**")

    if completed == 5:
        st.success("🎉 Em đã hoàn thành quy trình kiểm chứng!")

    if st.button("✅ GHI NHẬN HOÀN THÀNH"):
        if completed == 5:
            st.session_state.verified_count += 1

            st.session_state.records.append({
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Loại hoạt động": "Kiểm chứng thông tin",
                "Điểm dấu hiệu": 0,
                "Mức đánh giá": "Hoàn thành"
            })

            st.success("Đã ghi nhận kết quả kiểm chứng!")
        else:
            st.warning("Em hãy hoàn thành cả 5 bước trước nhé.")

    st.markdown("---")
    st.markdown("## ✦ Một số nguồn tham khảo")

    st.markdown("""
    - [Google Fact Check Explorer](https://toolbox.google.com/factcheck/explorer)
    - [WHO - World Health Organization](https://www.who.int/)
    - [UNESCO](https://www.unesco.org/)
    """)


# =========================================================
# 10. MÔ PHỎNG MẠNG XÃ HỘI
# =========================================================

elif menu == "🎭 Mô phỏng mạng xã hội":

    st.markdown("# 🎭 Mô phỏng mạng xã hội")
    st.markdown(
        '<p class="subtitle">SIMULATED SOCIAL MEDIA ENVIRONMENT</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>📱 Bảng tin mô phỏng</h3>
        <p>
        Em sẽ gặp các tình huống giả định giống với những nội dung
        có thể xuất hiện trên mạng xã hội.
        Hãy lựa chọn cách xử lý phù hợp.
        </p>
    </div>
    """, unsafe_allow_html=True)

    scenarios = [
        {
            "title": "Tin nhắn khẩn cấp",
            "content": "Một bài đăng nói rằng một sự kiện nguy hiểm sắp xảy ra và yêu cầu mọi người chia sẻ ngay lập tức. Bài đăng không dẫn nguồn cụ thể.",
            "question": "Em sẽ làm gì?",
            "options": [
                "Chia sẻ ngay để cảnh báo mọi người.",
                "Kiểm tra nguồn và tìm thông tin từ cơ quan đáng tin cậy.",
                "Tin ngay vì bài đăng có nhiều lượt chia sẻ."
            ],
            "correct": 1,
            "explanation": "Cần kiểm tra nguồn và đối chiếu với thông báo từ cơ quan có thẩm quyền. Lượt chia sẻ không chứng minh thông tin chính xác."
        },
        {
            "title": "Hình ảnh gây tranh cãi",
            "content": "Một hình ảnh đang được lan truyền với chú thích gây sốc. Không có thời gian, địa điểm hoặc nguồn gốc hình ảnh.",
            "question": "Em nên làm gì trước tiên?",
            "options": [
                "Tin vào chú thích của người đăng.",
                "Chia sẻ để hỏi ý kiến bạn bè.",
                "Tìm nguồn gốc hình ảnh và kiểm tra bối cảnh."
            ],
            "correct": 2,
            "explanation": "Hình ảnh có thể bị sử dụng sai bối cảnh. Cần tìm nguồn gốc và thông tin liên quan trước khi kết luận."
        },
        {
            "title": "Thông tin từ người nổi tiếng",
            "content": "Một tài khoản có nhiều người theo dõi đăng thông tin về một vấn đề nhưng không đưa ra bằng chứng.",
            "question": "Lượt theo dõi cao có đủ để chứng minh thông tin đúng không?",
            "options": [
                "Có, vì người nổi tiếng thường đáng tin.",
                "Không, cần kiểm tra bằng chứng và nguồn độc lập.",
                "Có, nếu nhiều người bình luận đồng ý."
            ],
            "correct": 1,
            "explanation": "Độ nổi tiếng và số lượng bình luận không thay thế được bằng chứng xác thực."
        }
    ]

    scenario_names = [s["title"] for s in scenarios]

    selected_scenario = st.selectbox(
        "Chọn tình huống mô phỏng:",
        scenario_names
    )

    scenario = next(
        s for s in scenarios if s["title"] == selected_scenario
    )

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
        key=f"scenario_{selected_scenario}"
    )

    if st.button("GỬI LỰA CHỌN", use_container_width=True):

        answer_index = scenario["options"].index(answer)

        if answer_index == scenario["correct"]:
            st.success("🎉 Chính xác! Em đã lựa chọn cách xử lý phù hợp.")
        else:
            st.warning("Chưa chính xác. Em hãy thử suy nghĩ lại nhé.")

        st.info(scenario["explanation"])

        st.session_state.scenario_done += 1

        st.session_state.records.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Loại hoạt động": "Mô phỏng mạng xã hội",
            "Điểm dấu hiệu": 100 if answer_index == scenario["correct"] else 0,
            "Mức đánh giá": "Trả lời đúng" if answer_index == scenario["correct"] else "Cần cải thiện"
        })


# =========================================================
# 11. PHẢN HỒI THÍCH ỨNG
# =========================================================

elif menu == "🧠 Phản hồi thích ứng":

    st.markdown("# 🧠 Phản hồi thích ứng")
    st.markdown(
        '<p class="subtitle">ADAPTIVE FEEDBACK ENGINE</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>💭 Không chỉ nhận diện, mà còn học cách suy nghĩ</h3>
        <p>
        Khu vực này giúp học sinh tự đánh giá thói quen tiếp nhận thông tin
        và xây dựng cách xử lý phù hợp hơn.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✦ Tự đánh giá hành vi")

    q1 = st.radio(
        "1. Khi gặp một thông tin gây sốc, em thường làm gì?",
        [
            "Chia sẻ ngay",
            "Đọc bình luận trước",
            "Kiểm tra nguồn trước khi tin"
        ]
    )

    q2 = st.radio(
        "2. Nếu một thông tin được nhiều người chia sẻ, em nghĩ gì?",
        [
            "Chắc chắn là đúng",
            "Có thể đúng nhưng cần kiểm chứng",
            "Không cần quan tâm đến nguồn"
        ]
    )

    q3 = st.radio(
        "3. Khi phát hiện mình đã chia sẻ thông tin chưa chính xác, em sẽ:",
        [
            "Bỏ qua",
            "Xóa hoặc đính chính thông tin",
            "Tiếp tục chia sẻ"
        ]
    )

    if st.button("📩 NHẬN PHẢN HỒI", use_container_width=True):

        score = 0

        if q1 == "Kiểm tra nguồn trước khi tin":
            score += 1

        if q2 == "Có thể đúng nhưng cần kiểm chứng":
            score += 1

        if q3 == "Xóa hoặc đính chính thông tin":
            score += 1

        st.session_state.reflection_count += 1

        st.session_state.records.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Loại hoạt động": "Tự đánh giá hành vi",
            "Điểm dấu hiệu": score,
            "Mức đánh giá": f"{score}/3 câu phù hợp"
        })

        st.markdown("---")
        st.markdown("## ✦ Kết quả phản hồi")

        st.metric("Số lựa chọn phù hợp", f"{score}/3")

        if score == 3:
            st.success(
                "🌟 Rất tốt! Em đã thể hiện thói quen tiếp nhận thông tin có trách nhiệm."
            )
        elif score == 2:
            st.info(
                "💡 Em đã có nền tảng tốt. Hãy chú ý kiểm chứng nguồn trước khi chia sẻ."
            )
        else:
            st.warning(
                "🔎 Em nên dành thêm thời gian rèn luyện kỹ năng kiểm chứng và tư duy phản biện."
            )

        st.markdown("### 💬 Câu hỏi suy ngẫm")

        st.write(
            "Nếu một thông tin khiến em rất tức giận hoặc lo lắng, "
            "em có nên chia sẻ ngay không? Vì sao?"
        )

        st.caption(
            "Hãy nhớ: cảm xúc mạnh không phải là bằng chứng cho tính chính xác của thông tin."
        )


# =========================================================
# 12. THỐNG KÊ NGHIÊN CỨU
# =========================================================

elif menu == "📊 Thống kê nghiên cứu":

    st.markdown("# 📊 Thống kê nghiên cứu")
    st.markdown(
        '<p class="subtitle">RESEARCH DATA & ACTIVITY ANALYTICS</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="glass-card">
        <h3>📈 Bảng điều khiển dữ liệu</h3>
        <p>
        Theo dõi số lượt hoạt động được ghi nhận trong phiên sử dụng hiện tại.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Phân tích", st.session_state.analysis_count)

    with col2:
        st.metric("Kiểm chứng", st.session_state.verified_count)

    with col3:
        st.metric("Phản hồi", st.session_state.reflection_count)

    with col4:
        st.metric("Mô phỏng", st.session_state.scenario_done)

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

        activity_counts = (
            df["Loại hoạt động"]
            .value_counts()
            .reset_index()
        )

        activity_counts.columns = ["Hoạt động", "Số lượt"]

        st.bar_chart(
            activity_counts.set_index("Hoạt động")
        )

        csv = df.to_csv(
            index=False,
            encoding="utf-8-sig"
        )

        st.download_button(
            label="⬇️ TẢI DỮ LIỆU NGHIÊN CỨU (CSV)",
            data=csv,
            file_name="social_sandbox_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info(
            "Chưa có dữ liệu. Em hãy trải nghiệm các chức năng "
            "để hệ thống bắt đầu ghi nhận hoạt động."
        )

    st.markdown("---")

    st.caption(
        "Lưu ý: Dữ liệu hiện được lưu trong session của ứng dụng. "
        "Khi phiên sử dụng kết thúc hoặc ứng dụng khởi động lại, "
        "dữ liệu có thể không còn. Đây chưa phải hệ thống lưu trữ lâu dài."
    )


# =========================================================
# 13. CHÂN TRANG
# =========================================================

st.markdown("---")

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    color:#CADCFC;
    font-size:12px;
">
    <div style="font-size:22px;">🌌</div>
    <b>SOCIAL SANDBOX AI</b><br>
    DIGITAL LITERACY LAB<br><br>
    THINK BEFORE YOU SHARE<br>
    <span style="opacity:.7;">
        Educational Research Project • Version 2.0
    </span>
</div>
""", unsafe_allow_html=True)
