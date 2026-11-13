
import streamlit as st
import pandas as pd
import html
from datetime import datetime

# =====================================================
# 1. CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

NAVY = "#00246B"
ICE = "#CADCFC"
WHITE = "#FFFFFF"
BLACK = "#000000"

# =====================================================
# 2. DESIGN SYSTEM
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800;900&display=swap');

.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(202,220,252,.15), transparent 25%),
        radial-gradient(circle at 85% 75%, rgba(202,220,252,.12), transparent 25%),
        linear-gradient(135deg,#00143D,#00246B,#00143D);
    font-family:'Be Vietnam Pro',sans-serif;
}

/* MAIN CONTENT */
.main .block-container {
    max-width:1450px;
    padding:2rem 2.5rem 3rem;
}

/* OUTSIDE TEXT */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp li,
.stApp label,
.stApp .stMarkdown,
.stApp .stCaption,
.stApp [data-testid="stMetricLabel"] {
    color:#FFFFFF;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#CADCFC,#FFFFFF);
}
section[data-testid="stSidebar"] * {
    color:#000000 !important;
}

/* HEADER */
.main-title {
    font-size:36px;
    font-weight:900;
    color:#FFFFFF;
    letter-spacing:-1px;
}
.main-subtitle {
    color:#CADCFC;
    font-size:13px;
    font-weight:600;
    letter-spacing:1px;
    margin-bottom:25px;
}

/* HERO */
.hero {
    background:linear-gradient(120deg,#FFFFFF,#CADCFC);
    padding:30px;
    border-radius:22px;
    margin-bottom:24px;
    box-shadow:0 10px 30px rgba(0,0,0,.2);
}
.hero * {
    color:#00246B !important;
}

/* LIGHT CARDS */
.light-card {
    background:linear-gradient(145deg,#FFFFFF,#EDF4FF);
    border:1px solid #CADCFC;
    border-radius:17px;
    padding:22px;
    margin:12px 0;
    box-shadow:0 6px 20px rgba(0,0,0,.12);
    color:#000000;
}
.light-card * {
    color:#000000 !important;
}
.card-title {
    font-size:18px;
    font-weight:800;
    margin-bottom:10px;
}

/* SECTION */
.section-title {
    color:#FFFFFF;
    font-size:24px;
    font-weight:850;
    margin:20px 0 14px;
}

/* INPUTS */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    background:#FFFFFF !important;
    color:#000000 !important;
    border-radius:10px !important;
}
.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color:#666666 !important;
}

/* DROPDOWN */
div[data-baseweb="popover"],
div[data-baseweb="menu"] {
    background:#FFFFFF !important;
}
div[data-baseweb="popover"] * {
    color:#000000 !important;
}

/* BUTTONS */
.stButton button,
.stDownloadButton button {
    background:linear-gradient(120deg,#CADCFC,#FFFFFF);
    color:#00246B !important;
    border:1px solid #CADCFC;
    border-radius:11px;
    font-weight:800;
    transition:.25s;
}
.stButton button:hover,
.stDownloadButton button:hover {
    transform:translateY(-2px);
    box-shadow:0 5px 18px rgba(202,220,252,.35);
}

/* METRICS */
[data-testid="stMetric"] {
    background:linear-gradient(145deg,#FFFFFF,#EDF4FF);
    border-radius:15px;
    padding:18px;
    border:1px solid #CADCFC;
}
[data-testid="stMetric"] * {
    color:#00246B !important;
}

/* ALERTS */
.stAlert {
    background:#FFFFFF !important;
    border-radius:12px;
}
.stAlert * {
    color:#000000 !important;
}

/* RADIO */
.stRadio label,
.stCheckbox label {
    color:#FFFFFF !important;
}

/* DATA */
[data-testid="stDataFrame"] {
    background:#FFFFFF;
    border-radius:12px;
}

/* DIVIDER */
hr {
    border-color:rgba(202,220,252,.4);
}

/* FOOTER */
.footer {
    text-align:center;
    color:#CADCFC;
    font-size:12px;
    padding:25px 0 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. SESSION DATA
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
# 4. HELPER FUNCTIONS
# =====================================================

def card(title, content):
    safe_title = html.escape(str(title))
    safe_content = html.escape(str(content)).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="light-card">
            <div class="card-title">{safe_title}</div>
            <div>{safe_content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def detect_signals(content):
    groups = {
        "Ngôn ngữ giật gân": [
            "sốc", "kinh hoàng", "chấn động",
            "không thể tin", "bí mật động trời"
        ],
        "Thúc giục chia sẻ": [
            "chia sẻ ngay", "share ngay",
            "gửi cho mọi người", "đừng bỏ lỡ"
        ],
        "Nguồn không rõ ràng": [
            "nghe nói", "người ta bảo",
            "theo nguồn tin", "có người nói"
        ],
        "Khẳng định tuyệt đối": [
            "100% đúng", "chắc chắn",
            "không bao giờ sai", "tất cả đều"
        ],
        "Tạo áp lực và sợ hãi": [
            "nguy hiểm", "khẩn cấp",
            "cảnh báo ngay", "nếu không sẽ"
        ]
    }

    found = []
    text = content.lower()

    for category, keywords in groups.items():
        matches = [word for word in keywords if word in text]
        if matches:
            found.append({
                "category": category,
                "keywords": matches
            })

    score = min(len(found) * 20, 100)
    return score, found


def risk_label(score):
    if score >= 60:
        return "Nhiều dấu hiệu cần kiểm tra", "#D62828"
    elif score >= 20:
        return "Có dấu hiệu cần chú ý", "#B77900"
    return "Ít dấu hiệu theo bộ lọc từ khóa", "#16834A"


# =====================================================
# 5. GEMINI AI - UPDATED MODEL
# =====================================================

def gemini_analysis(content):

    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        return None, "Chưa cấu hình GEMINI_API_KEY trong secrets.toml."

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Bạn là trợ lý giáo dục về năng lực số dành cho học sinh trung học.

Hãy phân tích nội dung sau:

{content}

Trình bày bằng tiếng Việt, dễ hiểu, theo các mục:

1. Tóm tắt nội dung.
2. Dấu hiệu đáng chú ý.
3. Đánh giá nguồn thông tin.
4. Những nội dung cần kiểm chứng.
5. Ba câu hỏi tư duy phản biện.
6. Khuyến nghị trước khi chia sẻ.

YÊU CẦU:
- Không kết luận thông tin thật hoặc giả nếu thiếu bằng chứng.
- Không tự tạo nguồn tham khảo.
- Phân biệt dấu hiệu nghi vấn với bằng chứng.
- Dùng ngôn ngữ phù hợp học sinh trung học.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text, None

    except Exception as error:
        return None, str(error)


def save_record(content, score, activity):
    st.session_state.records.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Nội dung": content[:150],
        "Điểm dấu hiệu": score,
        "Hoạt động": activity
    })


# =====================================================
# 6. SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:18px 5px;">
        <div style="font-size:42px;">🌐</div>
        <div style="font-size:22px;font-weight:900;">
            SOCIAL SANDBOX
        </div>
        <div style="font-size:11px;font-weight:700;">
            DIGITAL LEARNING PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

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

    st.markdown("### 🎯 Mục tiêu")
    st.caption(
        "Phát triển năng lực số, tư duy phản biện "
        "và kỹ năng xác thực thông tin."
    )

    st.divider()
    st.caption("SOCIAL SANDBOX AI • V2.1")


# =====================================================
# 7. MAIN HEADER
# =====================================================

st.markdown("""
<div class="main-title">SOCIAL SANDBOX AI</div>
<div class="main-subtitle">
DIGITAL LITERACY • CRITICAL THINKING • RESPONSIBLE SHARING
</div>
""", unsafe_allow_html=True)


# =====================================================
# PAGE 1 - OVERVIEW
# =====================================================

if page == "🏠 Tổng quan":

    st.markdown("""
    <div class="hero">
        <div style="font-size:13px;font-weight:800;">
            DIGITAL LITERACY LAB
        </div>
        <h1>Học cách kiểm chứng trước khi chia sẻ</h1>
        <p>
            Môi trường học tập mô phỏng giúp học sinh nhận diện
            dấu hiệu bất thường, đánh giá nguồn tin và hình thành
            thói quen sử dụng thông tin có trách nhiệm.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">📌 Tổng quan hoạt động</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(4)
    metrics = [
        ("Lượt phân tích", st.session_state.analysis_count),
        ("Lượt kiểm chứng", st.session_state.verified_count),
        ("Lượt phản hồi", st.session_state.reflection_count),
        ("Kịch bản hoàn thành", st.session_state.scenario_done)
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.metric(label, value)

    st.markdown(
        '<div class="section-title">🎯 Mục tiêu học tập</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        card(
            "🔎 Nhận diện thông tin",
            "Nhận biết ngôn ngữ giật gân, nguồn tin chưa rõ "
            "và dấu hiệu cần kiểm tra."
        )
        card(
            "🧠 Tư duy phản biện",
            "Biết đặt câu hỏi, đối chiếu bằng chứng "
            "và không vội tin vào nội dung trên mạng."
        )

    with col2:
        card(
            "🛡️ An toàn số",
            "Hình thành thói quen sử dụng và chia sẻ "
            "thông tin có trách nhiệm."
        )
        card(
            "📚 Học tập chủ động",
            "Tự đánh giá, tiếp nhận phản hồi và cải thiện "
            "năng lực xác thực thông tin."
        )

    st.info("Chọn một chức năng ở thanh điều hướng để bắt đầu.")


# =====================================================
# PAGE 2 - AI ANALYSIS
# =====================================================

elif page == "🔍 Phân tích thông tin bằng AI":

    st.markdown(
        '<div class="section-title">🔍 Phân tích thông tin bằng AI</div>',
        unsafe_allow_html=True
    )

    card(
        "Hướng dẫn sử dụng",
        "Nhập nội dung bài viết, thông báo hoặc thông tin trên mạng. "
        "Hệ thống sẽ nhận diện dấu hiệu bằng bộ lọc từ khóa và "
        "hỗ trợ phân tích bằng Gemini AI."
    )

    content = st.text_area(
        "NỘI DUNG CẦN PHÂN TÍCH",
        height=220,
        placeholder="Dán nội dung thông tin vào đây..."
    )

    st.caption(
        "Ví dụ: Bài đăng có tiêu đề gây sốc, yêu cầu chia sẻ ngay "
        "nhưng không ghi rõ nguồn."
    )

    if st.button("🚀 BẮT ĐẦU PHÂN TÍCH", use_container_width=True):

        if len(content.strip()) < 10:
            st.warning("Vui lòng nhập nội dung dài hơn 10 ký tự.")

        else:
            st.session_state.analysis_count += 1

            with st.spinner("Đang phân tích nội dung..."):

                score, detected = detect_signals(content)
                label, color = risk_label(score)

                st.markdown(
                    '<div class="section-title">📊 Kết quả nhận diện</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <div class="light-card">
                        <div class="card-title">
                            Điểm dấu hiệu theo bộ lọc từ khóa
                        </div>
                        <div style="font-size:40px;font-weight:900;color:{color};">
                            {score}/100
                        </div>
                        <b style="color:{color};">{label}</b>
                        <p>
                            Đây là chỉ số heuristic dựa trên từ khóa,
                            không phải xác suất thông tin sai lệch.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if detected:
                    st.markdown("### Các dấu hiệu phát hiện được")

                    for item in detected:
                        card(
                            item["category"],
                            "Từ khóa liên quan: " +
                            ", ".join(item["keywords"])
                        )
                else:
                    st.info(
                        "Không phát hiện từ khóa thuộc các nhóm đã thiết lập. "
                        "Điều này không chứng minh nội dung là chính xác."
                    )

                st.markdown(
                    '<div class="section-title">🤖 Kết quả Gemini AI</div>',
                    unsafe_allow_html=True
                )

                ai_result, ai_error = gemini_analysis(content)

                if ai_result:
                    card("Phân tích từ AI", ai_result)
                else:
                    st.error(f"Lỗi kết nối AI: {ai_error}")
                    st.caption(
                        "Hãy kiểm tra API Key, tên model và kết nối mạng."
                    )

                save_record(content, score, "Phân tích AI")
                st.success("Đã hoàn thành phân tích.")


# =====================================================
# PAGE 3 - VERIFICATION
# =====================================================

elif page == "🛡️ Phòng kiểm chứng":

    st.markdown(
        '<div class="section-title">🛡️ Phòng kiểm chứng thông tin</div>',
        unsafe_allow_html=True
    )

    card(
        "Nhiệm vụ học tập",
        "Thực hiện quy trình 5 bước trước khi tin tưởng "
        "hoặc chia sẻ thông tin trên môi trường số."
    )

    steps = [
        "Xác định nguồn đăng tải thông tin.",
        "Kiểm tra tác giả hoặc đơn vị chịu trách nhiệm.",
        "Tìm bằng chứng và dữ liệu hỗ trợ.",
        "Đối chiếu với nguồn độc lập, đáng tin cậy.",
        "Đánh giá lại trước khi chia sẻ."
    ]

    checked = []

    for i, step in enumerate(steps):
        checked.append(
            st.checkbox(step, key=f"verify_{i}")
        )

    progress = sum(checked) / 5

    st.progress(progress)
    st.write(f"Tiến độ: {sum(checked)}/5 bước")

    if st.button("✅ HOÀN THÀNH KIỂM CHỨNG",
                 use_container_width=True):

        if all(checked):
            st.session_state.verified_count += 1
            st.success("Em đã hoàn thành quy trình kiểm chứng.")
            card(
                "Kết luận",
                "Hãy lưu lại bằng chứng và chỉ chia sẻ thông tin "
                "khi có căn cứ phù hợp."
            )
        else:
            st.warning("Em hãy hoàn thành các bước còn lại.")


# =====================================================
# PAGE 4 - SOCIAL SIMULATION
# =====================================================

elif page == "🎭 Mô phỏng mạng xã hội":

    st.markdown(
        '<div class="section-title">🎭 Mô phỏng mạng xã hội</div>',
        unsafe_allow_html=True
    )

    card(
        "Thử thách tình huống",
        "Đọc tình huống và lựa chọn cách xử lý phù hợp."
    )

    scenarios = {
        "Bài đăng không rõ nguồn":
            "Một tài khoản đăng thông tin quan trọng nhưng không dẫn nguồn.",
        "Thông tin giật gân":
            "Một bài viết sử dụng tiêu đề gây sốc để thu hút lượt xem.",
        "Kêu gọi chia sẻ khẩn cấp":
            "Một bài đăng yêu cầu mọi người chia sẻ ngay lập tức.",
        "Hình ảnh thiếu bối cảnh":
            "Một hình ảnh được đăng lại nhưng không rõ thời gian và địa điểm."
    }

    scenario = st.selectbox(
        "CHỌN TÌNH HUỐNG",
        list(scenarios.keys())
    )

    card("📱 Bài đăng mô phỏng", scenarios[scenario])

    answer = st.radio(
        "Em sẽ lựa chọn hành động nào?",
        [
            "Chia sẻ ngay vì nhiều người quan tâm.",
            "Tin ngay vì bài viết có nhiều lượt tương tác.",
            "Kiểm tra nguồn và đối chiếu bằng chứng.",
            "Khẳng định thông tin là đúng."
        ]
    )

    if st.button("GỬI LỰA CHỌN", use_container_width=True):

        st.session_state.scenario_done += 1

        if answer == "Kiểm tra nguồn và đối chiếu bằng chứng.":
            st.success("Chính xác! Đây là lựa chọn có trách nhiệm.")
            card(
                "Giải thích",
                "Cần xác định nguồn, tìm bằng chứng và đối chiếu "
                "thông tin trước khi chia sẻ."
            )
        else:
            st.warning("Hãy suy nghĩ thêm về lựa chọn của em.")
            card(
                "Gợi ý",
                "Lượt tương tác không phải bằng chứng xác thực. "
                "Hãy kiểm tra nguồn tin trước khi kết luận."
            )


# =====================================================
# PAGE 5 - ADAPTIVE FEEDBACK
# =====================================================

elif page == "🧠 Phản hồi thích ứng":

    st.markdown(
        '<div class="section-title">🧠 Phản hồi thích ứng</div>',
        unsafe_allow_html=True
    )

    card(
        "Mục tiêu",
        "Giúp học sinh tự đánh giá cách tiếp nhận thông tin "
        "và lựa chọn hành động phù hợp."
    )

    question = st.radio(
        "Khi gặp thông tin chưa rõ nguồn trên mạng, em thường:",
        [
            "Tin ngay nếu nội dung có vẻ hợp lý.",
            "Đọc bình luận để xem mọi người nghĩ gì.",
            "Kiểm tra nguồn và tìm thêm bằng chứng.",
            "Chia sẻ để hỏi ý kiến bạn bè."
        ]
    )

    reason = st.text_area(
        "Vì sao em lựa chọn như vậy?",
        placeholder="Viết suy nghĩ của em..."
    )

    if st.button("📩 NHẬN PHẢN HỒI", use_container_width=True):

        st.session_state.reflection_count += 1

        if question == "Kiểm tra nguồn và tìm thêm bằng chứng.":
            card(
                "🌟 Phản hồi tích cực",
                "Em đã thể hiện thói quen tiếp nhận thông tin "
                "có trách nhiệm. Hãy tiếp tục đối chiếu nguồn và bằng chứng."
            )
        else:
            card(
                "💡 Gợi ý cải thiện",
                "Em nên kiểm tra nguồn đăng tải, tác giả và bằng chứng "
                "trước khi đưa ra kết luận hoặc chia sẻ."
            )

        if reason.strip():
            card("Suy nghĩ của em", reason)

        st.success("Đã ghi nhận hoạt động phản hồi.")


# =====================================================
# PAGE 6 - RESEARCH STATISTICS
# =====================================================

elif page == "📊 Thống kê nghiên cứu":

    st.markdown(
        '<div class="section-title">📊 Thống kê nghiên cứu</div>',
        unsafe_allow_html=True
    )

    cols = st.columns(3)

    with cols[0]:
        st.metric("Lượt phân tích", st.session_state.analysis_count)

    with cols[1]:
        st.metric("Lượt kiểm chứng", st.session_state.verified_count)

    with cols[2]:
        st.metric("Lượt phản hồi", st.session_state.reflection_count)

    activity = pd.DataFrame({
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

    st.markdown("### 📈 Biểu đồ hoạt động")
    st.bar_chart(activity.set_index("Hoạt động"))

    st.markdown("### 📋 Lịch sử phân tích")

    if st.session_state.records:

        df = pd.DataFrame(st.session_state.records)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

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
        card(
            "Chưa có dữ liệu",
            "Các hoạt động sẽ được ghi nhận trong phiên sử dụng hiện tại."
        )

    st.warning(
        "Dữ liệu hiện được lưu trong phiên Streamlit và có thể mất "
        "khi phiên kết thúc hoặc ứng dụng khởi động lại."
    )


# =====================================================
# 8. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    SOCIAL SANDBOX AI • DIGITAL LITERACY LAB<br>
    Nền tảng hỗ trợ học tập, tư duy phản biện và năng lực số<br>
    Phiên bản thử nghiệm giáo dục
</div>
""", unsafe_allow_html=True)
