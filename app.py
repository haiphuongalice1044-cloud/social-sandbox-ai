
import streamlit as st
import pandas as pd
import re
import random
from datetime import datetime

# =====================================================
# 1. CẤU HÌNH ỨNG DỤNG
# =====================================================

st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. GIAO DIỆN RED COSMIC
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

:root {
    --red: #ff3155;
    --red-light: #ff7189;
    --black: #08070d;
    --panel: rgba(25, 15, 25, 0.88);
}

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 15% 15%, rgba(160,0,45,.30), transparent 40%),
        radial-gradient(ellipse at 85% 80%, rgba(255,25,70,.18), transparent 35%),
        linear-gradient(135deg, #050509, #190711, #08070c);
    background-size: 200% 200%;
    animation: backgroundMove 18s ease infinite;
}

@keyframes backgroundMove {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* BẦU TRỜI SAO */
.starfield {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
    background-image:
        radial-gradient(2px 2px at 20% 30%, white 98%, transparent),
        radial-gradient(1px 1px at 40% 70%, #ff829a 98%, transparent),
        radial-gradient(2px 2px at 70% 20%, white 98%, transparent),
        radial-gradient(1px 1px at 85% 65%, #ff3155 98%, transparent),
        radial-gradient(2px 2px at 55% 45%, white 98%, transparent),
        radial-gradient(1px 1px at 10% 85%, #ff9aab 98%, transparent);
    background-size: 300px 300px;
    animation: stars 70s linear infinite, twinkle 4s ease-in-out infinite alternate;
}

@keyframes stars {
    from { background-position: 0 0; }
    to { background-position: 0 1000px; }
}

@keyframes twinkle {
    from { opacity: .25; }
    to { opacity: .85; }
}

/* TINH VÂN */
.nebula {
    position: fixed;
    width: 550px;
    height: 550px;
    top: 15%;
    left: 25%;
    border-radius: 50%;
    background: radial-gradient(
        circle,
        rgba(220,0,55,.19),
        rgba(120,0,35,.08) 45%,
        transparent 70%
    );
    filter: blur(45px);
    pointer-events: none;
    z-index: 0;
    animation: nebulaMove 24s ease-in-out infinite alternate;
}

@keyframes nebulaMove {
    from { transform: translate(-100px,-60px) scale(.8); }
    to { transform: translate(200px,150px) scale(1.2); }
}

.block-container {
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #100810, #210812);
    border-right: 1px solid rgba(255,50,85,.3);
}

section[data-testid="stSidebar"] * {
    color: #f7eaf0;
}

h1, h2, h3 {
    color: #fff !important;
}

p, label, span {
    color: #e7dce2;
}

.cosmic-card {
    background: rgba(25, 15, 25, .83);
    border: 1px solid rgba(255,60,90,.30);
    border-radius: 20px;
    padding: 23px;
    box-shadow: 0 10px 35px rgba(0,0,0,.3);
    backdrop-filter: blur(12px);
    transition: .3s ease;
    margin-bottom: 15px;
}

.cosmic-card:hover {
    border-color: #ff3155;
    box-shadow: 0 0 25px rgba(255,30,75,.22);
    transform: translateY(-3px);
}

.hero {
    padding: 35px;
    border-radius: 24px;
    border: 1px solid rgba(255,70,100,.4);
    background: linear-gradient(
        120deg,
        rgba(100,0,35,.75),
        rgba(12,8,16,.9),
        rgba(130,0,40,.6)
    );
    box-shadow: 0 0 35px rgba(255,0,55,.13);
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 40px;
    font-weight: 800;
    letter-spacing: 1px;
}

.hero p {
    color: #e7cbd4;
}

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

.stTextArea textarea,
.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    background: rgba(10,8,15,.9) !important;
    color: white !important;
    border: 1px solid rgba(255,70,100,.4) !important;
    border-radius: 12px !important;
}

.stTabs [aria-selected="true"] {
    color: #ff7189 !important;
}

div[data-testid="stMetric"] {
    background: rgba(35,15,27,.8);
    border: 1px solid rgba(255,60,90,.3);
    padding: 18px;
    border-radius: 16px;
}

div[data-testid="stMetricValue"] {
    color: #ff7189;
}

.stProgress > div > div > div {
    background: #ff3155;
}

hr {
    border-color: rgba(255,60,90,.25);
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        animation-iteration-count: 1 !important;
    }
}
</style>

<div class="starfield"></div>
<div class="nebula"></div>
""", unsafe_allow_html=True)

# =====================================================
# 3. KHỞI TẠO DỮ LIỆU
# =====================================================

if "records" not in st.session_state:
    st.session_state.records = []

if "verified_count" not in st.session_state:
    st.session_state.verified_count = 0

if "reflection_count" not in st.session_state:
    st.session_state.reflection_count = 0

if "pre_score" not in st.session_state:
    st.session_state.pre_score = None

if "post_score" not in st.session_state:
    st.session_state.post_score = None

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

# =====================================================
# 4. HÀM PHÂN TÍCH NỘI DUNG
# =====================================================

def analyze_content(content):
    text = content.lower()

    categories = {
        "Ngôn ngữ giật gân": [
            "sốc", "kinh hoàng", "chấn động", "không thể tin",
            "bí mật động trời", "gây sốc"
        ],
        "Thúc giục chia sẻ": [
            "chia sẻ ngay", "gửi cho mọi người", "share ngay",
            "lan truyền", "chuyển tiếp ngay"
        ],
        "Nguồn không rõ ràng": [
            "nghe nói", "người ta nói", "theo nguồn tin",
            "một người bạn", "tin nội bộ"
        ],
        "Khẳng định tuyệt đối": [
            "100%", "chắc chắn", "không bao giờ sai",
            "tất cả đều", "ai cũng biết"
        ],
        "Tạo áp lực và lo sợ": [
            "khẩn cấp", "nguy hiểm", "sắp bị khóa",
            "mất tài khoản", "ngay lập tức"
        ]
    }

    detected = []

    for category, keywords in categories.items():
        found = [word for word in keywords if word in text]
        if found:
            detected.append({
                "category": category,
                "keywords": found
            })

    score = min(len(detected) * 20, 100)

    if score >= 60:
        level = "Cần cảnh giác cao"
        advice = "Nội dung có nhiều dấu hiệu đáng chú ý. Em nên dừng lại và kiểm chứng từ các nguồn độc lập."
    elif score >= 20:
        level = "Cần kiểm tra thêm"
        advice = "Nội dung có một số dấu hiệu cần xem xét. Hãy kiểm tra nguồn và bằng chứng trước khi tin."
    else:
        level = "Ít dấu hiệu được phát hiện"
        advice = "Chưa phát hiện nhiều dấu hiệu trong bộ từ khóa. Điều này không đồng nghĩa nội dung chắc chắn đúng."

    return {
        "score": score,
        "level": level,
        "detected": detected,
        "advice": advice
    }

# =====================================================
# 5. HÀM LƯU LỊCH SỬ
# =====================================================

def save_record(content, result):
    st.session_state.records.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Nội dung": content,
        "Điểm cảnh báo": result["score"],
        "Mức đánh giá": result["level"],
        "Số nhóm dấu hiệu": len(result["detected"])
    })

# =====================================================
# 6. THANH MENU
# =====================================================

st.sidebar.markdown("""
<div style="text-align:center;padding:15px 0;">
    <div style="font-size:42px;">🌌</div>
    <h2 style="color:#ff7189!important;">SOCIAL SANDBOX</h2>
    <p style="font-size:11px;letter-spacing:3px;">DIGITAL LITERACY LAB</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "ĐIỀU HƯỚNG",
    [
        "🏠 Tổng quan",
        "🔍 Phân tích thông tin",
        "🛡️ Phòng kiểm chứng",
        "🎭 Mô phỏng mạng xã hội",
        "🧠 Phản hồi thích ứng",
        "📝 Khảo sát nghiên cứu",
        "📊 Thống kê",
        "ℹ️ Giới thiệu đề tài"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("SOCIAL SANDBOX AI • PROTOTYPE v2.0")
st.sidebar.caption("Think Before You Share.")

# =====================================================
# 7. TRANG TỔNG QUAN
# =====================================================

if page == "🏠 Tổng quan":

    st.markdown("""
    <div class="hero">
        <p style="letter-spacing:5px;font-size:12px;">
            DIGITAL LITERACY LAB
        </p>
        <h1>🌌 SOCIAL SANDBOX AI</h1>
        <p>
            Think Before You Share • Explore • Verify • Protect
        </p>
        <p>
            Không gian mô phỏng và rèn luyện kỹ năng xác thực
            thông tin số dành cho học sinh trung học.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("✨ Tổng quan hệ thống")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Lượt phân tích", st.session_state.analysis_count)

    with c2:
        st.metric("Lượt kiểm chứng", st.session_state.verified_count)

    with c3:
        st.metric("Lượt phản hồi", st.session_state.reflection_count)

    st.markdown("---")

    st.subheader("🚀 Khám phá các chức năng")

    cards = [
        ("🔍", "Phân tích thông tin", "Nhận diện các dấu hiệu đáng ngờ trong nội dung số."),
        ("🛡️", "Phòng kiểm chứng", "Thực hành quy trình kiểm tra thông tin."),
        ("🎭", "Mô phỏng mạng xã hội", "Trải nghiệm các tình huống thông tin giả định."),
        ("🧠", "Phản hồi thích ứng", "Nhận lời khuyên dựa trên dấu hiệu được phát hiện."),
        ("📊", "Thống kê nghiên cứu", "Theo dõi hoạt động và kết quả khảo sát.")
    ]

    cols = st.columns(2)

    for i, item in enumerate(cards):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="cosmic-card">
                <h2>{item[0]} {item[1]}</h2>
                <p>{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.info("💡 Hãy luôn kiểm chứng thông tin trước khi chia sẻ.")

# =====================================================
# 8. TRANG PHÂN TÍCH
# =====================================================

elif page == "🔍 Phân tích thông tin":

    st.title("🔍 Phân tích nội dung số")
    st.write("Nhập một bài đăng, tin nhắn hoặc nội dung cần đánh giá.")

    content = st.text_area(
        "Nội dung cần phân tích",
        height=200,
        placeholder="Dán nội dung cần kiểm tra tại đây..."
    )

    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", use_container_width=True):

        if not content.strip():
            st.warning("Em hãy nhập nội dung trước khi phân tích.")
        else:
            result = analyze_content(content)

            st.session_state.analysis_count += 1
            st.session_state.last_analysis = result
            save_record(content, result)

            st.success("Đã hoàn thành phân tích!")

    result = st.session_state.last_analysis

    if result:

        st.markdown("---")
        st.subheader("📋 Kết quả phân tích")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Điểm cảnh báo", f'{result["score"]}/100')

        with col2:
            st.metric("Mức đánh giá", result["level"])

        st.progress(result["score"] / 100)

        if result["score"] >= 60:
            st.error("⚠️ Cần cảnh giác cao")
        elif result["score"] >= 20:
            st.warning("🔎 Cần kiểm tra thêm")
        else:
            st.success("Chưa phát hiện nhiều dấu hiệu cảnh báo.")

        st.subheader("🔎 Các dấu hiệu được phát hiện")

        if result["detected"]:
            for item in result["detected"]:
                st.markdown(f"""
                <div class="cosmic-card">
                    <h4>⚠️ {item["category"]}</h4>
                    <p>Từ khóa: {", ".join(item["keywords"])}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Chưa phát hiện dấu hiệu thuộc bộ từ khóa hiện tại.")

        st.markdown("### 💡 Gợi ý")
        st.write(result["advice"])

        st.caption(
            "Lưu ý: Điểm cảnh báo là chỉ số mô phỏng dựa trên từ khóa, "
            "không phải xác suất tin giả và không xác nhận nội dung đúng hay sai."
        )

# =====================================================
# 9. PHÒNG KIỂM CHỨNG
# =====================================================

elif page == "🛡️ Phòng kiểm chứng":

    st.title("🛡️ Phòng kiểm chứng thông tin")
    st.write("Thực hiện 5 bước để đánh giá độ tin cậy của một thông tin.")

    checklist = [
        "Kiểm tra tác giả hoặc đơn vị đăng tải.",
        "Kiểm tra ngày đăng và thời điểm sự việc.",
        "Tìm nguồn thông tin gốc.",
        "Đối chiếu với ít nhất một nguồn độc lập đáng tin cậy.",
        "Kiểm tra hình ảnh, số liệu và ngữ cảnh."
    ]

    st.markdown("### 📌 Danh sách kiểm chứng")

    checked = []

    for i, task in enumerate(checklist):
        value = st.checkbox(task, key=f"check_{i}")
        checked.append(value)

    completed = sum(checked)

    st.progress(completed / len(checklist))
    st.write(f"Đã hoàn thành: **{completed}/5 bước**")

    if st.button("✅ HOÀN THÀNH KIỂM CHỨNG"):

        if completed == 5:
            st.session_state.verified_count += 1
            st.success("Tuyệt vời! Em đã hoàn thành quy trình kiểm chứng.")
        else:
            st.warning("Em hãy hoàn thành các bước còn lại.")

    st.markdown("---")
    st.subheader("💭 Tự đánh giá")

    reflection = st.radio(
        "Sau khi kiểm chứng, em sẽ làm gì?",
        [
            "Chia sẻ ngay mà không cần kiểm tra thêm.",
            "Tạm dừng và tìm hiểu thêm.",
            "Đối chiếu với các nguồn đáng tin cậy.",
            "Không chia sẻ khi chưa đủ bằng chứng."
        ]
    )

    if st.button("Gửi lựa chọn"):
        st.session_state.reflection_count += 1
        st.success("Đã ghi nhận lựa chọn của em.")
        st.write("Gợi ý: Nên ưu tiên kiểm tra nguồn và bằng chứng trước khi chia sẻ.")

# =====================================================
# 10. MÔ PHỎNG MẠNG XÃ HỘI
# =====================================================

elif page == "🎭 Mô phỏng mạng xã hội":

    st.title("🎭 Mô phỏng tình huống mạng xã hội")
    st.write("Hãy đọc tình huống và lựa chọn cách xử lý phù hợp.")

    scenarios = {
        "Tình huống 1: Tin nhắn nhận thưởng": {
            "content": "Bạn nhận được thông báo giả định: Bạn đã trúng một phần thưởng. Hãy truy cập đường dẫn lạ và cung cấp thông tin cá nhân để nhận quà.",
            "options": [
                "Truy cập ngay để nhận thưởng.",
                "Chia sẻ cho bạn bè.",
                "Không cung cấp thông tin và kiểm tra đơn vị gửi."
            ],
            "answer": 2,
            "explain": "Yêu cầu cung cấp thông tin cá nhân qua đường dẫn không rõ nguồn là dấu hiệu cần cảnh giác."
        },
        "Tình huống 2: Tin đồn tại trường": {
            "content": "Một bài đăng chưa rõ nguồn nói rằng ngày mai toàn trường được nghỉ học.",
            "options": [
                "Chia sẻ ngay vào nhóm lớp.",
                "Kiểm tra thông báo chính thức của nhà trường.",
                "Tin ngay vì nhiều người đang chia sẻ."
            ],
            "answer": 1,
            "explain": "Thông tin lịch học cần được đối chiếu với thông báo chính thức từ nhà trường."
        },
        "Tình huống 3: Hình ảnh thiếu ngữ cảnh": {
            "content": "Một hình ảnh được đăng kèm lời khẳng định về một sự kiện vừa xảy ra, nhưng không có ngày tháng hoặc nguồn gốc.",
            "options": [
                "Tin ngay vì hình ảnh là bằng chứng.",
                "Kiểm tra nguồn gốc và thời điểm của hình ảnh.",
                "Chia sẻ vì nội dung đang được quan tâm."
            ],
            "answer": 1,
            "explain": "Hình ảnh có thể cũ hoặc được sử dụng sai ngữ cảnh. Cần kiểm tra nguồn gốc."
        },
        "Tình huống 4: Cảnh báo tài khoản": {
            "content": "Một tin nhắn tự xưng là bộ phận hỗ trợ thông báo tài khoản của bạn có vấn đề và yêu cầu cung cấp mã xác minh.",
            "options": [
                "Gửi mã xác minh ngay.",
                "Kiểm tra qua kênh hỗ trợ chính thức.",
                "Chuyển tiếp tin nhắn cho nhiều người."
            ],
            "answer": 1,
            "explain": "Không chia sẻ mã xác minh. Hãy liên hệ nền tảng qua kênh chính thức."
        }
    }

    selected = st.selectbox("Chọn tình huống", list(scenarios.keys()))
    scenario = scenarios[selected]

    st.markdown(f"""
    <div class="cosmic-card">
        <h3>📱 Tình huống giả định</h3>
        <p>{scenario["content"]}</p>
    </div>
    """, unsafe_allow_html=True)

    choice = st.radio(
        "Em sẽ xử lý như thế nào?",
        scenario["options"],
        key="scenario_choice"
    )

    if st.button("Kiểm tra lựa chọn", use_container_width=True):

        answer_index = scenario["options"].index(choice)

        if answer_index == scenario["answer"]:
            st.success("🎉 Chính xác! Đây là lựa chọn an toàn hơn.")
        else:
            st.warning("Em hãy suy nghĩ thêm về nguồn tin và rủi ro.")

        st.info(scenario["explain"])

# =====================================================
# 11. PHẢN HỒI THÍCH ỨNG
# =====================================================

elif page == "🧠 Phản hồi thích ứng":

    st.title("🧠 Hệ thống phản hồi thích ứng")

    st.write(
        "Hệ thống đưa ra gợi ý dựa trên mức cảnh báo của nội dung "
        "đã được phân tích gần nhất."
    )

    result = st.session_state.last_analysis

    if result is None:
        st.info("Em cần phân tích ít nhất một nội dung trước.")
    else:

        st.metric("Mức cảnh báo hiện tại", result["level"])

        if result["score"] >= 60:
            st.error("⚠️ PHẢN HỒI: CẢNH BÁO")
            st.markdown("""
            - Tạm dừng việc chia sẻ.
            - Không cung cấp thông tin cá nhân.
            - Kiểm tra nguồn gốc nội dung.
            - Tìm kiếm bằng chứng từ nguồn độc lập.
            """)

        elif result["score"] >= 20:
            st.warning("🔎 PHẢN HỒI: CẦN SUY NGHĨ")
            st.markdown("""
            - Đọc kỹ nội dung.
            - Đặt câu hỏi về nguồn tin.
            - Kiểm tra các khẳng định quan trọng.
            - Không vội kết luận.
            """)

        else:
            st.success("🌱 PHẢN HỒI: TIẾP TỤC TƯ DUY PHẢN BIỆN")
            st.markdown("""
            - Tiếp tục kiểm tra nguồn.
            - Chú ý ngữ cảnh và thời gian.
            - Không coi việc thiếu dấu hiệu cảnh báo là bằng chứng nội dung đúng.
            """)

        st.markdown("---")
        st.subheader("💬 Câu hỏi tư duy")

        question = st.radio(
            "Trước khi chia sẻ thông tin, em nên tự hỏi điều gì?",
            [
                "Thông tin này có nhiều lượt thích không?",
                "Nguồn tin và bằng chứng có đáng tin cậy không?",
                "Bạn bè đã chia sẻ chưa?"
            ]
        )

        if st.button("Gửi câu trả lời"):
            if question == "Nguồn tin và bằng chứng có đáng tin cậy không?":
                st.success("Chính xác! Hãy ưu tiên nguồn và bằng chứng.")
            else:
                st.info("Lượt thích và việc nhiều người chia sẻ không chứng minh thông tin đúng.")

# =====================================================
# 12. KHẢO SÁT NGHIÊN CỨU
# =====================================================

elif page == "📝 Khảo sát nghiên cứu":

    st.title("📝 Khảo sát nhận thức thông tin số")

    st.write(
        "Khảo sát mô phỏng phục vụ nghiên cứu hành vi xác thực "
        "thông tin số của học sinh."
    )

    questions = [
        (
            "Khi thấy một thông tin gây sốc trên mạng, em nên làm gì?",
            [
                "Chia sẻ ngay",
                "Kiểm tra nguồn trước",
                "Tin vì có nhiều lượt thích"
            ],
            1
        ),
        (
            "Nguồn nào nên được ưu tiên khi kiểm tra thông báo của trường?",
            [
                "Bình luận trên mạng",
                "Tin nhắn không rõ người gửi",
                "Kênh thông báo chính thức"
            ],
            2
        ),
        (
            "Một hình ảnh trên mạng có luôn phản ánh đúng sự kiện không?",
            [
                "Có",
                "Không, cần kiểm tra ngữ cảnh",
                "Không cần quan tâm"
            ],
            1
        ),
        (
            "Khi nhận đường dẫn lạ yêu cầu thông tin cá nhân, em nên:",
            [
                "Cung cấp ngay",
                "Chuyển tiếp cho bạn bè",
                "Dừng lại và kiểm tra nguồn gửi"
            ],
            2
        ),
        (
            "Điều gì quan trọng nhất trước khi chia sẻ thông tin?",
            [
                "Tốc độ chia sẻ",
                "Nguồn tin và bằng chứng",
                "Số lượng lượt thích"
            ],
            1
        )
    ]

    survey_type = st.radio(
        "Chọn loại khảo sát",
        ["Khảo sát trước trải nghiệm", "Khảo sát sau trải nghiệm"]
    )

    answers = []

    with st.form("survey_form"):

        for i, item in enumerate(questions):
            st.markdown(f"**Câu {i+1}. {item[0]}**")
            selected = st.radio(
                "Lựa chọn",
                item[1],
                key=f"{survey_type}_{i}",
                label_visibility="collapsed"
            )
            answers.append(selected)

        submitted = st.form_submit_button(
            "📨 NỘP KHẢO SÁT",
            use_container_width=True
        )

    if submitted:

        score = 0

        for i, answer in enumerate(answers):
            if item_index := questions[i][1].index(answer):
                pass

            if item_index == questions[i][2]:
                score += 1

        if survey_type == "Khảo sát trước trải nghiệm":
            st.session_state.pre_score = score
        else:
            st.session_state.post_score = score

        st.success("Đã ghi nhận kết quả khảo sát.")
        st.metric("Số câu trả lời đúng", f"{score}/5")

    st.markdown("---")

    a, b = st.columns(2)

    with a:
        st.metric(
            "Kết quả trước trải nghiệm",
            str(st.session_state.pre_score)
            if st.session_state.pre_score is not None else "Chưa có"
        )

    with b:
        st.metric(
            "Kết quả sau trải nghiệm",
            str(st.session_state.post_score)
            if st.session_state.post_score is not None else "Chưa có"
        )

# =====================================================
# 13. THỐNG KÊ
# =====================================================

elif page == "📊 Thống kê":

    st.title("📊 Thống kê hoạt động nghiên cứu")

    records = st.session_state.records

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Tổng lượt phân tích", st.session_state.analysis_count)

    with col2:
        st.metric("Tổng lượt kiểm chứng", st.session_state.verified_count)

    with col3:
        st.metric("Tổng lượt phản hồi", st.session_state.reflection_count)

    st.markdown("---")

    if records:

        df = pd.DataFrame(records)

        st.subheader("📋 Lịch sử phân tích")
        st.dataframe(df, use_container_width=True)

        st.subheader("📈 Phân bố điểm cảnh báo")
        st.bar_chart(df["Điểm cảnh báo"])

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "⬇️ TẢI DỮ LIỆU CSV",
            data=csv,
            file_name="social_sandbox_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("Chưa có dữ liệu. Hãy thực hiện phân tích để xem thống kê.")

    st.markdown("---")
    st.subheader("📊 Kết quả khảo sát")

    if st.session_state.pre_score is not None:
        st.metric("Điểm trước trải nghiệm", f'{st.session_state.pre_score}/5')

    if st.session_state.post_score is not None:
        st.metric("Điểm sau trải nghiệm", f'{st.session_state.post_score}/5')

    if (
        st.session_state.pre_score is not None
        and st.session_state.post_score is not None
    ):
        difference = (
            st.session_state.post_score - st.session_state.pre_score
        )

        st.metric("Chênh lệch điểm", f"{difference:+d}")

# =====================================================
# 14. GIỚI THIỆU ĐỀ TÀI
# =====================================================

elif page == "ℹ️ Giới thiệu đề tài":

    st.title("ℹ️ Giới thiệu Social Sandbox AI")

    st.markdown("""
    <div class="cosmic-card">
        <h2>🔬 Tên đề tài</h2>
        <p>
        Nghiên cứu hành vi xác thực thông tin số của học sinh trung học
        và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 Mục tiêu nghiên cứu")

    st.write("""
    - Tìm hiểu hành vi tiếp nhận và chia sẻ thông tin số của học sinh.
    - Nhận diện một số dấu hiệu thường gặp trong nội dung đáng ngờ.
    - Xây dựng môi trường mô phỏng để rèn luyện tư duy phản biện.
    - Đưa ra phản hồi nhằm khuyến khích học sinh kiểm chứng trước khi chia sẻ.
    """)

    st.subheader("⚙️ Công nghệ sử dụng")

    technologies = [
        ("Python", "Ngôn ngữ lập trình chính."),
        ("Streamlit", "Xây dựng giao diện ứng dụng web."),
        ("Pandas", "Quản lý và xuất dữ liệu nghiên cứu."),
        ("HTML/CSS", "Thiết kế giao diện và hiệu ứng chuyển động."),
        ("Rule-based analysis", "Nhận diện dấu hiệu bằng bộ quy tắc từ khóa.")
    ]

    for name, description in technologies:
        st.markdown(f"""
        <div class="cosmic-card">
            <h4>✦ {name}</h4>
            <p>{description}</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("⚠️ Giới hạn của phiên bản thử nghiệm")

    st.warning("""
    Phiên bản này sử dụng bộ từ khóa và quy tắc để nhận diện dấu hiệu.
    Hệ thống chưa xác minh sự thật của thông tin, chưa kiểm tra nguồn
    trên Internet và chưa phải mô hình AI có khả năng hiểu ngữ cảnh đầy đủ.

    Điểm cảnh báo không phải xác suất thông tin sai lệch.
    Dữ liệu trong session có thể mất khi ứng dụng khởi động lại.
    """)

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center;padding:20px;">
        <h2 style="color:#ff7189!important;">🌌 SOCIAL SANDBOX AI</h2>
        <p>Think Before You Share.</p>
        <p style="font-size:12px;">Digital Literacy Lab • Educational Prototype</p>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# 15. CHÂN TRANG
# =====================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center;padding:15px;">
    <p style="color:#ff7189;font-size:13px;">
        🌌 SOCIAL SANDBOX AI
    </p>
    <p style="font-size:11px;color:#a99aa3;">
        THINK BEFORE YOU SHARE • EXPLORE • VERIFY • PROTECT
    </p>
</div>
""", unsafe_allow_html=True)
