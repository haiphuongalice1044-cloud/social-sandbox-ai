
import re
import random
from datetime import datetime

import pandas as pd
import streamlit as st

# =========================================================
# 1. CAU HINH UNG DUNG
# =========================================================

st.set_page_config(
    page_title="Simulated Social Sandbox",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    .stApp {
        background:
          radial-gradient(ellipse at top left,
          rgba(87, 65, 180, 0.17), transparent 38%),
          #0b1020;
        color: #edf1ff;
    }

    [data-testid="stSidebar"] {
        background: #11182b;
        border-right: 1px solid #26304b;
    }

    [data-testid="stSidebar"] * {
        color: #edf1ff;
    }

    .hero {
        padding: 28px;
        border-radius: 22px;
        background: linear-gradient(
          120deg, #25205a, #143b59
        );
        border: 1px solid #414b81;
        margin-bottom: 22px;
    }

    .hero h1 {
        font-size: 34px;
        line-height: 1.3;
        margin-bottom: 8px;
        color: white;
    }

    .hero p {
        color: #d4e7ff;
        font-size: 15px;
    }

    .panel {
        padding: 20px;
        border: 1px solid #293651;
        background: rgba(20, 28, 48, 0.9);
        border-radius: 16px;
        margin-bottom: 14px;
    }

    .muted {
        color: #aebbd5;
        font-size: 13px;
    }

    .stButton > button {
        border-radius: 11px;
        font-weight: 600;
        min-height: 44px;
    }

    div[data-testid="stMetric"] {
        background: #151d32;
        padding: 15px;
        border: 1px solid #293651;
        border-radius: 14px;
    }

    .stTextArea textarea, .stTextInput input {
        border-radius: 12px;
    }

    hr {
        border-color: #293651;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# 2. DU LIEU MAU VA KHOI TAO
# =========================================================

SAMPLES = {
    "Tin nhắn nhận quà": (
        "Chúc mừng bạn trúng thưởng 20 triệu đồng! "
        "Hãy bấm vào liên kết và đóng phí xác nhận ngay "
        "trong 10 phút để nhận thưởng."
    ),
    "Tin nhắn giả danh ngân hàng": (
        "Tài khoản ngân hàng của bạn sắp bị khóa. "
        "Hãy truy cập đường link này và nhập mật khẩu, "
        "mã OTP để xác minh ngay."
    ),
    "Tin tuyển cộng tác viên": (
        "Tuyển cộng tác viên làm việc tại nhà, thu nhập "
        "5 triệu mỗi ngày. Chỉ cần chuyển tiền đặt cọc "
        "để kích hoạt tài khoản."
    ),
    "Bài đăng sức khỏe": (
        "Một bài đăng trên mạng khẳng định uống một loại "
        "nước mỗi ngày có thể chữa khỏi mọi bệnh, nhưng "
        "không nêu tên nghiên cứu hay nguồn y khoa."
    ),
    "Tin tức chưa rõ nguồn": (
        "Một bài viết lan truyền thông tin rằng ngày mai "
        "tất cả trường học sẽ nghỉ học. Bài viết không có "
        "nguồn chính thức hoặc ngày đăng rõ ràng."
    ),
    "Tin nhắn từ người quen": (
        "Một tài khoản dùng ảnh đại diện của bạn em nhắn "
        "mượn tiền gấp và yêu cầu chuyển khoản ngay. "
        "Tài khoản nói không tiện gọi điện."
    ),
}

SCENARIOS = [
    {
        "title": "Trúng thưởng bất ngờ",
        "content": (
            "Bạn nhận được tin nhắn báo trúng điện thoại "
            "mới, nhưng phải chuyển phí nhận quà trước."
        ),
        "question": "Em nên làm gì trước tiên?",
        "options": [
            "Chuyển phí ngay để không mất quà",
            "Kiểm tra đơn vị tổ chức qua nguồn chính thức",
            "Gửi tin nhắn cho tất cả bạn bè",
        ],
        "answer": 1,
        "explain": (
            "Yêu cầu trả phí để nhận phần thưởng bất ngờ "
            "là dấu hiệu cần cảnh giác. Hãy kiểm tra nguồn "
            "độc lập trước khi cung cấp tiền hoặc dữ liệu."
        ),
    },
    {
        "title": "Đường link ngân hàng",
        "content": (
            "Một tin nhắn cảnh báo tài khoản sẽ bị khóa "
            "và yêu cầu nhập mật khẩu cùng mã OTP."
        ),
        "question": "Lựa chọn an toàn nhất là gì?",
        "options": [
            "Nhập thông tin ngay",
            "Chuyển tiếp tin nhắn cho người khác",
            "Không mở link, tự liên hệ ngân hàng qua kênh chính thức",
        ],
        "answer": 2,
        "explain": (
            "Không chia sẻ mật khẩu hoặc OTP qua liên kết "
            "trong tin nhắn. Hãy tự mở ứng dụng hoặc liên hệ "
            "ngân hàng bằng kênh chính thức."
        ),
    },
    {
        "title": "Tin tức lan truyền",
        "content": (
            "Một bài đăng có hàng nghìn lượt chia sẻ nhưng "
            "không nêu nguồn gốc của thông tin."
        ),
        "question": "Em nên kiểm chứng như thế nào?",
        "options": [
            "Tin vì nhiều người chia sẻ",
            "Tìm nguồn ban đầu và đối chiếu nguồn độc lập",
            "Chia sẻ ngay để mọi người biết",
        ],
        "answer": 1,
        "explain": (
            "Lượt chia sẻ không chứng minh thông tin đúng. "
            "Cần tìm nguồn gốc, ngày đăng và nguồn độc lập."
        ),
    },
    {
        "title": "Cộng tác viên online",
        "content": (
            "Một công việc hứa thu nhập rất cao, yêu cầu "
            "nộp tiền để mở nhiệm vụ."
        ),
        "question": "Điều gì cần được xem xét?",
        "options": [
            "Chuyển tiền để thử",
            "Kiểm tra doanh nghiệp, điều khoản và yêu cầu đặt cọc",
            "Cung cấp thông tin ngân hàng ngay",
        ],
        "answer": 1,
        "explain": (
            "Lời hứa thu nhập cao và yêu cầu nộp tiền trước "
            "cần được xác minh kỹ. Không chuyển tiền khi "
            "chưa hiểu rõ đơn vị tuyển dụng."
        ),
    },
    {
        "title": "Bạn bè mượn tiền",
        "content": (
            "Tài khoản của một người bạn bất ngờ mượn tiền "
            "và liên tục thúc giục chuyển khoản."
        ),
        "question": "Em nên làm gì?",
        "options": [
            "Gọi điện xác nhận bằng cách liên hệ đã biết",
            "Chuyển tiền ngay vì là bạn",
            "Đăng công khai số tài khoản của bạn ấy",
        ],
        "answer": 0,
        "explain": (
            "Tài khoản có thể bị chiếm quyền hoặc giả mạo. "
            "Hãy xác minh danh tính qua một kênh khác."
        ),
    },
    {
        "title": "Ứng dụng không rõ nguồn",
        "content": (
            "Một trang web yêu cầu tải ứng dụng lạ và cấp "
            "quyền truy cập danh bạ, tin nhắn."
        ),
        "question": "Em nên ưu tiên điều gì?",
        "options": [
            "Cấp tất cả quyền để ứng dụng chạy",
            "Kiểm tra nhà phát triển và quyền cần thiết",
            "Gửi ứng dụng cho bạn bè cài thử",
        ],
        "answer": 1,
        "explain": (
            "Chỉ cài ứng dụng từ nguồn đáng tin cậy và xem "
            "xét kỹ quyền truy cập. Không cấp quyền không "
            "cần thiết."
        ),
    },
    {
        "title": "Học bổng trực tuyến",
        "content": (
            "Một tài khoản tự nhận cấp học bổng yêu cầu "
            "học sinh gửi giấy tờ cá nhân và đóng phí hồ sơ "
            "qua tài khoản cá nhân."
        ),
        "question": "Em nên làm gì?",
        "options": [
            "Gửi giấy tờ ngay",
            "Kiểm tra thông báo của đơn vị cấp học bổng",
            "Đăng giấy tờ lên mạng để hỏi mọi người",
        ],
        "answer": 1,
        "explain": (
            "Cần xác minh chương trình và kênh tiếp nhận hồ sơ "
            "qua trang chính thức trước khi cung cấp dữ liệu."
        ),
    },
    {
        "title": "Ảnh chụp làm bằng chứng",
        "content": (
            "Một bài đăng dùng ảnh chụp màn hình làm bằng "
            "chứng nhưng không có liên kết đến nguồn gốc."
        ),
        "question": "Cách kiểm tra phù hợp là gì?",
        "options": [
            "Tin hoàn toàn vì có hình ảnh",
            "Tìm ngữ cảnh và nguồn ban đầu của hình ảnh",
            "Chỉ đọc bình luận đồng tình",
        ],
        "answer": 1,
        "explain": (
            "Ảnh chụp có thể thiếu ngữ cảnh hoặc bị chỉnh sửa. "
            "Hãy tìm nguồn gốc và đối chiếu thông tin."
        ),
    },
]

RULES = {
    "Bảo mật tài khoản": [
        "mật khẩu", "password", "mã otp", "otp",
        "mã xác minh", "đăng nhập",
    ],
    "Yêu cầu tiền": [
        "chuyển tiền", "đặt cọc", "đóng phí",
        "nộp phí", "phí xác nhận", "chuyển khoản",
    ],
    "Thúc giục hoặc đe dọa": [
        "ngay lập tức", "trong 10 phút", "sắp bị khóa",
        "khẩn cấp", "ngay", "đe dọa",
    ],
    "Lời hứa bất thường": [
        "trúng thưởng", "thu nhập 5 triệu",
        "lợi nhuận cao", "chữa khỏi mọi bệnh",
        "nhận quà", "kiếm tiền dễ dàng",
    ],
    "Thông tin cá nhân": [
        "căn cước", "số căn cước", "ngày sinh",
        "địa chỉ nhà", "danh bạ", "giấy tờ cá nhân",
    ],
    "Nguồn chưa rõ": [
        "không có nguồn", "nghe nói", "lan truyền",
        "không nêu nguồn", "bài đăng khẳng định",
    ],
}


def init_state():
    if "history" not in st.session_state:
        st.session_state.history = []

    if "survey" not in st.session_state:
        st.session_state.survey = []

    if "scenario_index" not in st.session_state:
        st.session_state.scenario_index = 0

    if "scenario_results" not in st.session_state:
        st.session_state.scenario_results = []


init_state()

# =========================================================
# 3. GEMINI API
# =========================================================

def get_api_key():
    """Lay khoa tu Streamlit Secrets, khong luu trong ma nguon."""
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def ask_gemini(text):
    """Phan tich noi dung bang Gemini; tra ve (ket_qua, loi)."""
    api_key = get_api_key()

    if not api_key:
        return None, (
            "Chưa tìm thấy GEMINI_API_KEY. "
            "Quản trị viên hãy kiểm tra Settings → Secrets "
            "trên Streamlit Cloud."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Bạn là trợ lý giáo dục giúp học sinh trung học rèn luyện
kỹ năng xác thực thông tin số và tư duy phản biện.

Hãy phân tích nội dung dưới đây bằng tiếng Việt, rõ ràng,
không gây hoang mang và không kết luận vượt quá bằng chứng.

NỘI DUNG CẦN PHÂN TÍCH:
{text}

Trình bày theo cấu trúc:

1. Tóm tắt nội dung.
2. Mức độ cần thận trọng: Thấp, Trung bình hoặc Cao.
   Đây là đánh giá sơ bộ dựa trên nội dung được cung cấp,
   không phải kết luận pháp lý hay xác minh sự thật.
3. Các dấu hiệu đáng chú ý và giải thích cụ thể.
4. Những điều chưa đủ bằng chứng để kết luận.
5. Ba bước kiểm chứng an toàn, thực tế.
6. Một câu hỏi giúp học sinh suy nghĩ phản biện.

Nguyên tắc:
- Không khẳng định chắc chắn là lừa đảo nếu thiếu bằng chứng.
- Không tuyên bố đã truy cập website hoặc xác minh nguồn trực tiếp.
- Không yêu cầu mật khẩu, mã OTP hoặc thông tin riêng tư.
- Nếu thiếu dữ liệu, hãy nói rõ giới hạn.
- Ưu tiên lời khuyên an toàn, dễ thực hiện.
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
        )

        if not response.text:
            return None, (
                "Gemini không trả về nội dung. Em thử lại sau nhé."
            )

        return response.text, None

    except Exception as error:
        message = str(error).lower()
        error_type = type(error).__name__

        if (
            "quota" in message
            or "429" in message
            or "resource_exhausted" in message
            or "rate limit" in message
        ):
            return None, (
                "Gemini đã hết hạn mức hoặc bị giới hạn lượt dùng. "
                "Hãy thử lại sau. Website không tự chuyển sang "
                "dịch vụ trả phí."
            )

        if (
            "api key" in message
            or "api_key" in message
            or "permission" in message
            or "403" in message
            or "unauthenticated" in message
        ):
            return None, (
                "Gemini không xác thực được API key. "
                "Hãy kiểm tra Secrets và quyền truy cập API."
            )

        if (
            "not found" in message
            or "404" in message
            or "model" in message
        ):
            return None, (
                "Không gọi được mô hình Gemini đang cấu hình. "
                "Hãy kiểm tra tên mô hình và quyền truy cập. "
                f"Mã lỗi: {error_type}"
            )

        return None, (
            "Gemini chưa xử lý được yêu cầu. "
            f"Loại lỗi: {error_type}. "
            "Quản trị viên có thể kiểm tra Logs trên Streamlit Cloud."
        )


# =========================================================
# 4. PHAN TICH CO BAN KHONG CAN AI
# =========================================================

def rule_analysis(text):
    found = []

    lower_text = text.lower()

    for category, keywords in RULES.items():
        matches = [word for word in keywords if word in lower_text]
        if matches:
            found.append({
                "category": category,
                "matches": matches,
            })

    url_matches = re.findall(
        r"https?://[^\s]+|www\.[^\s]+",
        text,
        flags=re.IGNORECASE,
    )

    if url_matches:
        found.append({
            "category": "Có đường dẫn cần kiểm tra",
            "matches": url_matches,
        })

    score = len(found)

    if score >= 3:
        level = "Cần thận trọng cao"
    elif score >= 1:
        level = "Cần kiểm tra thêm"
    else:
        level = "Chưa phát hiện dấu hiệu theo bộ quy tắc"

    return {
        "level": level,
        "score": score,
        "found": found,
    }


def save_history(content, method, result, level):
    st.session_state.history.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Phương pháp": method,
        "Nội dung": content[:300],
        "Đánh giá": level,
        "Kết quả": result[:1000],
    })


# =========================================================
# 5. THANH DIEU HUONG
# =========================================================

st.sidebar.markdown("# 🛡️ Social Sandbox AI")
st.sidebar.caption("Không gian thực hành xác thực thông tin số")
st.sidebar.divider()

page = st.sidebar.radio(
    "CHỨC NĂNG",
    [
        "🔎 Kiểm tra thông tin",
        "🧩 Thử tình huống",
        "📝 Khảo sát nhanh",
        "📊 Lịch sử & thống kê",
        "ℹ️ Về đề tài",
    ],
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    <div class="muted">
    Dự án nghiên cứu giáo dục<br>
    AI hỗ trợ, con người quyết định.<br><br>
    Dữ liệu lịch sử hiện lưu trong phiên sử dụng.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 6. TRANG KIEM TRA THONG TIN
# =========================================================

if page == "🔎 Kiểm tra thông tin":

    st.markdown(
        """
        <div class="hero">
            <h1>🔎 Kiểm tra trước khi tin</h1>
            <p>
            Phân tích dấu hiệu đáng chú ý, luyện cách kiểm chứng
            và suy nghĩ phản biện trước khi chia sẻ thông tin.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("### Nội dung cần phân tích")

        sample_name = st.selectbox(
            "Hoặc chọn một nội dung mẫu",
            ["Tự nhập nội dung"] + list(SAMPLES.keys()),
        )

        default_text = ""
        if sample_name in SAMPLES:
            default_text = SAMPLES[sample_name]

        content = st.text_area(
            "Dán nội dung bài đăng hoặc tin nhắn tại đây",
            value=default_text,
            height=210,
            placeholder=(
                "Ví dụ: một tin nhắn yêu cầu chuyển tiền, "
                "một bài đăng chưa rõ nguồn..."
            ),
            help=(
                "Không nhập mật khẩu, mã OTP, số tài khoản "
                "hoặc dữ liệu cá nhân nhạy cảm."
            ),
        )

        st.caption(
            "Lưu ý: ứng dụng đánh giá nội dung được nhập, "
            "không tự động xác minh sự thật trên Internet."
        )

        col1, col2 = st.columns(2)

        with col1:
            analyze_ai = st.button(
                "✨ Phân tích bằng AI",
                type="primary",
                use_container_width=True,
            )

        with col2:
            analyze_rules = st.button(
                "🧠 Kiểm tra quy tắc",
                use_container_width=True,
            )

    with right:
        st.markdown("### Quy trình kiểm chứng")
        st.markdown(
            """
            <div class="panel">
                <b>01 · Quan sát</b>
                <p class="muted">Đọc kỹ nội dung và tìm dấu hiệu bất thường.</p>
                <hr>
                <b>02 · Đối chiếu</b>
                <p class="muted">Tìm nguồn gốc và nguồn độc lập đáng tin cậy.</p>
                <hr>
                <b>03 · Quyết định</b>
                <p class="muted">Chưa đủ bằng chứng thì chưa vội tin hoặc chia sẻ.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "AI có thể sai. Kết quả là gợi ý giáo dục, "
            "không phải bằng chứng xác thực cuối cùng."
        )

    if analyze_ai:
        if not content.strip():
            st.warning("Em hãy nhập nội dung cần phân tích trước nhé.")
        else:
            with st.spinner("Đang phân tích bằng Gemini..."):
                result, error = ask_gemini(content)

            if error:
                st.error(error)
                st.caption(
                    "Em vẫn có thể dùng chức năng kiểm tra quy tắc "
                    "trong lúc khắc phục kết nối AI."
                )
            else:
                st.markdown("### ✨ Kết quả phân tích AI")
                st.markdown(
                    '<div class="panel">',
                    unsafe_allow_html=True,
                )
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)

                save_history(
                    content,
                    "Gemini AI",
                    result,
                    "AI phân tích sơ bộ",
                )

    if analyze_rules:
        if not content.strip():
            st.warning("Em hãy nhập nội dung cần kiểm tra trước nhé.")
        else:
            result = rule_analysis(content)

            st.markdown("### 🧠 Kết quả kiểm tra quy tắc")

            metric_col1, metric_col2 = st.columns(2)
            metric_col1.metric("Nhóm dấu hiệu", result["score"])
            metric_col2.metric("Đánh giá sơ bộ", result["level"])

            if result["found"]:
                for item in result["found"]:
                    with st.expander(item["category"], expanded=True):
                        st.write(
                            "Từ khóa hoặc dấu hiệu:",
                            ", ".join(item["matches"]),
                        )
            else:
                st.info(
                    "Bộ quy tắc chưa phát hiện dấu hiệu trong "
                    "danh sách. Điều này không chứng minh nội dung đúng."
                )

            st.warning(
                "Đây là bộ quy tắc từ khóa đơn giản, không phải "
                "mô hình AI đã được huấn luyện và không thể tự "
                "xác minh tính đúng sai của thông tin."
            )

            save_history(
                content,
                "Bộ quy tắc",
                str(result),
                result["level"],
            )


# =========================================================
# 7. TRANG THU TINH HUONG
# =========================================================

elif page == "🧩 Thử tình huống":

    st.markdown(
        """
        <div class="hero">
            <h1>🧩 Phòng thực hành tư duy phản biện</h1>
            <p>
            Thử xử lý các tình huống giả lập và học cách
            xác minh thông tin an toàn.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = len(SCENARIOS)

    index = st.session_state.scenario_index % total
    scenario = SCENARIOS[index]

    st.progress((index + 1) / total)
    st.caption(f"Tình huống {index + 1}/{total}")

    st.markdown(
        f"""
        <div class="panel">
            <h3>{scenario['title']}</h3>
            <p>{scenario['content']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form(f"scenario_form_{index}"):
        answer = st.radio(
            scenario["question"],
            scenario["options"],
            index=None,
        )
        submitted = st.form_submit_button(
            "Kiểm tra lựa chọn",
            type="primary",
        )

    if submitted:
        if answer is None:
            st.warning("Em hãy chọn một phương án trước nhé.")
        else:
            selected = scenario["options"].index(answer)
            correct = selected == scenario["answer"]

            if correct:
                st.success("Chính xác! Em đã chọn phương án phù hợp.")
            else:
                st.info(
                    "Mình cùng xem lại nhé. "
                    "Đáp án phù hợp hơn là: "
                    + scenario["options"][scenario["answer"]]
                )

            st.write(scenario["explain"])

            st.session_state.scenario_results.append({
                "Tình huống": scenario["title"],
                "Đúng": correct,
            })

    col_prev, col_next = st.columns(2)

    with col_prev:
        if st.button("← Tình huống trước", use_container_width=True):
            st.session_state.scenario_index = (index - 1) % total
            st.rerun()

    with col_next:
        if st.button("Tình huống tiếp theo →", use_container_width=True):
            st.session_state.scenario_index = (index + 1) % total
            st.rerun()

    if st.session_state.scenario_results:
        correct_count = sum(
            item["Đúng"]
            for item in st.session_state.scenario_results
        )
        attempt_count = len(st.session_state.scenario_results)

        st.divider()
        st.metric(
            "Kết quả các lượt đã trả lời",
            f"{correct_count}/{attempt_count}",
        )


# =========================================================
# 8. TRANG KHAO SAT
# =========================================================

elif page == "📝 Khảo sát nhanh":

    st.markdown(
        """
        <div class="hero">
            <h1>📝 Khảo sát hành vi xác thực thông tin</h1>
            <p>
            Khảo sát phục vụ nghiên cứu giáo dục về cách học sinh
            đánh giá thông tin trên môi trường số.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "Không nhập họ tên, số điện thoại, địa chỉ, mật khẩu "
        "hoặc thông tin nhận dạng cá nhân. Em có thể bỏ qua khảo sát."
    )

    with st.form("survey_form"):
        q1 = st.radio(
            "1. Khi thấy một tin gây sốc trên mạng, em thường làm gì?",
            [
                "Chia sẻ ngay",
                "Đọc nội dung rồi tự đánh giá",
                "Tìm nguồn khác để đối chiếu",
                "Bỏ qua",
            ],
        )

        q2 = st.radio(
            "2. Em thường kiểm tra nguồn tin ở mức nào?",
            [
                "Hầu như không",
                "Đôi khi",
                "Thường xuyên",
                "Gần như luôn luôn",
            ],
        )

        q3 = st.radio(
            "3. Điều gì khiến em dễ tin một bài đăng?",
            [
                "Nhiều lượt thích và chia sẻ",
                "Người quen gửi",
                "Có nguồn đáng tin cậy và bằng chứng",
                "Tiêu đề gây chú ý",
            ],
        )

        q4 = st.radio(
            "4. Em có muốn dùng công cụ giúp kiểm tra thông tin không?",
            [
                "Có",
                "Chưa chắc",
                "Không",
            ],
        )

        submitted = st.form_submit_button(
            "Gửi câu trả lời",
            type="primary",
        )

    if submitted:
        st.session_state.survey.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Hành vi khi thấy tin": q1,
            "Tần suất kiểm tra": q2,
            "Yếu tố ảnh hưởng": q3,
            "Nhu cầu công cụ": q4,
        })
        st.success(
            "Câu trả lời đã được ghi nhận trong phiên sử dụng hiện tại."
        )
        st.caption(
            "Dữ liệu hiện chưa tự động lưu lên máy chủ hoặc cơ sở dữ liệu."
        )


# =========================================================
# 9. TRANG LICH SU VA THONG KE
# =========================================================

elif page == "📊 Lịch sử & thống kê":

    st.markdown(
        """
        <div class="hero">
            <h1>📊 Lịch sử & thống kê nghiên cứu</h1>
            <p>
            Theo dõi dữ liệu trong phiên sử dụng và xuất dữ liệu
            để phục vụ việc tổng hợp kết quả nghiên cứu.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    history = st.session_state.history
    surveys = st.session_state.survey
    scenario_results = st.session_state.scenario_results

    col1, col2, col3 = st.columns(3)

    col1.metric("Lượt phân tích", len(history))
    col2.metric("Phiếu khảo sát", len(surveys))
    col3.metric("Lượt làm tình huống", len(scenario_results))

    st.divider()

    if history:
        st.markdown("### Lịch sử phân tích")

        df_history = pd.DataFrame(history)
        st.dataframe(
            df_history,
            use_container_width=True,
            hide_index=True,
        )

        csv_history = df_history.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ Tải lịch sử phân tích CSV",
            data=csv_history,
            file_name="social_sandbox_history.csv",
            mime="text/csv",
        )
    else:
        st.info(
            "Chưa có lịch sử phân tích trong phiên hiện tại. "
            "Hãy thử kiểm tra một nội dung trước nhé."
        )

    if surveys:
        st.markdown("### Dữ liệu khảo sát")

        df_survey = pd.DataFrame(surveys)
        st.dataframe(
            df_survey,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Tải dữ liệu khảo sát CSV",
            data=df_survey.to_csv(index=False).encode("utf-8-sig"),
            file_name="social_sandbox_survey.csv",
            mime="text/csv",
        )

        st.markdown("#### Tần suất xác thực thông tin")
        counts = (
            df_survey["Tần suất kiểm tra"]
            .value_counts()
            .rename_axis("Tần suất")
            .reset_index(name="Số câu trả lời")
        )

        st.bar_chart(
            counts.set_index("Tần suất"),
            use_container_width=True,
        )
    else:
        st.info("Chưa có dữ liệu khảo sát trong phiên này.")

    st.warning(
        "Dữ liệu đang được lưu trong session của ứng dụng. "
        "Dữ liệu có thể mất khi phiên kết thúc hoặc ứng dụng khởi động lại. "
        "Đây chưa phải hệ thống lưu trữ nghiên cứu lâu dài."
    )


# =========================================================
# 10. TRANG GIOI THIEU
# =========================================================

elif page == "ℹ️ Về đề tài":

    st.markdown(
        """
        <div class="hero">
            <h1>🛡️ Social Sandbox AI</h1>
            <p>
            Môi trường mô phỏng giúp học sinh rèn luyện hành vi
            xác thực thông tin số và tư duy phản biện.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Tên đề tài nghiên cứu")

    st.markdown(
        """
        **Nghiên cứu hành vi xác thực thông tin số của học sinh
        trung học và xây dựng hệ thống can thiệp thích ứng
        ứng dụng trí tuệ nhân tạo.**
        """
    )

    st.markdown("### Mục tiêu")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="panel">
                <h4>🔎 Phân tích nội dung</h4>
                <p class="muted">
                Gợi ý các dấu hiệu cần chú ý và giải thích
                vì sao người đọc nên kiểm tra thêm.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="panel">
                <h4>🧠 Rèn luyện tư duy</h4>
                <p class="muted">
                Đưa ra tình huống mô phỏng và câu hỏi
                giúp học sinh tự suy nghĩ.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="panel">
                <h4>🧭 Hướng dẫn kiểm chứng</h4>
                <p class="muted">
                Khuyến khích đối chiếu nguồn và tìm
                bằng chứng độc lập trước khi chia sẻ.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="panel">
                <h4>📊 Hỗ trợ nghiên cứu</h4>
                <p class="muted">
                Tổng hợp lịch sử trong phiên và xuất
                dữ liệu khảo sát để phân tích.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Giới hạn và quyền riêng tư")

    st.write(
        "- Kết quả AI có thể sai và cần được kiểm chứng độc lập."
    )
    st.write(
        "- Ứng dụng không tự động xác minh website hoặc "
        "tính xác thực của nguồn trực tuyến."
    )
    st.write(
        "- Bộ quy tắc từ khóa chỉ là công cụ hỗ trợ đơn giản, "
        "không phải mô hình đã được huấn luyện."
    )
    st.write(
        "- Không nhập mật khẩu, mã OTP hoặc dữ liệu cá nhân nhạy cảm."
    )
    st.write(
        "- Dữ liệu hiện chỉ được lưu trong phiên ứng dụng; "
        "chưa có cơ sở dữ liệu lâu dài."
    )

    st.caption(
        "Social Sandbox AI · Công cụ hỗ trợ giáo dục và nghiên cứu."
    )


# =========================================================
# 11. CHAN TRANG
# =========================================================

st.divider()
st.caption(
    "🛡️ Social Sandbox AI | Hãy kiểm tra nguồn, "
    "đối chiếu bằng chứng và suy nghĩ trước khi chia sẻ."
)
