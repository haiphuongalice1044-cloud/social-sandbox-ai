
import streamlit as st
import pandas as pd
import re
import json
from datetime import datetime

# =========================================================
# 1. CẤU HÌNH ỨNG DỤNG
# =========================================================

st.set_page_config(
    page_title="Social Sandbox AI | Digital Learning",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

NAVY = "#00246B"
ICE = "#CADCFC"
WHITE = "#FFFFFF"
BLACK = "#000000"
LIGHT = "#F3F7FF"
RED = "#D62828"
GREEN = "#16834A"
GOLD = "#F0B429"

# =========================================================
# 2. CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>

/* NỀN TOÀN ỨNG DỤNG */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(202,220,252,0.13), transparent 25%),
        radial-gradient(circle at 85% 80%, rgba(202,220,252,0.12), transparent 25%),
        linear-gradient(135deg, #001746, #00246B, #00143D);
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
}

/* KHU VỰC CHÍNH */
.main .block-container {
    padding: 2rem 2.5rem 3rem 2.5rem;
    max-width: 1450px;
}

/* CHỮ BÊN NGOÀI KHUNG */
.stApp p,
.stApp label,
.stApp li,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp .stMarkdown,
.stApp .stCaption,
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stMetricDelta"] {
    color: #FFFFFF;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #CADCFC, #FFFFFF);
}

section[data-testid="stSidebar"] * {
    color: #000000 !important;
}

section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    font-weight: 600;
}

/* TIÊU ĐỀ */
.main-title {
    font-size: 38px;
    font-weight: 850;
    color: #FFFFFF;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 15px;
    color: #CADCFC;
    margin-bottom: 25px;
}

.section-title {
    color: #FFFFFF;
    font-size: 25px;
    font-weight: 800;
    margin-top: 12px;
    margin-bottom: 15px;
}

/* THẺ SÁNG */
.light-card {
    background: linear-gradient(145deg, #FFFFFF, #EDF4FF);
    border: 1px solid rgba(202,220,252,0.8);
    border-radius: 18px;
    padding: 22px;
    margin: 12px 0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.16);
    color: #000000 !important;
}

.light-card * {
    color: #000000 !important;
}

.card-heading {
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* HERO */
.hero {
    background: linear-gradient(120deg, #FFFFFF, #CADCFC);
    border-radius: 22px;
    padding: 30px;
    color: #000000;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.hero * {
    color: #000000 !important;
}

/* NÚT */
.stButton > button {
    background: linear-gradient(120deg, #CADCFC, #FFFFFF);
    color: #00246B !important;
    border: 1px solid #CADCFC;
    border-radius: 12px;
    font-weight: 750;
    padding: 10px 20px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    background: #FFFFFF;
    border-color: #FFFFFF;
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(202,220,252,0.35);
}

/* INPUT */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"],
.stNumberInput input {
    background: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #555555 !important;
}

/* DROPDOWN */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[data-testid="stSelectboxVirtualDropdown"] {
    background: #FFFFFF !important;
}

div[data-baseweb="popover"] * {
    color: #000000 !important;
}

/* RADIO VÀ CHECKBOX */
.stRadio label,
.stCheckbox label {
    color: #FFFFFF !important;
}

/* METRIC */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #FFFFFF, #EAF1FF);
    border-radius: 15px;
    padding: 18px;
    border: 1px solid #CADCFC;
}

[data-testid="stMetric"] * {
    color: #00246B !important;
}

/* ALERT */
.stAlert {
    background: #FFFFFF !important;
    border-radius: 12px;
}

.stAlert * {
    color: #000000 !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 5px;
}

/* PROGRESS */
.stProgress > div > div > div {
    background: #CADCFC;
}

/* DIVIDER */
hr {
    border-color: rgba(202,220,252,0.35);
}

/* FOOTER */
.footer {
    text-align: center;
    color: #CADCFC;
    font-size: 12px;
    padding: 25px 0 10px 0;
}

/* BADGE */
.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 30px;
    background: #CADCFC;
    color: #00246B;
    font-weight: 750;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. KHỞI TẠO DỮ LIỆU
# =========================================================

defaults = {
    "records": [],
    "analysis_count": 0,
    "verified_count": 0,
    "reflection_count": 0,
    "scenario_done": 0,
    "quiz_answers": {}
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# 4. CÁC HÀM HỖ TRỢ
# =========================================================

def show_card(title, content):
    st.markdown(
        f"""
        <div class="light-card">
            <div class="card-heading">{title}</div>
            <div>{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def rule_based_analysis(content):
    categories = {
        "Ngôn ngữ giật gân": [
            "sốc", "kinh hoàng", "chấn động", "không thể tin",
            "gây sốc", "bí mật động trời"
        ],
        "Thúc giục chia sẻ": [
            "chia sẻ ngay", "share ngay", "gửi cho mọi người",
            "lan truyền", "đừng bỏ lỡ"
        ],
        "Nguồn không rõ ràng": [
            "nghe nói", "người ta bảo", "theo nguồn tin",
            "có người nói", "tin nội bộ"
        ],
        "Khẳng định tuyệt đối": [
            "100% đúng", "chắc chắn", "không bao giờ sai",
            "tất cả đều", "hoàn toàn đúng"
        ],
        "Tạo áp lực và sợ hãi": [
            "nguy hiểm", "khẩn cấp", "nếu không sẽ",
            "cảnh báo ngay", "sắp bị"
        ]
    }

    detected = []

    text = content.lower()

    for category, keywords in categories.items():
        found = [word for word in keywords if word in text]
        if found:
            detected.append({
                "category": category,
                "keywords": found
            })

    score = min(len(detected) * 20, 100)

    return score, detected


def get_risk_label(score):
    if score >= 60:
        return "Nhiều dấu hiệu cần kiểm tra", RED
    elif score >= 20:
        return "Có dấu hiệu cần chú ý", GOLD
    else:
        return "Ít dấu hiệu theo bộ lọc từ khóa", GREEN


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
Bạn là trợ lý giáo dục về năng lực số dành cho học sinh trung học.

Hãy phân tích nội dung sau theo hướng giáo dục tư duy phản biện.

NỘI DUNG:
{content}

Yêu cầu trả lời bằng tiếng Việt, dễ hiểu, gồm:

1. Tóm tắt nội dung.
2. Những dấu hiệu đáng chú ý.
3. Đánh giá mức độ rõ ràng của nguồn thông tin.
4. Những thông tin cần được kiểm chứng thêm.
5. Ba câu hỏi tư duy phản biện dành cho học sinh.
6. Khuyến nghị trước khi chia sẻ.

Lưu ý:
- Không tự khẳng định thông tin là thật hoặc giả khi chưa có bằng chứng.
- Không tự tạo nguồn tham khảo.
- Phân biệt rõ dấu hiệu nghi vấn và bằng chứng xác thực.
- Dùng ngôn ngữ phù hợp với học sinh.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text, None

    except Exception as error:
        return None, f"Lỗi kết nối AI: {error}"


def save_record(content, score, result_type):
    st.session_state.records.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Nội dung": content[:150],
        "Điểm dấu hiệu": score,
        "Hoạt động": result_type
    })


# =========================================================
# 5. SIDEBAR - ĐIỀU HƯỚNG
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:15px 5px;">
            <div style="font-size:42px;">🌐</div>
            <div style="font-size:22px;font-weight:900;">
                SOCIAL SANDBOX
            </div>
            <div style="font-size:12px;">
                DIGITAL LEARNING PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
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

    st.markdown("### 🎓 Đối tượng sử dụng")
    st.caption("Học sinh trung học")

    st.markdown("### 💡 Mục tiêu")
    st.caption(
        "Phát triển năng lực xác thực thông tin, "
        "tư duy phản biện và trách nhiệm số."
    )

    st.divider()
    st.caption("SOCIAL SANDBOX AI • VERSION 2.0")


# =========================================================
# 6. HEADER CHUNG
# =========================================================

st.markdown(
    """
    <div class="main-title">
        SOCIAL SANDBOX AI
    </div>
    <div class="subtitle">
        NỀN TẢNG GIÁO DỤC NĂNG LỰC SỐ VÀ XÁC THỰC THÔNG TIN
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TRANG 1: TỔNG QUAN
# =========================================================

if page == "🏠 Tổng quan":

    st.markdown("""
    <div class="hero">
        <div style="font-size:14px;font-weight:800;">
            DIGITAL LITERACY LAB
        </div>
        <h1 style="font-size:34px;margin:12px 0;">
            Học cách kiểm chứng trước khi chia sẻ
        </h1>
        <p style="font-size:16px;">
            Một môi trường học tập mô phỏng giúp học sinh
            nhận diện dấu hiệu bất thường, đánh giá nguồn tin
            và hình thành thói quen sử dụng thông tin có trách nhiệm.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">📌 Tổng quan hoạt động</div>',
                unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Lượt phân tích", st.session_state.analysis_count)

    with c2:
        st.metric("Lượt kiểm chứng", st.session_state.verified_count)

    with c3:
        st.metric("Lượt phản hồi", st.session_state.reflection_count)

    with c4:
        st.metric("Kịch bản hoàn thành", st.session_state.scenario_done)

    st.markdown('<div class="section-title">🎯 Mục tiêu học tập</div>',
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        show_card(
            "🔎 Nhận diện thông tin",
            "Nhận biết ngôn ngữ giật gân, nguồn tin chưa rõ "
            "và những dấu hiệu cần được kiểm tra."
        )

        show_card(
            "🧠 Tư duy phản biện",
            "Biết đặt câu hỏi, đối chiếu bằng chứng "
            "và không vội tin vào thông tin trên mạng."
        )

    with col2:
        show_card(
            "🛡️ An toàn số",
            "Hình thành thói quen sử dụng và chia sẻ "
            "thông tin có trách nhiệm."
        )

        show_card(
            "📚 Học tập chủ động",
            "Tự đánh giá, tiếp nhận phản hồi và cải thiện "
            "năng lực xác thực thông tin."
        )

    st.markdown('<div class="section-title">🚀 Bắt đầu học tập</div>',
                unsafe_allow_html=True)

    st.info(
        "Hãy chọn một chức năng ở thanh điều hướng bên trái "
        "để bắt đầu trải nghiệm Social Sandbox AI."
    )

# =========================================================
# TRANG 2: PHÂN TÍCH THÔNG TIN BẰNG AI
# =========================================================

elif page == "🔍 Phân tích thông tin bằng AI":

    st.markdown('<div class="section-title">🔍 Phân tích thông tin</div>',
                unsafe_allow_html=True)

    show_card(
        "Hướng dẫn",
        "Dán một bài viết, thông báo hoặc nội dung trên mạng xã hội. "
        "Hệ thống sẽ nhận diện dấu hiệu cần chú ý và sử dụng Gemini "
        "để hỗ trợ phân tích."
    )

    content = st.text_area(
        "NỘI DUNG CẦN PHÂN TÍCH",
        height=220,
        placeholder="Dán nội dung thông tin vào đây..."
    )

    st.caption(
        "Ví dụ: Một bài viết có tiêu đề gây sốc, yêu cầu chia sẻ ngay "
        "nhưng không ghi rõ nguồn."
    )

    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", use_container_width=True):

        if len(content.strip()) < 10:
            st.warning("Vui lòng nhập nội dung dài hơn để phân tích.")

        else:
            st.session_state.analysis_count += 1

            with st.spinner("Đang phân tích nội dung..."):

                score, detected = rule_based_analysis(content)

                st.markdown(
                    '<div class="section-title">📊 Kết quả nhận diện dấu hiệu</div>',
                    unsafe_allow_html=True
                )

                label, color = get_risk_label(score)

                st.markdown(
                    f"""
                    <div class="light-card">
                        <div style="font-size:17px;font-weight:800;">
                            Điểm dấu hiệu theo bộ lọc từ khóa
                        </div>
                        <div style="font-size:42px;font-weight:900;color:{color};">
                            {score}/100
                        </div>
                        <div style="font-weight:800;">{label}</div>
                        <p style="margin-top:10px;">
                            Đây là chỉ số heuristic dựa trên từ khóa,
                            không phải xác suất thông tin sai lệch.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if detected:
                    st.markdown("### Các dấu hiệu được phát hiện")

                    for item in detected:
                        words = ", ".join(item["keywords"])

                        show_card(
                            item["category"],
                            f"Từ khóa liên quan: {words}"
                        )
                else:
                    st.info(
                        "Bộ lọc chưa phát hiện từ khóa thuộc các nhóm "
                        "đã thiết lập. Điều này không chứng minh nội dung là đúng."
                    )

                st.markdown("### 🤖 Phân tích bằng Gemini AI")

                ai_result, ai_error = gemini_analysis(content)

                if ai_result:
                    show_card("Kết quả phân tích AI", ai_result)
                else:
                    st.warning(ai_error)
                    st.caption(
                        "Em vẫn có thể sử dụng kết quả nhận diện từ khóa "
                        "trong khi chưa cấu hình Gemini."
                    )

                save_record(content, score, "Phân tích AI")

                st.success("Đã hoàn thành lượt phân tích.")

    st.markdown("---")
    st.caption(
        "Lưu ý: Công cụ hỗ trợ học tập và tư duy phản biện, "
        "không thay thế việc kiểm chứng bằng nguồn đáng tin cậy."
    )

# =========================================================
# TRANG 3: PHÒNG KIỂM CHỨNG
# =========================================================

elif page == "🛡️ Phòng kiểm chứng":

    st.markdown('<div class="section-title">🛡️ Phòng kiểm chứng thông tin</div>',
                unsafe_allow_html=True)

    show_card(
        "Nhiệm vụ",
        "Thực hiện quy trình 5 bước trước khi tin tưởng "
        "hoặc chia sẻ một thông tin trên môi trường số."
    )

    steps = [
        "Xác định nguồn đăng tải thông tin.",
        "Kiểm tra tác giả hoặc đơn vị chịu trách nhiệm.",
        "Tìm bằng chứng và dữ liệu hỗ trợ.",
        "Đối chiếu với nguồn độc lập, đáng tin cậy.",
        "Đánh giá lại trước khi bình luận hoặc chia sẻ."
    ]

    st.markdown("### 📋 Danh sách kiểm chứng")

    checked = []

    for i, step in enumerate(steps):
        value = st.checkbox(
            f"Bước {i+1}: {step}",
            key=f"verify_{i}"
        )
        checked.append(value)

    progress = sum(checked) / len(steps)

    st.progress(progress)

    st.markdown(
        f"**Tiến độ hoàn thành: {sum(checked)}/{len(steps)} bước**"
    )

    if st.button("✅ HOÀN THÀNH KIỂM CHỨNG",
                 use_container_width=True):

        if all(checked):
            st.session_state.verified_count += 1
            st.success(
                "Em đã hoàn thành đầy đủ quy trình kiểm chứng!"
            )
            show_card(
                "Kết luận học tập",
                "Em đã thực hiện đủ các bước kiểm tra. "
                "Hãy lưu lại bằng chứng và chỉ chia sẻ khi có căn cứ phù hợp."
            )
        else:
            st.warning(
                "Em hãy hoàn thành các bước còn lại trước khi kết thúc."
            )

    st.markdown("---")

    show_card(
        "💡 Ghi nhớ",
        "Một thông tin có nhiều lượt chia sẻ không đồng nghĩa "
        "với việc thông tin đó chính xác."
    )

# =========================================================
# TRANG 4: MÔ PHỎNG MẠNG XÃ HỘI
# =========================================================

elif page == "🎭 Mô phỏng mạng xã hội":

    st.markdown('<div class="section-title">🎭 Mô phỏng mạng xã hội</div>',
                unsafe_allow_html=True)

    show_card(
        "Thử thách tình huống",
        "Đọc tình huống dưới đây và lựa chọn cách xử lý phù hợp. "
        "Đây là môi trường mô phỏng phục vụ học tập."
    )

    scenario = st.selectbox(
        "CHỌN TÌNH HUỐNG",
        [
            "Bài đăng không rõ nguồn",
            "Thông tin giật gân",
            "Lời kêu gọi chia sẻ khẩn cấp",
            "Hình ảnh chưa rõ bối cảnh"
        ]
    )

    scenarios = {
        "Bài đăng không rõ nguồn": {
            "content": "Một tài khoản đăng thông tin quan trọng nhưng không dẫn nguồn.",
            "question": "Em sẽ làm gì trước khi tin hoặc chia sẻ?"
        },
        "Thông tin giật gân": {
            "content": "Một bài viết sử dụng tiêu đề gây sốc để thu hút lượt xem.",
            "question": "Em cần chú ý điều gì trong trường hợp này?"
        },
        "Lời kêu gọi chia sẻ khẩn cấp": {
            "content": "Một bài đăng yêu cầu mọi người chia sẻ ngay lập tức.",
            "question": "Em nên phản ứng như thế nào?"
        },
        "Hình ảnh chưa rõ bối cảnh": {
            "content": "Một hình ảnh được đăng lại nhưng không có thời gian và địa điểm.",
            "question": "Em cần kiểm tra những thông tin nào?"
        }
    }

    current = scenarios[scenario]

    st.markdown(
        f"""
        <div class="light-card">
            <div class="card-heading">📱 Bài đăng mô phỏng</div>
            <p>{current["content"]}</p>
            <hr>
            <b>{current["question"]}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "LỰA CHỌN CỦA EM",
        [
            "Chia sẻ ngay vì nhiều người đang quan tâm.",
            "Tin ngay vì bài viết có nhiều lượt tương tác.",
            "Kiểm tra nguồn và đối chiếu bằng chứng.",
            "Bình luận khẳng định thông tin là đúng."
        ]
    )

    if st.button("GỬI LỰA CHỌN", use_container_width=True):

        st.session_state.scenario_done += 1

        if answer == "Kiểm tra nguồn và đối chiếu bằng chứng.":
            st.success("Chính xác! Đây là lựa chọn có trách nhiệm.")
            show_card(
                "Giải thích",
                "Trước khi chia sẻ, cần xác định nguồn, "
                "tìm bằng chứng và đối chiếu thông tin."
            )
        else:
            st.warning("Em hãy suy nghĩ thêm về lựa chọn của mình.")
            show_card(
                "Gợi ý",
                "Lượt tương tác không phải bằng chứng xác thực. "
                "Hãy kiểm tra nguồn tin trước khi đưa ra kết luận."
            )

# =========================================================
# TRANG 5: PHẢN HỒI THÍCH ỨNG
# =========================================================

elif page == "🧠 Phản hồi thích ứng":

    st.markdown('<div class="section-title">🧠 Phản hồi thích ứng</div>',
                unsafe_allow_html=True)

    show_card(
        "Mục tiêu",
        "Giúp học sinh tự đánh giá cách tiếp nhận thông tin "
        "và lựa chọn hành động phù hợp hơn trong môi trường số."
    )

    question = st.radio(
        "Khi gặp một thông tin chưa rõ nguồn trên mạng, em thường:",
        [
            "Tin ngay nếu nội dung có vẻ hợp lý.",
            "Đọc bình luận để xem mọi người nghĩ gì.",
            "Kiểm tra nguồn và tìm thêm bằng chứng.",
            "Chia sẻ để hỏi ý kiến bạn bè."
        ],
        key="reflection_question"
    )

    reason = st.text_area(
        "Vì sao em chọn cách xử lý đó?",
        placeholder="Hãy viết suy nghĩ của em..."
    )

    if st.button("📩 NHẬN PHẢN HỒI", use_container_width=True):

        st.session_state.reflection_count += 1

        if question == "Kiểm tra nguồn và tìm thêm bằng chứng.":
            show_card(
                "🌟 Phản hồi tích cực",
                "Em đã thể hiện thói quen tiếp nhận thông tin có trách nhiệm. "
                "Hãy tiếp tục đối chiếu nguồn và bằng chứng."
            )
        else:
            show_card(
                "💡 Gợi ý cải thiện",
                "Em nên kiểm tra nguồn đăng tải, tác giả và bằng chứng "
                "trước khi đưa ra kết luận hoặc chia sẻ."
            )

        if reason.strip():
            show_card("Suy nghĩ của em", reason)

        st.success("Đã ghi nhận hoạt động phản hồi.")

    st.markdown("---")

    show_card(
        "Thông điệp",
        "Không cần là người biết mọi thứ. "
        "Điều quan trọng là biết đặt câu hỏi và kiểm tra trước khi tin."
    )

# =========================================================
# TRANG 6: THỐNG KÊ NGHIÊN CỨU
# =========================================================

elif page == "📊 Thống kê nghiên cứu":

    st.markdown('<div class="section-title">📊 Thống kê nghiên cứu</div>',
                unsafe_allow_html=True)

    records = st.session_state.records

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Tổng lượt phân tích", st.session_state.analysis_count)

    with c2:
        st.metric("Tổng lượt kiểm chứng", st.session_state.verified_count)

    with c3:
        st.metric("Tổng lượt phản hồi", st.session_state.reflection_count)

    st.markdown("### 📈 Dữ liệu hoạt động")

    activity_data = pd.DataFrame({
        "Hoạt động": [
            "Phân tích thông tin",
            "Kiểm chứng",
            "Phản hồi thích ứng",
            "Mô phỏng tình huống"
        ],
        "Số lượt": [
            st.session_state.analysis_count,
            st.session_state.verified_count,
            st.session_state.reflection_count,
            st.session_state.scenario_done
        ]
    })

    st.bar_chart(
        activity_data.set_index("Hoạt động")
    )

    st.markdown("### 📋 Lịch sử phân tích")

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(
            index=False,
            encoding="utf-8-sig"
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ TẢI DỮ LIỆU CSV",
            data=csv,
            file_name="social_sandbox_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        show_card(
            "Chưa có dữ liệu",
            "Các hoạt động phân tích sẽ được ghi nhận tại đây "
            "trong phiên sử dụng hiện tại."
        )

    st.markdown("---")

    st.warning(
        "Dữ liệu hiện được lưu trong phiên làm việc Streamlit. "
        "Khi phiên kết thúc hoặc ứng dụng khởi động lại, "
        "dữ liệu có thể không còn. Không sử dụng dữ liệu này "
        "như số liệu nghiên cứu chính thức nếu chưa có quy trình lưu trữ."
    )

# =========================================================
# 7. FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    SOCIAL SANDBOX AI • DIGITAL LITERACY LAB<br>
    Nền tảng hỗ trợ học tập, tư duy phản biện và năng lực số<br>
    Phiên bản thử nghiệm giáo dục
</div>
""", unsafe_allow_html=True)

