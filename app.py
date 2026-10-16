
import re
import html
import random
from datetime import datetime
from urllib.parse import urlparse

import pandas as pd
import streamlit as st

# =========================================================
# SOCIAL SANDBOX AI
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
}

.hero h1 {
    color: white;
    font-size: clamp(27px, 4vw, 43px);
    line-height: 1.3;
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

.muted {
    color: var(--muted);
    font-size: 13px;
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


# =========================================================
# KHỞI TẠO DỮ LIỆU PHIÊN
# =========================================================

defaults = {
    "history": [],
    "last_result": None,
    "draft": "",
    "quiz_before": None,
    "quiz_after": None,
    "survey_history": [],
    "scenario_current": None,
    "scenario_seen": [],
    "scenario_answered": {},
    "scenario_feedback": {},
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# BỘ QUY TẮC PHÁT HIỆN DẤU HIỆU ĐÁNG NGỜ
# =========================================================

RULES = [
    {
        "name": "Yêu cầu OTP hoặc mật khẩu",
        "keywords": [
            "mã otp", "otp", "mã xác thực", "mã xác minh",
            "mật khẩu", "password", "mã pin"
        ],
        "weight": 28,
        "reason": "Thông tin xác thực có thể bị lợi dụng để chiếm quyền truy cập."
    },
    {
        "name": "Thúc ép chuyển tiền",
        "keywords": [
            "chuyển khoản ngay", "chuyển tiền ngay",
            "nạp tiền trước", "đóng phí", "phí nhận quà",
            "phí xác minh", "đặt cọc trước", "phí giải ngân"
        ],
        "weight": 25,
        "reason": "Yêu cầu chuyển tiền gấp hoặc trả phí trước cần được xác minh."
    },
    {
        "name": "Trúng thưởng hoặc quà tặng",
        "keywords": [
            "trúng thưởng", "bạn đã trúng", "nhận quà miễn phí",
            "nhận giải thưởng", "chúc mừng bạn đã trúng",
            "nhận thưởng", "phí nhận thưởng"
        ],
        "weight": 18,
        "reason": "Phần thưởng bất ngờ có thể được dùng để dụ chuyển tiền."
    },
    {
        "name": "Đầu tư lợi nhuận cao",
        "keywords": [
            "cam kết lợi nhuận", "lãi chắc chắn", "không rủi ro",
            "lợi nhuận 100%", "nhân đôi tài khoản", "lãi khủng",
            "lợi nhuận bảo đảm"
        ],
        "weight": 25,
        "reason": "Lời hứa lợi nhuận cao và chắc chắn cần được kiểm chứng."
    },
    {
        "name": "Giả danh ngân hàng hoặc cơ quan",
        "keywords": [
            "tài khoản bị khóa", "xác minh tài khoản",
            "công an yêu cầu", "cơ quan chức năng",
            "vi phạm pháp luật", "ngân hàng thông báo",
            "cơ quan thuế"
        ],
        "weight": 18,
        "reason": "Kẻ gian có thể giả danh tổ chức đáng tin để gây áp lực."
    },
    {
        "name": "Tuyển dụng đáng ngờ",
        "keywords": [
            "việc nhẹ lương cao", "nạp tiền làm nhiệm vụ",
            "tuyển cộng tác viên", "nhận hoa hồng",
            "chốt đơn nhận tiền", "làm nhiệm vụ nhận tiền"
        ],
        "weight": 20,
        "reason": "Công việc yêu cầu nạp tiền hoặc trả phí trước cần được kiểm tra."
    },
    {
        "name": "Giả danh người quen",
        "keywords": [
            "mượn tiền gấp", "đang cấp cứu", "đừng gọi lại",
            "giữ bí mật", "chuyển tiền giúp", "đang rất cần tiền"
        ],
        "weight": 22,
        "reason": "Tài khoản người quen có thể bị chiếm quyền."
    },
    {
        "name": "Mua bán trực tuyến đáng ngờ",
        "keywords": [
            "thanh toán ngoài nền tảng", "chuyển khoản để giữ hàng",
            "giá rẻ bất thường", "phí giao hàng hoàn tiền",
            "hoàn tiền đơn hàng"
        ],
        "weight": 16,
        "reason": "Cần kiểm tra người bán và phương thức thanh toán."
    },
    {
        "name": "Vay tiền và phí trước",
        "keywords": [
            "phí giải ngân", "phí mở hồ sơ", "vay nhanh",
            "xóa nợ xấu", "vay không cần gặp mặt", "duyệt vay ngay"
        ],
        "weight": 20,
        "reason": "Cần xác minh đơn vị cho vay và các khoản phí."
    },
    {
        "name": "Thúc ép hoặc đe dọa",
        "keywords": [
            "ngay lập tức", "khẩn cấp", "sắp hết hạn",
            "trong 5 phút", "nếu không sẽ", "lần cuối",
            "không làm sẽ bị khóa"
        ],
        "weight": 12,
        "reason": "Ngôn ngữ gây áp lực có thể khiến người nhận quyết định vội."
    },
    {
        "name": "Ứng dụng hoặc quyền truy cập lạ",
        "keywords": [
            "tải file apk", "chia sẻ màn hình", "điều khiển từ xa",
            "cấp quyền truy cập", "cài ứng dụng lạ",
            "cài app theo hướng dẫn"
        ],
        "weight": 22,
        "reason": "Ứng dụng và quyền truy cập không rõ nguồn có thể làm lộ dữ liệu."
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


def analyze_content(text):
    raw = text.strip()
    low = raw.lower()
    findings = []
    score = 0

    for rule in RULES:
        hits = [
            word for word in rule["keywords"]
            if word in low
        ]
        if hits:
            findings.append({
                "name": rule["name"],
                "hits": hits[:5],
                "reason": rule["reason"],
            })
            score += rule["weight"]

    urls = []
    for found in URL_PATTERN.findall(raw):
        candidate = found.rstrip(".,;:!?)\"]}")
        normalized = (
            candidate if candidate.lower().startswith(
                ("http://", "https://")
            ) else "https://" + candidate
        )
        parsed = urlparse(normalized)
        host = (parsed.hostname or "").lower()
        flags = []

        if parsed.scheme == "http":
            flags.append("Sử dụng HTTP; cần thận trọng với dữ liệu.")
            score += 8

        if host:
            if host.startswith("xn--") or ".xn--" in host:
                flags.append("Tên miền có dạng mã hóa ký tự.")
                score += 15

            if any(host.endswith(tld) for tld in SUSPICIOUS_TLDS):
                flags.append("Đuôi tên miền cần được xác minh.")
                score += 8

            if re.search(r"\d{5,}", host):
                flags.append("Tên miền chứa chuỗi số dài.")
                score += 6

            if host.count("-") >= 2:
                flags.append("Tên miền có nhiều dấu gạch nối.")
                score += 5

            if not flags:
                flags.append(
                    "Chưa thấy dấu hiệu rõ ràng qua kiểm tra URL cơ bản."
                )

        urls.append({
            "url": candidate,
            "host": host or "Không xác định",
            "flags": flags,
        })

    score = min(100, score)

    if score >= 55:
        level = "Cảnh báo cao"
        css = "result-high"
        headline = "Có nhiều dấu hiệu cần cảnh giác"
        advice = (
            "Tạm dừng thao tác. Không chuyển tiền, nhập OTP hoặc mật khẩu, "
            "không tải tệp và không cấp quyền truy cập. Hãy xác minh qua "
            "kênh chính thức do em tự tìm."
        )
    elif score >= 25:
        level = "Cần kiểm tra thêm"
        css = "result-medium"
        headline = "Nội dung có dấu hiệu đáng ngờ"
        advice = (
            "Chưa nên làm theo ngay. Kiểm tra nguồn gửi, địa chỉ website "
            "và đối chiếu thông tin qua nguồn độc lập."
        )
    else:
        level = "Chưa thấy nhiều dấu hiệu"
        css = "result-low"
        headline = "Chưa phát hiện nhiều dấu hiệu theo bộ quy tắc"
        advice = (
            "Điều này không chứng minh nội dung an toàn. Hãy kiểm tra "
            "nguồn, đường link và bảo vệ thông tin nhạy cảm."
        )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "level": level,
        "css": css,
        "headline": headline,
        "advice": advice,
        "score": score,
        "findings": findings,
        "urls": urls,
        "preview": raw[:200],
    }


def save_history(result):
    st.session_state.history.insert(0, {
        "Thời gian": result["timestamp"],
        "Kết quả": result["level"],
        "Điểm quy tắc": result["score"],
        "Nội dung rút gọn": result["preview"],
    })


# =========================================================
# 12 TÌNH HUỐNG LUYỆN TẬP
# =========================================================

CASES = [
    {
        "category": "🏦 Giả danh ngân hàng",
        "title": "Tài khoản của em sắp bị khóa?",
        "text": (
            "Vào lúc 9 giờ tối, em nhận được tin nhắn thông báo tài khoản "
            "ngân hàng sẽ bị tạm khóa vì chưa cập nhật thông tin. Tin nhắn "
            "yêu cầu truy cập đường link để xác minh trong vòng 10 phút. "
            "Trang web có logo gần giống ngân hàng và yêu cầu tên đăng nhập, "
            "mật khẩu cùng mã OTP. Em không thực hiện giao dịch nào trước đó."
        ),
        "options": [
            "Nhập đủ thông tin để tránh bị khóa.",
            "Bấm link nhưng chỉ nhập tên đăng nhập.",
            "Không nhập dữ liệu; tự mở ứng dụng ngân hàng chính thức hoặc liên hệ ngân hàng qua kênh đã xác minh.",
            "Chuyển tiếp tin nhắn cho bạn bè để hỏi."
        ],
        "answer": 2,
        "why": (
            "Kẻ gian có thể giả danh ngân hàng để lấy thông tin đăng nhập "
            "và OTP. Logo không chứng minh website là thật. Hãy tự mở ứng "
            "dụng hoặc website chính thức thay vì dùng link trong tin nhắn."
        ),
        "lesson": "Không cung cấp mật khẩu hoặc OTP qua đường link bất ngờ."
    },
    {
        "category": "💼 Tuyển dụng trực tuyến",
        "title": "Việc nhẹ, lương cao tại nhà",
        "text": (
            "Một tài khoản đăng tuyển cộng tác viên đặt đơn hàng ảo và nhận "
            "hoa hồng. Họ gửi ảnh chụp những người được cho là đã nhận tiền. "
            "Sau đó, họ yêu cầu em chuyển trước 200.000 đồng để mở nhiệm vụ "
            "cấp cao và hứa hoàn lại tiền cùng hoa hồng sau vài phút."
        ),
        "options": [
            "Chuyển tiền vì số tiền ban đầu không lớn.",
            "Xác minh công ty và không chuyển tiền trước khi xác minh độc lập.",
            "Mượn tiền bạn để làm nhiệm vụ.",
            "Gửi ảnh giấy tờ cá nhân để đăng ký."
        ],
        "answer": 1,
        "why": (
            "Yêu cầu nạp tiền để nhận việc hoặc mở nhiệm vụ là dấu hiệu đáng "
            "cảnh giác. Ảnh chụp giao dịch có thể không xác thực. Hãy kiểm tra "
            "đơn vị tuyển dụng và không gửi giấy tờ cá nhân cho bên chưa rõ."
        ),
        "lesson": "Không trả tiền chỉ để được nhận việc hoặc hoa hồng."
    },
    {
        "category": "🎁 Trúng thưởng",
        "title": "Em đã trúng một chiếc điện thoại!",
        "text": (
            "Em nhận được tin nhắn báo trúng một chiếc điện thoại đời mới "
            "trong chương trình quay thưởng mà em không nhớ đã tham gia. "
            "Người gửi yêu cầu họ tên, địa chỉ và phí vận chuyển trước khi "
            "hết hạn nhận quà trong ngày."
        ),
        "options": [
            "Thanh toán ngay vì phần quà có giá trị.",
            "Gửi địa chỉ nhà trước rồi quyết định sau.",
            "Kiểm tra xem mình có tham gia chương trình và xác minh qua kênh chính thức.",
            "Nhờ người lạ thanh toán hộ."
        ],
        "answer": 2,
        "why": (
            "Phần thưởng bất ngờ kèm yêu cầu phí và dữ liệu cá nhân cần "
            "được xác minh. Thời hạn gấp có thể tạo áp lực khiến em quyết "
            "định vội vàng."
        ),
        "lesson": "Xác minh chương trình trước khi tin thông báo trúng thưởng."
    },
    {
        "category": "👥 Giả danh người quen",
        "title": "Bạn thân nhắn mượn tiền khẩn cấp",
        "text": (
            "Một tài khoản dùng tên và ảnh của bạn thân nhắn rằng họ đang "
            "gặp việc gấp và cần tiền ngay. Người đó bảo em đừng gọi vì "
            "không tiện nghe máy. Cách nhắn hơi khác bình thường, nhưng "
            "tài khoản có nhiều ảnh cũ nên em vẫn phân vân."
        ),
        "options": [
            "Chuyển tiền ngay vì có ảnh bạn thân.",
            "Yêu cầu họ gửi mã OTP để chứng minh.",
            "Liên hệ qua số điện thoại hoặc kênh khác đã biết để xác minh.",
            "Đăng công khai toàn bộ tin nhắn."
        ],
        "answer": 2,
        "why": (
            "Tài khoản có thể bị chiếm quyền hoặc giả mạo. Ảnh và bài đăng "
            "cũ không chứng minh người nhắn là chủ tài khoản. Hãy xác minh "
            "qua một kênh độc lập."
        ),
        "lesson": "Xác minh yêu cầu chuyển tiền qua một kênh khác."
    },
    {
        "category": "🛍️ Mua bán trực tuyến",
        "title": "Món hàng giá rẻ bất thường",
        "text": (
            "Một cửa hàng bán tai nghe rẻ hơn nhiều nơi khác. Người bán "
            "nói chỉ còn một sản phẩm và yêu cầu chuyển khoản trực tiếp "
            "vào tài khoản cá nhân để giữ hàng. Họ không muốn giao dịch "
            "qua nền tảng mua sắm và trả lời mơ hồ về chính sách hoàn tiền."
        ),
        "options": [
            "Chuyển tiền ngay để không bỏ lỡ món hời.",
            "Kiểm tra đánh giá độc lập, thông tin cửa hàng và phương thức thanh toán an toàn.",
            "Gửi thông tin thẻ ngân hàng qua tin nhắn.",
            "Mua thêm nhiều món vì giá rẻ."
        ],
        "answer": 1,
        "why": (
            "Giá bất thường, thúc ép mua ngay và né tránh nền tảng thanh "
            "toán là các dấu hiệu cần kiểm tra. Chúng không tự chứng minh "
            "lừa đảo nhưng cần được xem xét cùng nhau."
        ),
        "lesson": "Đừng để giá rẻ khiến em bỏ qua bước kiểm tra."
    },
    {
        "category": "📈 Đầu tư trực tuyến",
        "title": "Lợi nhuận cao, cam kết không rủi ro",
        "text": (
            "Một người mới quen trên mạng giới thiệu nền tảng đầu tư và "
            "khẳng định ai cũng kiếm lợi nhuận lớn mỗi ngày. Họ gửi ảnh "
            "số dư và lời chứng thực, sau đó nói cơ hội chỉ có hôm nay "
            "và yêu cầu em nạp tiền ngay để vào nhóm đặc biệt."
        ),
        "options": [
            "Nạp tiền vì có nhiều ảnh chụp lợi nhuận.",
            "Vay tiền để tận dụng cơ hội.",
            "Kiểm tra thông tin độc lập, hiểu rủi ro và không quyết định vì áp lực.",
            "Gửi mật khẩu tài khoản cho người hướng dẫn."
        ],
        "answer": 2,
        "why": (
            "Lợi nhuận chắc chắn, lời mời gấp và bằng chứng chỉ do người "
            "quảng bá cung cấp đều cần kiểm chứng. Ảnh chụp có thể không "
            "xác thực và mọi quyết định tài chính đều có rủi ro."
        ),
        "lesson": "Kiểm tra độc lập trước khi quyết định tài chính."
    },
    {
        "category": "📦 Giả mạo giao hàng",
        "title": "Bưu kiện cần trả thêm phí",
        "text": (
            "Em nhận được tin nhắn nói bưu kiện đang chờ giao vì địa chỉ "
            "chưa đầy đủ. Tin nhắn có link yêu cầu điền địa chỉ và trả "
            "một khoản phí nhỏ. Em không nhớ có đơn hàng nào đang chờ, "
            "nhưng người gửi nói bưu kiện sẽ bị hủy nếu em không làm ngay."
        ),
        "options": [
            "Bấm link và điền thông tin.",
            "Trả phí vì số tiền nhỏ.",
            "Tự kiểm tra mã vận đơn trên ứng dụng hoặc website chính thức của đơn vị giao hàng.",
            "Nhập thông tin thẻ để xem bưu kiện."
        ],
        "answer": 2,
        "why": (
            "Tin nhắn giao hàng giả có thể nhằm thu thập dữ liệu hoặc "
            "thông tin thanh toán. Nếu không biết có đơn hàng, em nên "
            "tự kiểm tra qua kênh chính thức."
        ),
        "lesson": "Không nhập thông tin thanh toán qua link chưa xác minh."
    },
    {
        "category": "📱 Ứng dụng lạ",
        "title": "Nhân viên hỗ trợ yêu cầu cài ứng dụng",
        "text": (
            "Một người tự xưng là nhân viên hỗ trợ gọi điện nói tài khoản "
            "của em gặp lỗi. Họ yêu cầu tải ứng dụng từ link bên ngoài "
            "cửa hàng ứng dụng và bật chia sẻ màn hình. Họ đe dọa rằng "
            "nếu không làm ngay, tài khoản sẽ bị khóa."
        ),
        "options": [
            "Cài ứng dụng vì người đó biết tên em.",
            "Bật chia sẻ màn hình để họ xử lý.",
            "Từ chối cài ứng dụng hoặc cấp quyền; tự liên hệ hỗ trợ chính thức.",
            "Đọc mọi mã xác thực cho họ."
        ],
        "answer": 2,
        "why": (
            "Ứng dụng không rõ nguồn và yêu cầu chia sẻ màn hình có thể "
            "làm lộ dữ liệu. Việc người gọi biết tên em không chứng minh "
            "họ là nhân viên thật."
        ),
        "lesson": "Không cài ứng dụng hoặc cấp quyền cho người chưa xác minh."
    },
    {
        "category": "🎓 Học bổng giả mạo",
        "title": "Học bổng cần phí xét duyệt",
        "text": (
            "Một trang mạng xã hội đăng học bổng cho học sinh và dùng "
            "tên gần giống một tổ chức giáo dục nổi tiếng. Trang báo "
            "hồ sơ của em đã được chọn sơ bộ, nhưng yêu cầu đóng phí "
            "xét duyệt và gửi ảnh giấy tờ trong ngày hôm nay. Em chưa "
            "tìm thấy thông báo này trên website chính thức."
        ),
        "options": [
            "Thanh toán ngay để không mất cơ hội.",
            "Gửi giấy tờ trước rồi xác minh sau.",
            "Tìm thông báo chính thức, liên hệ tổ chức độc lập và hỏi người lớn đáng tin.",
            "Chia sẻ bài đăng để bạn bè đăng ký."
        ],
        "answer": 2,
        "why": (
            "Tên và hình ảnh gần giống tổ chức thật có thể bị lợi dụng. "
            "Yêu cầu phí và giấy tờ cần được xác minh trước khi thực hiện."
        ),
        "lesson": "Xác minh học bổng qua kênh chính thức của đơn vị tổ chức."
    },
    {
        "category": "📰 Tin giả",
        "title": "Bài đăng gây sốc được chia sẻ hàng nghìn lần",
        "text": (
            "Em đọc bài đăng nói trường sẽ đóng cửa vào ngày mai vì một "
            "sự việc nghiêm trọng. Bài viết không ghi nguồn rõ ràng, dùng "
            "tiêu đề gây sốc và kêu gọi mọi người chia sẻ thật nhanh. "
            "Nhiều tài khoản đã chia sẻ nhưng em chưa thấy thông báo từ trường."
        ),
        "options": [
            "Chia sẻ ngay vì có nhiều người đã chia sẻ.",
            "Kiểm tra thông báo của trường và nguồn đáng tin trước khi chia sẻ.",
            "Viết lại bài cho gây sốc hơn.",
            "Tin bài viết vì tiêu đề khẩn cấp."
        ],
        "answer": 1,
        "why": (
            "Lượt chia sẻ lớn không đồng nghĩa với thông tin chính xác. "
            "Hãy tìm thông báo trực tiếp từ trường hoặc cơ quan có trách nhiệm."
        ),
        "lesson": "Kiểm tra nguồn và ngày đăng trước khi chia sẻ."
    },
    {
        "category": "📞 Giả danh cơ quan chức năng",
        "title": "Cuộc gọi đe dọa liên quan đến giấy tờ",
        "text": (
            "Một người gọi điện tự xưng là cán bộ cơ quan chức năng và "
            "nói thông tin của em liên quan đến một vụ việc. Họ yêu cầu "
            "em giữ bí mật với gia đình, cung cấp thông tin tài khoản "
            "hoặc chuyển tiền để chứng minh mình không liên quan. Họ "
            "không cho em thời gian hỏi người lớn."
        ),
        "options": [
            "Làm theo vì sợ gặp rắc rối.",
            "Cung cấp thông tin tài khoản để chứng minh mình vô tội.",
            "Không cung cấp dữ liệu hay chuyển tiền; báo cho người lớn đáng tin và xác minh qua kênh chính thức.",
            "Giữ bí mật vì người gọi đã yêu cầu."
        ],
        "answer": 2,
        "why": (
            "Đe dọa, yêu cầu giữ bí mật và đòi dữ liệu hoặc tiền là dấu "
            "hiệu nghiêm trọng cần cảnh giác. Em nên trao đổi với phụ huynh "
            "hoặc người lớn đáng tin và kiểm tra thông tin qua kênh chính thức."
        ),
        "lesson": "Không để lời đe dọa khiến em chuyển tiền hoặc cung cấp dữ liệu."
    },
    {
        "category": "🔗 Đường link đáng ngờ",
        "title": "Website có địa chỉ gần giống trang thật",
        "text": (
            "Em nhận được một link quảng cáo chương trình giảm giá lớn. "
            "Tên website gần giống một thương hiệu quen thuộc nhưng có "
            "thêm dấu gạch nối và vài ký tự lạ. Trang yêu cầu đăng nhập "
            "bằng tài khoản cá nhân để nhận mã giảm giá, đồng thời thông "
            "báo mã chỉ có hiệu lực trong vài phút."
        ),
        "options": [
            "Đăng nhập vì tên website trông quen.",
            "Dùng mật khẩu của tài khoản khác để thử.",
            "Không đăng nhập; tự tìm website chính thức và so sánh tên miền.",
            "Gửi link cho bạn để họ đăng nhập thử trước."
        ],
        "answer": 2,
        "why": (
            "Tên miền giả mạo có thể được tạo để đánh lừa người dùng. "
            "Biểu tượng ổ khóa hoặc giao diện giống thật không đảm bảo "
            "đơn vị vận hành đáng tin. Hãy tự tìm trang chính thức."
        ),
        "lesson": "Đọc kỹ tên miền và không đăng nhập qua link bất ngờ."
    },
]


# =========================================================
# MENU
# =========================================================

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


# =========================================================
# HEADER
# =========================================================

st.markdown(f"""
<div class="hero">
    <div class="hero-label">DIGITAL SAFETY · SOCIAL SANDBOX AI</div>
    <h1>Kiểm tra trước khi bạn bấm.</h1>
    <p>{html.escape(PROJECT_TITLE)}</p>
    <p>
        Nhận diện dấu hiệu đáng ngờ, luyện tư duy phản biện
        và xác minh thông tin trước khi chia sẻ.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TRANG 1: KIỂM TRA THÔNG TIN
# =========================================================

if page == "🔎 Kiểm tra thông tin":

    st.subheader("🔎 Kiểm tra nội dung đáng ngờ")

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
        "Trúng thưởng": (
            "Chúc mừng bạn đã trúng thưởng điện thoại! "
            "Bấm link nhận quà và đóng phí nhận thưởng hôm nay."
        ),
        "Mượn tiền khẩn cấp": (
            "Mình đang cấp cứu, mượn tiền gấp giúp mình. "
            "Đừng gọi lại, chuyển khoản ngay nhé."
        ),
        "Mua bán online": (
            "Giá rẻ bất thường, chuyển khoản để giữ hàng. "
            "Thanh toán ngoài nền tảng để được giảm giá."
        ),
        "Đầu tư lợi nhuận cao": (
            "Cam kết lợi nhuận 100%, không rủi ro. "
            "Nạp tiền ngay để nhân đôi tài khoản."
        ),
        "Vay tiền": (
            "Duyệt vay ngay, phí giải ngân và phí mở hồ sơ "
            "cần được thanh toán trước."
        ),
    }

    choice = st.selectbox("Thử nội dung mẫu", list(examples.keys()))

    if choice != "Tự nhập nội dung":
        st.session_state.draft = examples[choice]

    content = st.text_area(
        "Nội dung cần kiểm tra",
        key="draft",
        height=180,
        placeholder="Dán tin nhắn, bài đăng hoặc đường link vào đây..."
    )

    c1, c2 = st.columns(2)

    with c1:
        analyze = st.button(
            "✨ Phân tích ngay",
            type="primary",
            use_container_width=True
        )

    with c2:
        clear = st.button("🗑️ Xóa nội dung", use_container_width=True)

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
            unsafe_allow_html=True
        )

        a, b, c = st.columns(3)
        a.metric("Mức cảnh báo", result["level"])
        b.metric("Điểm quy tắc", f"{result['score']}/100")
        c.metric("Nhóm dấu hiệu", len(result["findings"]))

        st.caption(
            "Điểm quy tắc nội bộ, không phải xác suất nội dung là lừa đảo."
        )

        st.markdown("### ⚠️ Dấu hiệu phát hiện")

        if result["findings"]:
            for finding in result["findings"]:
                with st.expander(f"🔎 {finding['name']}"):
                    st.write(finding["reason"])
                    st.write("Cụm từ khớp: " + ", ".join(finding["hits"]))
        else:
            st.info(
                "Chưa tìm thấy cụm từ phổ biến đáng chú ý. "
                "Lừa đảo vẫn có thể dùng cách diễn đạt khác."
            )

        if result["urls"]:
            st.markdown("### 🌐 Kiểm tra đường link")

            for item in result["urls"]:
                st.write("**" + item["url"] + "**")
                st.caption("Tên miền: " + item["host"])
                for flag in item["flags"]:
                    st.write("• " + flag)

            st.warning(
                "Không mở link đáng ngờ để thử. Hãy tự tìm website "
                "hoặc ứng dụng chính thức để xác minh."
            )

        st.markdown("### ✅ Các bước xử lý an toàn")

        st.markdown("""
        1. **Dừng lại:** Không chuyển tiền, nhập OTP hoặc mật khẩu.
        2. **Xác minh:** Tự tìm kênh liên hệ chính thức.
        3. **Đối chiếu:** Kiểm tra thông tin từ nguồn độc lập.
        4. **Hỏi người đáng tin:** Nhờ phụ huynh hoặc giáo viên nếu còn phân vân.
        """)

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
                việc xác minh từ nguồn chính thức.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Giới hạn của bộ phân tích"):
        st.write(
            "Phiên bản hiện tại sử dụng quy tắc từ khóa và một số kiểm tra "
            "URL cơ bản. Chưa tích hợp mô hình AI lớn hoặc cơ sở dữ liệu "
            "xác minh thời gian thực. Có thể xảy ra cảnh báo nhầm hoặc bỏ sót."
        )


# =========================================================
# TRANG 2: THỬ TÌNH HUỐNG
# =========================================================

elif page == "🧩 Thử tình huống":

    st.subheader("🧩 Phòng thực hành an toàn số")

    st.write(
        "Đọc kỹ tình huống mô phỏng, lựa chọn cách xử lý an toàn nhất "
        "và xem lời giải thích. Mỗi lần đổi, hệ thống sẽ chọn một tình "
        "huống khác; các tình huống chưa luyện sẽ được ưu tiên."
    )

    total_cases = len(CASES)

    if st.session_state.scenario_current is None:
        st.session_state.scenario_current = random.randrange(total_cases)
        st.session_state.scenario_seen = [st.session_state.scenario_current]

    current = st.session_state.scenario_current
    case = CASES[current]

    answered = len(st.session_state.scenario_answered)
    correct_count = sum(st.session_state.scenario_answered.values())

    a, b, c = st.columns(3)
    a.metric("Tình huống", f"{current + 1}/{total_cases}")
    b.metric("Đã trả lời", answered)
    c.metric("Trả lời đúng", correct_count)

    st.progress(answered / total_cases)

    st.markdown(
        f"""
        <div class="panel">
            <div class="pill">{html.escape(case['category'])}</div>
            <h3>{html.escape(case['title'])}</h3>
            <p style="line-height:1.95">
                {html.escape(case['text'])}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.radio(
        "Theo em, đâu là cách xử lý an toàn nhất?",
        case["options"],
        key=f"scenario_choice_{current}"
    )

    if st.button(
        "Kiểm tra câu trả lời",
        type="primary",
        use_container_width=True,
        key=f"scenario_check_{current}"
    ):
        selected_index = case["options"].index(answer)
        is_correct = selected_index == case["answer"]

        st.session_state.scenario_answered[current] = is_correct
        st.session_state.scenario_feedback[current] = {
            "choice": selected_index,
            "correct": is_correct,
        }

    feedback = st.session_state.scenario_feedback.get(current)

    if feedback:
        if feedback["correct"]:
            st.success("🎉 Chính xác! Em đã chọn cách xử lý an toàn.")
        else:
            st.error(
                "Chưa chính xác. Không sao, đây là cơ hội để em học "
                "cách nhận diện dấu hiệu đáng ngờ."
            )

        st.markdown("### 💡 Giải thích chi tiết")
        st.write(case["why"])
        st.info("**Bài học cần nhớ:** " + case["lesson"])

        st.markdown("### 🔎 Câu hỏi suy ngẫm")

        reflection = [
            "Dấu hiệu nào trong tình huống khiến em cần dừng lại?",
            "Em có thể kiểm tra thông tin bằng nguồn độc lập nào?",
            "Nếu người gửi tiếp tục gây áp lực, em sẽ xử lý ra sao?"
        ]

        for question in reflection:
            st.write("• " + question)

    st.divider()

    left, right = st.columns(2)

    with left:
        if st.button(
            "🎲 Đổi tình huống khác",
            use_container_width=True
        ):
            available = [
                i for i in range(total_cases)
                if i != current
            ]

            unseen = [
                i for i in available
                if i not in st.session_state.scenario_seen
            ]

            if not unseen:
                unseen = available
                st.session_state.scenario_seen = [current]

            next_index = random.choice(unseen)
            st.session_state.scenario_current = next_index
            st.session_state.scenario_seen.append(next_index)
            st.rerun()

    with right:
        if st.button(
            "🔄 Bắt đầu lại",
            use_container_width=True
        ):
            st.session_state.scenario_answered = {}
            st.session_state.scenario_feedback = {}
            next_index = random.randrange(total_cases)
            st.session_state.scenario_current = next_index
            st.session_state.scenario_seen = [next_index]
            st.rerun()

    if answered:
        st.markdown("### 📊 Kết quả luyện tập")

        a, b, c = st.columns(3)
        a.metric("Đã trả lời", answered)
        b.metric("Đúng", correct_count)
        c.metric("Tỉ lệ đúng", f"{round(correct_count / answered * 100)}%")

        st.caption(
            "Kết quả chỉ lưu trong phiên hiện tại. Các tình huống là "
            "mô phỏng để luyện kỹ năng, không đại diện cho mọi trường hợp thực tế."
        )


# =========================================================
# TRANG 3: KHẢO SÁT NHANH
# =========================================================

elif page == "📝 Khảo sát nhanh":

    st.subheader("📝 Khảo sát kỹ năng xác thực thông tin")

    st.write(
        "Bài khảo sát ngắn phục vụ trải nghiệm nghiên cứu. "
        "Không cần nhập tên hoặc thông tin cá nhân."
    )

    mode = st.radio(
        "Thời điểm khảo sát",
        ["Trước trải nghiệm", "Sau trải nghiệm"],
        horizontal=True
    )

    questions = [
        {
            "q": "Tin nhắn yêu cầu OTP qua link lạ. Em nên:",
            "opts": [
                "Nhập ngay",
                "Không cung cấp OTP và xác minh qua kênh chính thức",
                "Gửi OTP cho bạn"
            ],
            "ans": 1
        },
        {
            "q": "Một công việc online yêu cầu nạp tiền trước. Em nên:",
            "opts": [
                "Nạp thử một khoản nhỏ",
                "Xác minh đơn vị và không chuyển tiền khi chưa rõ",
                "Làm theo ngay"
            ],
            "ans": 1
        },
        {
            "q": "Người quen mượn tiền gấp và bảo đừng gọi. Em nên:",
            "opts": [
                "Chuyển tiền ngay",
                "Đăng công khai tin nhắn",
                "Xác minh qua kênh khác"
            ],
            "ans": 2
        },
        {
            "q": "Website có tên gần giống thương hiệu quen thuộc. Em nên:",
            "opts": [
                "Tin ngay",
                "Kiểm tra tên miền và tìm kênh chính thức",
                "Nhập thử mật khẩu"
            ],
            "ans": 1
        },
        {
            "q": "Cảnh báo thấp có nghĩa là:",
            "opts": [
                "Chắc chắn an toàn",
                "Không cần kiểm tra thêm",
                "Chưa thấy nhiều dấu hiệu theo quy tắc, vẫn cần xác minh"
            ],
            "ans": 2
        }
    ]

    with st.form("survey_form"):
        answers = []

        for i, q in enumerate(questions):
            st.markdown(f"**Câu {i + 1}. {q['q']}**")
            answers.append(
                st.radio(
                    "Chọn đáp án",
                    q["opts"],
                    key=f"survey_{mode}_{i}",
                    label_visibility="collapsed"
                )
            )

        submitted = st.form_submit_button(
            "Chấm điểm khảo sát",
            type="primary",
            use_container_width=True
        )

    if submitted:
        correct = sum(
            1 for i, q in enumerate(questions)
            if answers[i] == q["opts"][q["ans"]]
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
            "Điểm": score
        })

        st.success(
            f"Em trả lời đúng {correct}/{len(questions)} câu — {score}/100."
        )

    a, b = st.columns(2)

    a.metric(
        "Điểm trước trải nghiệm",
        "—" if st.session_state.quiz_before is None
        else f"{st.session_state.quiz_before}/100"
    )

    b.metric(
        "Điểm sau trải nghiệm",
        "—" if st.session_state.quiz_after is None
        else f"{st.session_state.quiz_after}/100"
    )

    if (
        st.session_state.quiz_before is not None
        and st.session_state.quiz_after is not None
    ):
        diff = st.session_state.quiz_after - st.session_state.quiz_before
        st.info(
            f"Chênh lệch điểm: {diff:+d} điểm phần trăm. "
            "Kết quả này không tự nó chứng minh quan hệ nhân quả."
        )

    st.caption("Dữ liệu chỉ lưu trong phiên ứng dụng hiện tại.")


# =========================================================
# TRANG 4: LỊCH SỬ VÀ THỐNG KÊ
# =========================================================

elif page == "📊 Lịch sử & thống kê":

    st.subheader("📊 Lịch sử và thống kê")

    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)

        st.metric("Số lượt kiểm tra", len(df))
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Tải lịch sử kiểm tra CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="social_sandbox_history.csv",
            mime="text/csv"
        )
    else:
        st.info("Chưa có lịch sử. Hãy kiểm tra một nội dung trước.")

    st.divider()
    st.markdown("### 📝 Kết quả khảo sát")

    if st.session_state.survey_history:
        survey_df = pd.DataFrame(st.session_state.survey_history)

        st.dataframe(
            survey_df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ Tải kết quả khảo sát CSV",
            data=survey_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="social_sandbox_survey.csv",
            mime="text/csv"
        )
    else:
        st.info("Chưa có kết quả khảo sát.")

    st.caption(
        "Lịch sử và khảo sát hiện được lưu trong phiên, "
        "chưa phải cơ sở dữ liệu lâu dài."
    )


# =========================================================
# TRANG 5: GIỚI THIỆU ĐỀ TÀI
# =========================================================

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
        unsafe_allow_html=True
    )

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="panel">
            <h3>🔎 Kiểm tra thông tin</h3>
            <p>Phân tích dấu hiệu ngôn ngữ và URL đáng ngờ.</p>
        </div>
        <div class="panel">
            <h3>🧩 Thực hành</h3>
            <p>Luyện tập qua các tình huống mô phỏng gần gũi.</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="panel">
            <h3>📝 Khảo sát</h3>
            <p>Quan sát kết quả trước và sau trải nghiệm.</p>
        </div>
        <div class="panel">
            <h3>📊 Thống kê</h3>
            <p>Xem lịch sử trong phiên và xuất dữ liệu CSV.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### ⚠️ Giới hạn hệ thống")

    st.warning(
        "Phiên bản hiện tại dùng quy tắc từ khóa và kiểm tra URL cơ bản. "
        "Chưa tích hợp mô hình AI lớn hoặc cơ sở dữ liệu xác minh thời gian "
        "thực. Kết quả có thể cảnh báo nhầm hoặc bỏ sót."
    )

    st.markdown("### 🔐 Nguyên tắc an toàn")

    st.markdown("""
    - Không nhập mật khẩu, OTP, số thẻ hoặc dữ liệu cá nhân thật.
    - Không xem điểm cảnh báo là xác suất lừa đảo.
    - Luôn xác minh qua kênh chính thức.
    - Khi nghiên cứu với học sinh, cần có sự cho phép phù hợp
      và bảo vệ dữ liệu người tham gia.
    """)


# =========================================================
# CHÂN TRANG
# =========================================================

st.divider()

st.markdown(
    f"""
    <p style="text-align:center; color:#9aa9c5; font-size:12px;">
        SOCIAL SANDBOX AI · XÁC THỰC THÔNG TIN SỐ<br>
        {html.escape(PROJECT_TITLE)}<br>
        Dừng lại · Kiểm tra · Suy nghĩ trước khi chia sẻ
    </p>
    """,
    unsafe_allow_html=True
)
