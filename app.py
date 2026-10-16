
import re
import html
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
import streamlit as st

# =========================================================
# SOCIAL SANDBOX AI
# Công cụ hỗ trợ xác thực thông tin số cho học sinh
# =========================================================

PROJECT_TITLE = (
    "Nghiên cứu hành vi xác thực thông tin số của học sinh "
    "trung học và xây dựng hệ thống can thiệp thích ứng "
    "ứng dụng trí tuệ nhân tạo"
)

st.set_page_config(
    page_title="Xác thực thông tin số | Social Sandbox AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------- GIAO DIỆN ---------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg: #0b1020;
    --panel: #141d32;
    --line: #2b3a57;
    --text: #edf2ff;
    --muted: #a8b5ce;
    --purple: #a78bfa;
    --cyan: #67e8f9;
}

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 90% 0%, #292650 0, transparent 34%),
        linear-gradient(135deg, #080d19, #10182b);
    color: var(--text);
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', 'Be Vietnam Pro', sans-serif !important;
    letter-spacing: -0.025em;
}

.hero {
    padding: 30px;
    border-radius: 24px;
    border: 1px solid #474779;
    background: linear-gradient(120deg, #202344, #122738);
    margin-bottom: 22px;
}

.hero-label {
    color: var(--cyan);
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero h1 {
    color: white;
    font-size: clamp(27px, 4vw, 43px);
    line-height: 1.25;
    margin: 12px 0;
}

.hero p {
    color: #c5d0e5;
    line-height: 1.8;
}

.panel {
    padding: 20px;
    border-radius: 18px;
    background: rgba(20, 29, 50, 0.92);
    border: 1px solid var(--line);
    margin-bottom: 12px;
}

.muted {
    color: var(--muted);
    font-size: 13px;
}

.pill {
    display: inline-block;
    background: #222d49;
    color: #d8ddff;
    border: 1px solid #3a496a;
    padding: 5px 10px;
    margin: 3px;
    border-radius: 30px;
    font-size: 12px;
}

.result-high {
    padding: 20px;
    border-radius: 17px;
    border: 1px solid #fb7185;
    background: rgba(251, 113, 133, 0.10);
}

.result-medium {
    padding: 20px;
    border-radius: 17px;
    border: 1px solid #fbbf24;
    background: rgba(251, 191, 36, 0.09);
}

.result-low {
    padding: 20px;
    border-radius: 17px;
    border: 1px solid #34d399;
    background: rgba(52, 211, 153, 0.08);
}

div.stButton > button,
div.stDownloadButton > button {
    min-height: 44px;
    border-radius: 12px;
    font-weight: 700;
}

div[data-testid="stMetric"] {
    background: rgba(20, 29, 50, 0.9);
    border: 1px solid var(--line);
    padding: 15px;
    border-radius: 15px;
}

section[data-testid="stSidebar"] {
    background: #0b1222;
    border-right: 1px solid var(--line);
}

hr {
    border-color: var(--line);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# --------------------- DỮ LIỆU PHIÊN ---------------------

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "draft" not in st.session_state:
    st.session_state.draft = ""

if "quiz_before" not in st.session_state:
    st.session_state.quiz_before = None

if "quiz_after" not in st.session_state:
    st.session_state.quiz_after = None

if "survey_history" not in st.session_state:
    st.session_state.survey_history = []


# --------------------- BỘ QUY TẮC ---------------------

RULES = [
    {
        "name": "Yêu cầu OTP hoặc mật khẩu",
        "keywords": [
            "mã otp", "otp", "mã xác thực", "mã xác minh",
            "mật khẩu", "password", "mã pin"
        ],
        "weight": 28,
        "reason": "Thông tin xác thực có thể bị lợi dụng để chiếm quyền truy cập tài khoản."
    },
    {
        "name": "Thúc ép chuyển tiền",
        "keywords": [
            "chuyển khoản ngay", "chuyển tiền ngay",
            "nạp tiền trước", "đóng phí", "phí nhận quà",
            "phí xác minh", "đặt cọc trước", "phí giải ngân"
        ],
        "weight": 25,
        "reason": "Yêu cầu chuyển tiền gấp hoặc trả phí trước cần được xác minh độc lập."
    },
    {
        "name": "Trúng thưởng hoặc quà tặng bất ngờ",
        "keywords": [
            "trúng thưởng", "bạn đã trúng", "nhận quà miễn phí",
            "nhận giải thưởng", "chúc mừng bạn đã trúng",
            "nhận thưởng", "phí nhận thưởng"
        ],
        "weight": 18,
        "reason": "Thông báo phần thưởng bất ngờ có thể được dùng để dụ người nhận chuyển tiền."
    },
    {
        "name": "Đầu tư lợi nhuận cao",
        "keywords": [
            "cam kết lợi nhuận", "lãi chắc chắn",
            "không rủi ro", "lợi nhuận 100%",
            "nhân đôi tài khoản", "lãi khủng",
            "lợi nhuận bảo đảm"
        ],
        "weight": 25,
        "reason": "Lời hứa lợi nhuận cao và chắc chắn là dấu hiệu cần kiểm tra."
    },
    {
        "name": "Giả danh ngân hàng hoặc cơ quan",
        "keywords": [
            "tài khoản bị khóa", "xác minh tài khoản",
            "công an yêu cầu", "cơ quan chức năng",
            "vi phạm pháp luật", "ngân hàng thông báo",
            "cơ quan thuế", "tài khoản ngân hàng"
        ],
        "weight": 18,
        "reason": "Kẻ gian có thể giả danh tổ chức đáng tin để tạo áp lực hoặc lấy dữ liệu."
    },
    {
        "name": "Tuyển dụng hoặc việc làm đáng ngờ",
        "keywords": [
            "việc nhẹ lương cao", "nạp tiền làm nhiệm vụ",
            "tuyển cộng tác viên", "nhận hoa hồng",
            "chốt đơn nhận tiền", "không cần kinh nghiệm",
            "làm nhiệm vụ nhận tiền"
        ],
        "weight": 20,
        "reason": "Cần cảnh giác nếu công việc yêu cầu nạp tiền, đặt cọc hoặc trả phí."
    },
    {
        "name": "Giả danh người quen hoặc mượn tiền",
        "keywords": [
            "mượn tiền gấp", "đang cấp cứu",
            "đừng gọi lại", "giữ bí mật",
            "chuyển tiền giúp", "đang rất cần tiền"
        ],
        "weight": 22,
        "reason": "Tài khoản người quen có thể bị chiếm quyền. Hãy xác minh qua kênh khác."
    },
    {
        "name": "Mua bán trực tuyến đáng ngờ",
        "keywords": [
            "thanh toán ngoài nền tảng",
            "chuyển khoản để giữ hàng",
            "giá rẻ bất thường",
            "phí giao hàng hoàn tiền",
            "hoàn tiền đơn hàng",
            "phí ship nhận hàng"
        ],
        "weight": 16,
        "reason": "Cần kiểm tra người bán và phương thức thanh toán trước khi giao dịch."
    },
    {
        "name": "Vay tiền và phí trước",
        "keywords": [
            "phí giải ngân", "phí mở hồ sơ",
            "vay nhanh", "xóa nợ xấu",
            "vay không cần gặp mặt", "duyệt vay ngay"
        ],
        "weight": 20,
        "reason": "Cần xác minh đơn vị cho vay và điều khoản trước khi cung cấp dữ liệu."
    },
    {
        "name": "Thúc ép hoặc đe dọa",
        "keywords": [
            "ngay lập tức", "khẩn cấp",
            "sắp hết hạn", "trong 5 phút",
            "nếu không sẽ", "lần cuối",
            "không làm sẽ bị khóa"
        ],
        "weight": 12,
        "reason": "Ngôn ngữ gây áp lực có thể khiến người nhận quyết định vội vàng."
    },
    {
        "name": "Ứng dụng hoặc quyền truy cập lạ",
        "keywords": [
            "tải file apk", "chia sẻ màn hình",
            "điều khiển từ xa", "cấp quyền truy cập",
            "cài ứng dụng lạ", "cài app theo hướng dẫn"
        ],
        "weight": 22,
        "reason": "Ứng dụng hoặc quyền điều khiển từ xa không rõ nguồn có thể làm lộ dữ liệu."
    },
]

URL_PATTERN = re.compile(
    r'https?://[^\s<>"\']+|www\.[^\s<>"\']+',
    re.IGNORECASE
)

SUSPICIOUS_TLDS = (
    ".top", ".xyz", ".click", ".work",
    ".monster", ".zip", ".country"
)


# --------------------- PHÂN TÍCH NỘI DUNG ---------------------

def analyze_content(text):
    raw = text.strip()
    low = raw.lower()

    findings = []
    score = 0

    for rule in RULES:
        hits = [
            keyword for keyword in rule["keywords"]
            if keyword in low
        ]

        if hits:
            findings.append({
                "name": rule["name"],
                "hits": hits[:5],
                "reason": rule["reason"],
                "weight": rule["weight"],
            })
            score += rule["weight"]

    urls = URL_PATTERN.findall(raw)
    url_results = []

    for found_url in urls:
        candidate = found_url.rstrip(".,;:!?)\"]}")
        normalized = (
            candidate if candidate.lower().startswith(
                ("http://", "https://")
            ) else "https://" + candidate
        )

        parsed = urlparse(normalized)
        host = (parsed.hostname or "").lower()
        url_flags = []

        if parsed.scheme == "http":
            url_flags.append(
                "Sử dụng HTTP không mã hóa; không nhập thông tin nhạy cảm."
            )
            score += 8

        if host:
            if host.startswith("xn--") or ".xn--" in host:
                url_flags.append("Tên miền có dạng mã hóa ký tự.")
                score += 15

            if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
                url_flags.append(
                    "Đuôi tên miền cần được xác minh kỹ."
                )
                score += 8

            if re.search(r"\d{5,}", host):
                url_flags.append("Tên miền chứa chuỗi số dài.")
                score += 6

            if host.count("-") >= 2:
                url_flags.append("Tên miền có nhiều dấu gạch nối.")
                score += 5

            if not url_flags:
                url_flags.append(
                    "Chưa phát hiện dấu hiệu rõ ràng từ kiểm tra URL cơ bản."
                )

        url_results.append({
            "url": candidate,
            "host": host or "Không xác định",
            "flags": url_flags,
        })

    score = min(100, score)

    if score >= 55:
        level = "Cảnh báo cao"
        css = "result-high"
        headline = "Có nhiều dấu hiệu cần cảnh giác"
        advice = (
            "Tạm dừng thao tác. Không chuyển tiền, không nhập OTP hoặc "
            "mật khẩu, không tải tệp và không cấp quyền truy cập. "
            "Hãy xác minh qua kênh chính thức do em tự tìm."
        )
    elif score >= 25:
        level = "Cần kiểm tra thêm"
        css = "result-medium"
        headline = "Nội dung có dấu hiệu đáng ngờ"
        advice = (
            "Chưa nên làm theo ngay. Kiểm tra nguồn gửi, địa chỉ website "
            "và đối chiếu thông tin qua một nguồn độc lập."
        )
    else:
        level = "Chưa thấy nhiều dấu hiệu"
        css = "result-low"
        headline = "Chưa phát hiện nhiều dấu hiệu theo bộ quy tắc"
        advice = (
            "Điều này không chứng minh nội dung an toàn. Hãy xác minh "
            "nguồn, kiểm tra đường link và tránh chia sẻ dữ liệu nhạy cảm."
        )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "css": css,
        "headline": headline,
        "advice": advice,
        "score": score,
        "findings": findings,
        "urls": url_results,
        "preview": raw[:200],
    }


def save_history(result):
    st.session_state.history.insert(0, {
        "Thời gian": result["timestamp"],
        "Kết quả": result["level"],
        "Điểm quy tắc": result["score"],
        "Nội dung rút gọn": result["preview"],
    })


# --------------------- MENU ---------------------

with st.sidebar:
    st.markdown("## 🛡️ Social Sandbox AI")
    st.caption("Công cụ xác thực thông tin số")

    page = st.radio(
        "MENU",
        [
            "🔎 Kiểm tra thông tin",
            "🧩 Thử tình huống",
            "📝 Khảo sát nhanh",
            "📊 Lịch sử & thống kê",
            "ℹ️ Về đề tài",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### 🔐 Lưu ý an toàn")
    st.caption(
        "Không nhập OTP, mật khẩu, số thẻ, địa chỉ nhà "
        "hoặc thông tin cá nhân thật."
    )
    st.caption(
        "Kết quả chỉ mang tính tham khảo, không phải kết luận chắc chắn."
    )


# --------------------- HEADER ---------------------

st.markdown(f"""
<div class="hero">
    <div class="hero-label">DIGITAL SAFETY · SOCIAL SANDBOX AI</div>
    <h1>Kiểm tra trước khi bạn bấm.</h1>
    <p>{html.escape(PROJECT_TITLE)}</p>
    <p>
        Dán tin nhắn, nội dung bài đăng hoặc đường link để tìm dấu hiệu
        đáng ngờ và xem hướng dẫn xác minh tiếp theo.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------- TRANG 1: KIỂM TRA ---------------------

if page == "🔎 Kiểm tra thông tin":

    st.subheader("🔍 Kiểm tra nội dung đáng ngờ")

    st.write(
        "Chỉ cần dán nội dung cần kiểm tra, sau đó nhấn nút phân tích."
    )

    examples = {
        "Tự nhập nội dung": "",
        "Giả danh ngân hàng": (
            "Tài khoản của bạn sẽ bị khóa. Hãy xác minh tài khoản "
            "và nhập mã OTP ngay lập tức tại đường link lạ."
        ),
        "Tuyển cộng tác viên": (
            "Tuyển cộng tác viên làm nhiệm vụ nhận hoa hồng. "
            "Việc nhẹ lương cao, nạp tiền trước để mở nhiệm vụ."
        ),
        "Thông báo trúng thưởng": (
            "Chúc mừng bạn đã trúng thưởng điện thoại! "
            "Bấm link nhận quà và đóng phí nhận thưởng hôm nay."
        ),
        "Mượn tiền khẩn cấp": (
            "Mình đang cấp cứu, mượn tiền gấp giúp mình. "
            "Đừng gọi lại, chuyển khoản ngay nhé."
        ),
        "Mua bán trực tuyến": (
            "Giá rẻ bất thường, chuyển khoản để giữ hàng. "
            "Thanh toán ngoài nền tảng để được giảm giá."
        ),
        "Đầu tư lợi nhuận cao": (
            "Cam kết lợi nhuận 100%, không rủi ro. "
            "Nạp tiền ngay để nhân đôi tài khoản."
        ),
        "Vay tiền trực tuyến": (
            "Duyệt vay ngay, phí giải ngân và phí mở hồ sơ "
            "cần được thanh toán trước."
        ),
    }

    choice = st.selectbox(
        "Thử một nội dung mẫu",
        list(examples.keys()),
    )

    if choice != "Tự nhập nội dung":
        st.session_state.draft = examples[choice]

    content = st.text_area(
        "Nội dung cần kiểm tra",
        key="draft",
        height=180,
        placeholder=(
            "Dán tin nhắn, bài đăng hoặc đường link tại đây..."
        ),
    )

    col1, col2 = st.columns(2)

    with col1:
        analyze = st.button(
            "✨ Phân tích ngay",
            type="primary",
            use_container_width=True,
        )

    with col2:
        clear = st.button(
            "🗑️ Xóa nội dung",
            use_container_width=True,
        )

    if clear:
        st.session_state.draft = ""
        st.session_state.last_result = None
        st.rerun()

    if analyze:
        if not content.strip():
            st.warning("Em hãy nhập hoặc chọn nội dung mẫu trước nhé.")
        else:
            result = analyze_content(content)
            st.session_state.last_result = result
            save_history(result)

    result = st.session_state.last_result

    if result:
        st.divider()
        st.subheader("📋 Kết quả kiểm tra")

        st.markdown(
            f"""
            <div class="{result['css']}">
                <div class="pill">{html.escape(result['level'])}</div>
                <h3>{html.escape(result['headline'])}</h3>
                <p>{html.escape(result['advice'])}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Mức cảnh báo", result["level"])
        c2.metric("Điểm quy tắc", f"{result['score']}/100")
        c3.metric("Nhóm dấu hiệu", len(result["findings"]))

        st.caption(
            "Điểm này là điểm quy tắc nội bộ, không phải xác suất "
            "nội dung là lừa đảo."
        )

        st.markdown("### ⚠️ Dấu hiệu được phát hiện")

        if result["findings"]:
            for finding in result["findings"]:
                with st.expander(f"🔎 {finding['name']}"):
                    st.write(finding["reason"])
                    st.write(
                        "**Cụm từ khớp:** "
                        + ", ".join(finding["hits"])
                    )
        else:
            st.info(
                "Bộ quy tắc chưa tìm thấy cụm từ phổ biến đáng chú ý. "
                "Lừa đảo vẫn có thể sử dụng cách diễn đạt khác."
            )

        if result["urls"]:
            st.markdown("### 🌐 Kiểm tra đường link")

            for url_info in result["urls"]:
                st.markdown(f"**{url_info['url']}**")
                st.caption("Tên miền: " + url_info["host"])

                for flag in url_info["flags"]:
                    st.write("• " + flag)

            st.warning(
                "Không mở link đáng ngờ chỉ để thử. Hãy tự tìm "
                "website hoặc ứng dụng chính thức để xác minh."
            )

        st.markdown("### ✅ Em nên làm gì tiếp theo?")

        st.markdown("""
        1. **Dừng lại:** Không chuyển tiền, nhập OTP hay mật khẩu.
        2. **Xác minh:** Tự tìm kênh liên hệ chính thức của tổ chức.
        3. **Đối chiếu:** Kiểm tra thông tin từ nguồn độc lập.
        4. **Hỏi người đáng tin:** Nhờ phụ huynh hoặc giáo viên nếu còn phân vân.
        """)

        with st.expander("Về cách hệ thống phân tích"):
            st.write(
                "Phiên bản hiện tại dùng bộ quy tắc và từ khóa mở rộng, "
                "kèm một số kiểm tra URL đơn giản. Hệ thống chưa kết nối "
                "mô hình AI lớn hoặc cơ sở dữ liệu xác minh thời gian thực. "
                "Có thể xảy ra cảnh báo nhầm hoặc bỏ sót."
            )

    else:
        st.markdown("""
        <div class="panel">
            <h3>🛡️ Bốn bước bảo vệ bản thân</h3>
            <span class="pill">Dừng lại</span>
            <span class="pill">Kiểm tra nguồn</span>
            <span class="pill">Đối chiếu thông tin</span>
            <span class="pill">Quyết định an toàn</span>
            <p class="muted">
                Công cụ hỗ trợ nhận diện dấu hiệu, không thay thế
                việc xác minh thông tin từ nguồn chính thức.
            </p>
        </div>
        """, unsafe_allow_html=True)


# --------------------- TRANG 2: TÌNH HUỐNG ---------------------

elif page == "🧩 Thử tình huống":

    st.subheader("🧩 Luyện tập nhận diện lừa đảo")
    st.write("Chọn cách xử lý an toàn nhất trong mỗi tình huống.")

    cases = [
        {
            "title": "Tin nhắn ngân hàng",
            "text": "Tin nhắn yêu cầu nhập OTP qua đường link lạ.",
            "options": [
                "Nhập OTP ngay",
                "Mở ứng dụng ngân hàng chính thức để kiểm tra",
                "Gửi OTP cho người gửi tin nhắn",
            ],
            "answer": 1,
            "why": "Không cung cấp OTP qua link trong tin nhắn. Hãy tự mở ứng dụng hoặc liên hệ ngân hàng qua kênh chính thức.",
        },
        {
            "title": "Việc làm online",
            "text": "Công việc yêu cầu nạp tiền trước để mở nhiệm vụ nhận hoa hồng.",
            "options": [
                "Nạp tiền để thử",
                "Gửi thông tin cá nhân ngay",
                "Dừng lại và xác minh đơn vị tuyển dụng",
            ],
            "answer": 2,
            "why": "Yêu cầu trả tiền trước để nhận việc hoặc hoa hồng là dấu hiệu cần cảnh giác.",
        },
        {
            "title": "Người quen mượn tiền",
            "text": "Một tài khoản quen thuộc xin tiền gấp và bảo đừng gọi lại.",
            "options": [
                "Chuyển tiền ngay",
                "Xác minh qua số điện thoại hoặc kênh khác đã biết",
                "Gửi mã xác thực cho họ",
            ],
            "answer": 1,
            "why": "Tài khoản người quen có thể bị chiếm quyền. Hãy xác minh bằng một kênh khác.",
        },
        {
            "title": "Trúng thưởng",
            "text": "Một tin nhắn báo trúng quà nhưng yêu cầu trả phí nhận quà.",
            "options": [
                "Thanh toán phí ngay",
                "Kiểm tra thể lệ và nguồn thông báo chính thức",
                "Cung cấp mật khẩu để nhận quà",
            ],
            "answer": 1,
            "why": "Không thanh toán hoặc cung cấp thông tin nhạy cảm chỉ vì một thông báo trúng thưởng bất ngờ.",
        },
    ]

    titles = [case["title"] for case in cases]
    selected = st.selectbox("Chọn tình huống", titles)
    case = cases[titles.index(selected)]

    st.markdown(
        f"""
        <div class="panel">
            <div class="pill">TÌNH HUỐNG MÔ PHỎNG</div>
            <h3>{html.escape(case['title'])}</h3>
            <p>{html.escape(case['text'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    answer = st.radio(
        "Em sẽ làm gì?",
        case["options"],
        key="answer_" + str(titles.index(selected)),
    )

    if st.button("Kiểm tra lựa chọn", type="primary"):
        index = case["options"].index(answer)

        if index == case["answer"]:
            st.success("Chính xác! " + case["why"])
        else:
            st.warning("Hãy thử suy nghĩ lại. " + case["why"])


# --------------------- TRANG 3: KHẢO SÁT ---------------------

elif page == "📝 Khảo sát nhanh":

    st.subheader("📝 Khảo sát kỹ năng xác thực thông tin")
    st.write(
        "Bài khảo sát ngắn phục vụ trải nghiệm nghiên cứu. "
        "Không cần cung cấp tên hoặc thông tin cá nhân."
    )

    mode = st.radio(
        "Thời điểm",
        ["Trước trải nghiệm", "Sau trải nghiệm"],
        horizontal=True,
    )

    questions = [
        {
            "q": "Tin nhắn yêu cầu OTP qua đường link lạ. Em nên:",
            "opts": [
                "Nhập ngay",
                "Không cung cấp OTP và xác minh qua kênh chính thức",
                "Gửi OTP cho bạn",
            ],
            "ans": 1,
        },
        {
            "q": "Một công việc online yêu cầu nạp tiền trước. Em nên:",
            "opts": [
                "Nạp một khoản nhỏ",
                "Xác minh đơn vị và không chuyển tiền khi chưa rõ",
                "Làm theo ngay",
            ],
            "ans": 1,
        },
        {
            "q": "Người quen nhắn mượn tiền gấp và bảo đừng gọi. Em nên:",
            "opts": [
                "Chuyển tiền ngay",
                "Đăng công khai tin nhắn",
                "Xác minh qua kênh khác",
            ],
            "ans": 2,
        },
        {
            "q": "Website có tên gần giống thương hiệu quen thuộc. Em nên:",
            "opts": [
                "Tin ngay",
                "Kiểm tra tên miền và dùng kênh chính thức",
                "Nhập thử mật khẩu",
            ],
            "ans": 1,
        },
        {
            "q": "Kết quả cảnh báo thấp có nghĩa là:",
            "opts": [
                "Chắc chắn an toàn",
                "Không cần kiểm tra thêm",
                "Chưa thấy nhiều dấu hiệu theo quy tắc, vẫn cần xác minh",
            ],
            "ans": 2,
        },
    ]

    with st.form("survey"):
        answers = []

        for i, question in enumerate(questions):
            st.markdown(f"**Câu {i + 1}. {question['q']}**")
            answers.append(
                st.radio(
                    "Chọn đáp án",
                    question["opts"],
                    key=f"survey_{mode}_{i}",
                    label_visibility="collapsed",
                )
            )

        submitted = st.form_submit_button(
            "Chấm điểm khảo sát",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        correct = sum(
            1
            for i, question in enumerate(questions)
            if answers[i] == question["opts"][question["ans"]]
        )

        score = round(correct / len(questions) * 100)

        if mode == "Trước trải nghiệm":
            st.session_state.quiz_before = score
        else:
            st.session_state.quiz_after = score

        st.session_state.survey_history.append({
            "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Thời điểm": mode,
            "Số câu đúng": correct,
            "Tổng câu": len(questions),
            "Điểm": score,
        })

        st.success(
            f"Em trả lời đúng {correct}/{len(questions)} câu — {score}/100."
        )

    c1, c2 = st.columns(2)

    c1.metric(
        "Điểm trước trải nghiệm",
        "—" if st.session_state.quiz_before is None
        else f"{st.session_state.quiz_before}/100",
    )

    c2.metric(
        "Điểm sau trải nghiệm",
        "—" if st.session_state.quiz_after is None
        else f"{st.session_state.quiz_after}/100",
    )

    if (
        st.session_state.quiz_before is not None
        and st.session_state.quiz_after is not None
    ):
        difference = (
            st.session_state.quiz_after - st.session_state.quiz_before
        )

        st.info(
            f"Chênh lệch điểm: {difference:+d} điểm phần trăm. "
            "Kết quả này không tự nó chứng minh quan hệ nhân quả."
        )

    st.caption(
        "Dữ liệu khảo sát chỉ lưu trong phiên ứng dụng hiện tại."
    )


# --------------------- TRANG 4: LỊCH SỬ ---------------------

elif page == "📊 Lịch sử & thống kê":

    st.subheader("📊 Lịch sử và thống kê")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)

        st.metric(
            "Số lượt kiểm tra nội dung",
            len(st.session_state.history),
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Tải lịch sử kiểm tra CSV",
            data=history_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="social_sandbox_history.csv",
            mime="text/csv",
        )

    else:
        st.info(
            "Chưa có lịch sử kiểm tra. Hãy phân tích một nội dung trước."
        )

    st.divider()
    st.markdown("### 📝 Kết quả khảo sát")

    if st.session_state.survey_history:
        survey_df = pd.DataFrame(
            st.session_state.survey_history
        )

        st.dataframe(
            survey_df,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "⬇️ Tải kết quả khảo sát CSV",
            data=survey_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="social_sandbox_survey.csv",
            mime="text/csv",
        )
    else:
        st.info("Chưa có kết quả khảo sát.")

    st.caption(
        "Dữ liệu hiện được lưu trong phiên sử dụng, chưa phải "
        "cơ sở dữ liệu lâu dài."
    )


# --------------------- TRANG 5: GIỚI THIỆU ---------------------

elif page == "ℹ️ Về đề tài":

    st.subheader("ℹ️ Giới thiệu đề tài")

    st.markdown(
        f"""
        <div class="panel">
            <div class="pill">ĐỀ TÀI NGHIÊN CỨU</div>
            <h3>{html.escape(PROJECT_TITLE)}</h3>
            <p>
                Xây dựng môi trường hỗ trợ học sinh luyện tập nhận diện
                dấu hiệu đáng ngờ, xác minh nguồn thông tin và suy nghĩ
                trước khi chia sẻ nội dung số.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="panel">
            <h3>🔎 Kiểm tra thông tin</h3>
            <p>Phân tích một số dấu hiệu ngôn ngữ và URL đáng ngờ.</p>
        </div>
        <div class="panel">
            <h3>🧩 Thực hành</h3>
            <p>Luyện tập qua các tình huống mô phỏng gần gũi.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="panel">
            <h3>📝 Khảo sát</h3>
            <p>Hỗ trợ quan sát kết quả trước và sau trải nghiệm.</p>
        </div>
        <div class="panel">
            <h3>📊 Thống kê</h3>
            <p>Xem lịch sử trong phiên và xuất dữ liệu CSV.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⚠️ Giới hạn của hệ thống")

    st.warning(
        "Phiên bản hiện tại sử dụng bộ quy tắc từ khóa và kiểm tra "
        "URL cơ bản. Chưa tích hợp mô hình AI lớn, chưa xác minh "
        "dữ liệu thời gian thực và có thể bỏ sót hoặc cảnh báo nhầm."
    )

    st.markdown("### 🔐 Nguyên tắc an toàn")

    st.markdown("""
    - Không nhập mật khẩu, OTP, số thẻ hoặc thông tin cá nhân thật.
    - Không xem điểm cảnh báo là xác suất lừa đảo.
    - Luôn xác minh qua kênh chính thức.
    - Khi nghiên cứu với học sinh, cần được cho phép phù hợp
      và bảo vệ dữ liệu người tham gia.
    """)


# --------------------- CHÂN TRANG ---------------------

st.divider()

st.markdown(
    f"""
    <p style="text-align:center; color:#9aa9c5; font-size:12px;">
        SOCIAL SANDBOX AI · XÁC THỰC THÔNG TIN SỐ<br>
        {html.escape(PROJECT_TITLE)}<br>
        Dừng lại · Kiểm tra · Suy nghĩ trước khi chia sẻ
    </p>
    """,
    unsafe_allow_html=True,
)

