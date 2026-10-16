
import random
import re
from datetime import datetime

import streamlit as st

st.set_page_config(
    page_title="Xác thực thông tin số | Social Sandbox AI",
    page_icon="🛡️",
    layout="wide",
)

# ---------- GIAO DIỆN ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 0% 0%, #20245b 0%, transparent 42%),
        linear-gradient(140deg, #080d1c, #10152c 60%, #11102b);
    color: #f3f5ff;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
[data-testid="stSidebar"] {
    background: #0b1021;
    border-right: 1px solid #292f51;
}
h1, h2, h3 { color: #f5f6ff; }
p, li, label { line-height: 1.7; }
div.stButton > button {
    border-radius: 12px;
    min-height: 44px;
    border: 1px solid #6565dd;
    background: linear-gradient(100deg, #5555ce, #7763e8);
    color: white;
    font-weight: 700;
}
div.stButton > button:hover {
    border-color: #72e5ff;
    color: white;
}
[data-testid="stTextArea"] textarea {
    background: #10172b;
    color: #f3f5ff;
    border: 1px solid #444c75;
    border-radius: 12px;
}
.panel {
    background: rgba(25, 32, 62, .85);
    border: 1px solid #343c65;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 15px;
}
.muted { color: #b8c1df; }
.small { font-size: 0.9rem; color: #b8c1df; }
</style>
""", unsafe_allow_html=True)


# ---------- TRẠNG THÁI ----------
for key, default in {
    "history": [],
    "content_input": "",
    "current_scenario": None,
    "seen_scenarios": [],
    "scenario_result": None,
    "survey_results": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ---------- CÁC TÌNH HUỐNG THỰC HÀNH ----------
SCENARIOS = [
    {
        "title": "Tin nhắn giả mạo ngân hàng",
        "text": "Tài khoản của bạn sẽ bị khóa sau 10 phút. Bấm đường link dưới đây và nhập mật khẩu, mã OTP để xác minh ngay.",
        "choices": [
            "Bấm link và nhập thông tin",
            "Gửi mã OTP cho người nhắn",
            "Không bấm link, kiểm tra qua ứng dụng hoặc kênh chính thức của ngân hàng",
            "Chuyển tiếp cho tất cả bạn bè",
        ],
        "correct": 2,
        "explain": "Tin nhắn tạo áp lực thời gian và yêu cầu thông tin xác thực. Hãy tự mở ứng dụng hoặc liên hệ ngân hàng qua kênh chính thức."
    },
    {
        "title": "Việc nhẹ lương cao",
        "text": "Một tài khoản tuyển cộng tác viên online, hứa trả 2 triệu đồng mỗi ngày. Muốn nhận việc, bạn phải nộp phí kích hoạt trước.",
        "choices": [
            "Nộp tiền ngay",
            "Kiểm tra đơn vị tuyển dụng, hợp đồng và yêu cầu phí",
            "Mượn tiền để tham gia",
            "Gửi ảnh giấy tờ tùy thân",
        ],
        "correct": 1,
        "explain": "Lời hứa thu nhập cao bất thường và yêu cầu nộp tiền trước là dấu hiệu cần kiểm tra kỹ."
    },
    {
        "title": "Thông báo trúng thưởng",
        "text": "Bạn được chọn nhận điện thoại miễn phí. Hãy đóng phí vận chuyển ngay và gửi mã xác minh để nhận quà.",
        "choices": [
            "Đóng phí ngay",
            "Gửi mã xác minh",
            "Kiểm tra chương trình trên trang chính thức, không cung cấp mã bảo mật",
            "Gửi cho bạn bè cùng tham gia",
        ],
        "correct": 2,
        "explain": "Cần xác minh chương trình và đơn vị tổ chức. Không chia sẻ mã xác minh chỉ vì lời hứa trúng thưởng."
    },
    {
        "title": "Bạn bè nhờ chuyển tiền",
        "text": "Một tài khoản giống tài khoản bạn thân nhắn rằng đang gặp việc gấp, cần chuyển tiền ngay và không được gọi điện.",
        "choices": [
            "Chuyển tiền vì là bạn thân",
            "Gọi qua số hoặc tài khoản đã biết để xác nhận",
            "Gửi thêm thông tin ngân hàng",
            "Làm theo vì người nhắn đang vội",
        ],
        "correct": 1,
        "explain": "Tài khoản có thể bị chiếm quyền hoặc bị giả mạo. Hãy xác nhận bằng một kênh liên lạc độc lập."
    },
    {
        "title": "Mua hàng giá rẻ bất thường",
        "text": "Một cửa hàng mới lập bán điện thoại giá thấp hơn nhiều nơi khác, yêu cầu chuyển khoản trước và không có thông tin đổi trả.",
        "choices": [
            "Chuyển khoản ngay",
            "Kiểm tra lịch sử cửa hàng, đánh giá độc lập và chính sách mua hàng",
            "Gửi ảnh thẻ ngân hàng",
            "Tin vì bài đăng có nhiều lượt thích",
        ],
        "correct": 1,
        "explain": "Giá quá thấp, thiếu thông tin và chỉ nhận chuyển khoản là các yếu tố cần kiểm chứng."
    },
    {
        "title": "Đầu tư lợi nhuận cao",
        "text": "Một nhóm chat cam kết đầu tư 1 triệu đồng sẽ nhận lại 3 triệu đồng sau vài ngày, đồng thời yêu cầu mời thêm thành viên.",
        "choices": [
            "Đầu tư toàn bộ tiền tiết kiệm",
            "Mượn tiền để đầu tư",
            "Tìm hiểu độc lập về đơn vị và rủi ro; không tin cam kết lợi nhuận chắc chắn",
            "Mời bạn bè tham gia ngay",
        ],
        "correct": 2,
        "explain": "Lợi nhuận cao được bảo đảm trong thời gian ngắn là lời hứa đáng nghi. Không nên quyết định chỉ dựa vào nhóm chat."
    },
    {
        "title": "Tin nhắn giao hàng",
        "text": "Bạn nhận tin nhắn yêu cầu trả thêm phí nhỏ để nhận bưu kiện, kèm một đường link lạ không thuộc trang giao hàng quen thuộc.",
        "choices": [
            "Bấm link và nhập thông tin thẻ",
            "Kiểm tra mã vận đơn trên ứng dụng hoặc trang chính thức của đơn vị giao hàng",
            "Gửi mã OTP cho người nhắn",
            "Chuyển tiếp tin nhắn cho mọi người",
        ],
        "correct": 1,
        "explain": "Không dùng đường link lạ để thanh toán. Hãy kiểm tra đơn hàng qua kênh chính thức."
    },
    {
        "title": "Ứng dụng yêu cầu quyền bất thường",
        "text": "Một ứng dụng không rõ nhà phát triển yêu cầu quyền đọc tin nhắn, danh bạ và hỗ trợ truy cập để nhận phần thưởng.",
        "choices": [
            "Cấp mọi quyền được yêu cầu",
            "Kiểm tra nhà phát triển và quyền truy cập; không cài nếu không đáng tin",
            "Gửi mật khẩu cho nhà phát triển",
            "Tắt mọi cảnh báo bảo mật",
        ],
        "correct": 1,
        "explain": "Chỉ cấp quyền cần thiết cho ứng dụng đáng tin cậy. Phần thưởng không phải lý do để bỏ qua quyền riêng tư."
    },
    {
        "title": "Tin tức gây sốc",
        "text": "Một bài đăng khẳng định trường học sẽ đóng cửa ngày mai, nhưng không nêu nguồn và kêu gọi chia sẻ gấp cho mọi người.",
        "choices": [
            "Chia sẻ ngay để cảnh báo",
            "Tin vì nhiều người đã bình luận",
            "Kiểm tra thông báo từ trường và đối chiếu nguồn độc lập",
            "Thêm nội dung giật gân để nhiều người chú ý",
        ],
        "correct": 2,
        "explain": "Cảm xúc mạnh và nhiều lượt tương tác không chứng minh tin là đúng. Hãy tìm thông báo từ nguồn có trách nhiệm."
    },
    {
        "title": "Giả danh cơ quan chức năng",
        "text": "Người gọi tự nhận là cán bộ, yêu cầu giữ bí mật, cung cấp thông tin cá nhân và chuyển tiền để giải quyết một vụ việc.",
        "choices": [
            "Làm theo ngay",
            "Cung cấp tất cả thông tin",
            "Kết thúc cuộc gọi và tự xác minh qua kênh chính thức",
            "Gửi ảnh giấy tờ qua tin nhắn",
        ],
        "correct": 2,
        "explain": "Không làm theo yêu cầu chuyển tiền hay cung cấp dữ liệu nhạy cảm chỉ dựa trên cuộc gọi chưa xác minh."
    },
    {
        "title": "Học bổng không rõ nguồn",
        "text": "Một trang lạ hứa cấp học bổng lớn, yêu cầu nộp phí hồ sơ và tải ảnh giấy tờ cá nhân lên một đường link.",
        "choices": [
            "Nộp phí để giữ suất",
            "Tìm thông báo từ trường hoặc đơn vị cấp học bổng chính thức",
            "Gửi thêm dữ liệu cá nhân",
            "Chia sẻ cho cả lớp trước khi kiểm tra",
        ],
        "correct": 1,
        "explain": "Xác minh đơn vị cấp học bổng, điều kiện và quy trình qua trang chính thức trước khi gửi dữ liệu."
    },
    {
        "title": "Đường link đăng nhập lạ",
        "text": "Một người gửi link có tên gần giống mạng xã hội quen thuộc và yêu cầu đăng nhập để xem một video đang gây chú ý.",
        "choices": [
            "Đăng nhập để xem",
            "Nhập mật khẩu rồi kiểm tra sau",
            "Không mở link đáng nghi; tự truy cập ứng dụng hoặc trang chính thức",
            "Gửi link cho bạn bè thử trước",
        ],
        "correct": 2,
        "explain": "Tên miền giả có thể giống tên thật. Tự mở ứng dụng chính thức thay vì đăng nhập qua link được gửi."
    },
]


# ---------- PHÂN TÍCH QUY TẮC DỰ PHÒNG ----------
RULES = {
    "Mã OTP và mật khẩu": [
        "otp", "mật khẩu", "mat khau", "mã xác minh",
        "ma xac minh", "password", "đăng nhập"
    ],
    "Chuyển tiền và phí trước": [
        "chuyển tiền", "chuyen tien", "nộp phí", "nop phi",
        "phí kích hoạt", "phi kich hoat", "đóng phí", "dong phi"
    ],
    "Khẩn cấp và đe dọa": [
        "ngay lập tức", "ngay lap tuc", "khẩn cấp", "khan cap",
        "bị khóa", "bi khoa", "10 phút", "10 phut", "giữ bí mật"
    ],
    "Trúng thưởng và lợi nhuận": [
        "trúng thưởng", "trung thuong", "lợi nhuận", "loi nhuan",
        "lương cao", "luong cao", "cam kết lợi nhuận"
    ],
    "Thông tin cá nhân": [
        "căn cước", "can cuoc", "số tài khoản", "so tai khoan",
        "danh bạ", "danh ba", "giấy tờ", "giay to"
    ],
    "Đường link cần kiểm tra": [
        "http://", "bit.ly", "tinyurl", "click vào", "click vao"
    ],
}


def rule_analysis(text):
    lower = text.lower()
    matched = []

    for category, words in RULES.items():
        found = [word for word in words if word in lower]
        if found:
            matched.append((category, found[:4]))

    urls = re.findall(r"https?://\S+", text, flags=re.IGNORECASE)
    url_notes = []

    for url in urls:
        if url.lower().startswith("http://"):
            url_notes.append("Đường link dùng HTTP, không phải HTTPS.")
        if "xn--" in url.lower():
            url_notes.append("Tên miền có ký tự mã hóa, cần kiểm tra cẩn thận.")
        if len(url) > 100:
            url_notes.append("Đường link dài bất thường.")

    score = min(95, len(matched) * 16 + len(url_notes) * 12)

    if score >= 55:
        level = "Nhiều dấu hiệu đáng nghi"
    elif score >= 25:
        level = "Cần kiểm chứng thêm"
    else:
        level = "Chưa phát hiện nhiều dấu hiệu theo quy tắc"

    return {
        "score": score,
        "level": level,
        "matched": matched,
        "url_notes": url_notes,
    }


# ---------- KẾT NỐI GEMINI ----------
def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""


def ask_gemini(text):
    api_key = get_api_key()
    if not api_key:
        return None, (
            "Chưa cấu hình Gemini API key. "
            "Quản trị viên cần thêm GEMINI_API_KEY trong Secrets của Streamlit Cloud."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        prompt = f"""
Bạn là trợ lý giáo dục về an toàn thông tin số cho học sinh trung học.
Hãy phân tích nội dung dưới đây bằng tiếng Việt, dễ hiểu và không phán xét.

Nội dung cần phân tích:
---
{text[:7000]}
---

Trả lời theo cấu trúc:
1. Tóm tắt nội dung.
2. Mức độ rủi ro sơ bộ: thấp, trung bình hoặc cao.
3. Các dấu hiệu đáng chú ý và giải thích cụ thể.
4. Những điều chưa đủ bằng chứng để kết luận.
5. Ba bước kiểm chứng an toàn, thực tế.
6. Một câu hỏi giúp học sinh suy nghĩ phản biện.

Không khẳng định chắc chắn nội dung là lừa đảo nếu chưa đủ bằng chứng.
Không tuyên bố đã kiểm tra website hoặc nguồn trực tiếp nếu bạn chưa thực sự truy cập.
Không yêu cầu người dùng cung cấp mật khẩu, mã OTP hay thông tin riêng tư.
"""

        response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)
        if not response.text:
            return None, "AI không trả về nội dung. Em thử lại sau nhé."

        return response.text, None

        except Exception as error:
        error_type = type(error).__name__
        message = str(error).lower()

        if "quota" in message or "429" in message or "rate" in message:
            return None, (
                "Gemini đã hết hạn mức hoặc bị giới hạn lượt dùng. "
                "Em hãy thử lại sau."
            )

        if "api key" in message or "permission" in message or "403" in message:
            return None, (
                "Gemini không xác thực được API key. "
                "Hãy kiểm tra mục Secrets trên Streamlit Cloud."
            )

        return None, (
            f"Lỗi Gemini ({error_type}). "
            "Hãy kiểm tra nhật ký ứng dụng trên Streamlit Cloud."
        )
# ---------- THANH ĐIỀU HƯỚNG ----------
st.sidebar.markdown("# 🛡️ Social Sandbox AI")
st.sidebar.caption("Không gian thực hành xác thực thông tin số")

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
st.sidebar.caption("Dự án nghiên cứu KHKT dành cho học sinh trung học")


# ---------- TRANG 1: PHÂN TÍCH ----------
if page == "🔎 Kiểm tra thông tin":
    st.title("🔎 Kiểm tra thông tin số")
    st.write(
        "Dán tin nhắn, bài đăng hoặc nội dung đáng ngờ. "
        "Hệ thống sẽ kết hợp quy tắc nhận diện với AI để hỗ trợ em kiểm chứng."
    )

    samples = {
        "Tin nhắn giả mạo ngân hàng":
            "Tài khoản của bạn sẽ bị khóa sau 10 phút. "
            "Bấm http://example.invalid/verify và nhập mật khẩu, mã OTP ngay.",
        "Tuyển cộng tác viên":
            "Tuyển cộng tác viên online, lương cao mỗi ngày. "
            "Nộp phí kích hoạt trước để bắt đầu công việc.",
        "Tin tức chưa xác minh":
            "Một bài đăng nói trường học sẽ đóng cửa ngày mai, "
            "nhưng không đưa nguồn chính thức và yêu cầu chia sẻ gấp.",
        "Tự nhập nội dung": "",
    }

    sample_choice = st.selectbox("Thử nhanh bằng nội dung mẫu", list(samples.keys()))

    if st.button("📥 Dùng nội dung mẫu"):
        st.session_state.content_input = samples[sample_choice]

    content = st.text_area(
        "Nội dung cần kiểm tra",
        key="content_input",
        height=220,
        max_chars=7000,
        placeholder="Dán nội dung tại đây. Không nhập mật khẩu, OTP hoặc dữ liệu cá nhân thật.",
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        analyze_clicked = st.button(
            "✨ Phân tích bằng AI",
            type="primary",
            use_container_width=True,
        )

    with col2:
        rule_clicked = st.button(
            "⚡ Kiểm tra quy tắc",
            use_container_width=True,
        )

    if analyze_clicked or rule_clicked:
        if len(content.strip()) < 10:
            st.warning("Em hãy nhập nội dung dài hơn một chút để phân tích.")
        else:
            result = rule_analysis(content)

            st.subheader("Kết quả kiểm tra sơ bộ")
            st.metric("Điểm rủi ro theo quy tắc", f"{result['score']}/95")
            st.write(f"**Đánh giá:** {result['level']}")

            if result["matched"]:
                st.write("**Các nhóm dấu hiệu được nhận diện:**")
                for category, words in result["matched"]:
                    st.write(f"- **{category}:** {', '.join(words)}")
            else:
                st.info(
                    "Quy tắc hiện tại chưa phát hiện từ khóa đáng chú ý. "
                    "Điều này không đồng nghĩa nội dung chắc chắn an toàn."
                )

            if result["url_notes"]:
                st.write("**Lưu ý về đường link:**")
                for note in result["url_notes"]:
                    st.write(f"- {note}")

            if analyze_clicked:
                with st.spinner("Gemini đang phân tích nội dung..."):
                    ai_text, error = ask_gemini(content)

                if ai_text:
                    st.subheader("🧠 Phân tích từ Gemini AI")
                    st.markdown(ai_text)
                else:
                    st.warning(error)
                    st.info(
                        "Em vẫn có thể dùng phần kiểm tra quy tắc ở trên. "
                        "Kết quả quy tắc không thay thế việc xác minh nguồn."
                    )

            st.markdown("""
            <div class="panel">
            <b>🔐 Nhớ an toàn:</b><br>
            Không gửi OTP, mật khẩu hay giấy tờ cá nhân cho người lạ.
            Hãy kiểm tra thông tin qua nguồn chính thức và độc lập.
            </div>
            """, unsafe_allow_html=True)

            st.session_state.history.insert(0, {
                "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Nội dung": content[:160],
                "Điểm quy tắc": result["score"],
                "Đánh giá": result["level"],
                "Đã gọi AI": bool(analyze_clicked),
            })


# ---------- TRANG 2: TÌNH HUỐNG ----------
elif page == "🧩 Thử tình huống":
    st.title("🧩 Phòng thực hành tình huống")
    st.write(
        "Luyện tập cách xử lý tin nhắn, đường link và thông tin đáng nghi. "
        "Mỗi lượt em có thể gặp một tình huống khác."
    )

    if st.session_state.current_scenario is None:
        st.session_state.current_scenario = random.randrange(len(SCENARIOS))

    current = st.session_state.current_scenario
    scenario = SCENARIOS[current]

    st.markdown(f"### {scenario['title']}")
    st.markdown(
        f'<div class="panel">{scenario["text"]}</div>',
        unsafe_allow_html=True,
    )

    answer = st.radio(
        "Em sẽ làm gì?",
        scenario["choices"],
        key=f"answer_{current}",
    )

    if st.button("Kiểm tra câu trả lời"):
        correct = scenario["choices"].index(answer) == scenario["correct"]
        st.session_state.scenario_result = {
            "index": current,
            "correct": correct,
            "explain": scenario["explain"],
        }

        if correct:
            st.success("Chính xác! Em đã chọn cách xử lý an toàn hơn.")
        else:
            st.warning("Chưa chính xác. Mình cùng xem lại tình huống nhé.")

        st.info(scenario["explain"])

    if st.button("🎲 Đổi tình huống khác"):
        unseen = [
            i for i in range(len(SCENARIOS))
            if i not in st.session_state.seen_scenarios
            and i != current
        ]

        if not unseen:
            unseen = [i for i in range(len(SCENARIOS)) if i != current]

        st.session_state.seen_scenarios.append(current)
        st.session_state.current_scenario = random.choice(unseen)
        st.rerun()


# ---------- TRANG 3: KHẢO SÁT ----------
elif page == "📝 Khảo sát nhanh":
    st.title("📝 Khảo sát kỹ năng xác thực")
    st.write(
        "Khảo sát tự đánh giá phục vụ học tập và nghiên cứu. "
        "Đây không phải bài kiểm tra năng lực đã được chuẩn hóa."
    )

    with st.form("survey_form"):
        q1 = st.select_slider(
            "1. Em thường kiểm tra nguồn trước khi chia sẻ thông tin?",
            options=[1, 2, 3, 4, 5],
            value=3,
        )
        q2 = st.select_slider(
            "2. Em nhận ra yêu cầu OTP hoặc chuyển tiền đáng nghi?",
            options=[1, 2, 3, 4, 5],
            value=3,
        )
        q3 = st.select_slider(
            "3. Em biết đối chiếu thông tin từ nhiều nguồn?",
            options=[1, 2, 3, 4, 5],
            value=3,
        )
        q4 = st.select_slider(
            "4. Em biết cách kiểm tra đường link trước khi mở?",
            options=[1, 2, 3, 4, 5],
            value=3,
        )
        q5 = st.select_slider(
            "5. Em sẵn sàng dừng lại khi nội dung tạo áp lực?",
            options=[1, 2, 3, 4, 5],
            value=3,
        )

        submitted = st.form_submit_button("Lưu kết quả khảo sát")

    if submitted:
        score = round((q1 + q2 + q3 + q4 + q5) / 25 * 100)
        st.session_state.survey_results.append({
            "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Điểm tự đánh giá": score,
        })
        st.success(f"Đã lưu kết quả phiên hiện tại: {score}/100")
        st.caption(
            "Điểm cao thể hiện mức tự đánh giá cao hơn, "
            "không tự động chứng minh kỹ năng thực tế."
        )


# ---------- TRANG 4: THỐNG KÊ ----------
elif page == "📊 Lịch sử & thống kê":
    st.title("📊 Lịch sử & thống kê")
    st.write("Dữ liệu dưới đây chỉ lưu trong phiên hoạt động hiện tại của ứng dụng.")

    history = st.session_state.history
    surveys = st.session_state.survey_results

    c1, c2, c3 = st.columns(3)
    c1.metric("Lượt phân tích", len(history))
    c2.metric("Lượt khảo sát", len(surveys))
    c3.metric(
        "Lượt đã gọi AI",
        sum(1 for item in history if item["Đã gọi AI"]),
    )

    if history:
        st.subheader("Lịch sử phân tích")
        st.dataframe(history, use_container_width=True)

        import pandas as pd
        csv_data = pd.DataFrame(history).to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "⬇️ Tải lịch sử dạng CSV",
            data=csv_data,
            file_name="lich_su_social_sandbox.csv",
            mime="text/csv",
        )
    else:
        st.info("Chưa có lượt phân tích nào trong phiên hiện tại.")

    if surveys:
        st.subheader("Kết quả khảo sát")
        st.dataframe(surveys, use_container_width=True)
    else:
        st.info("Chưa có kết quả khảo sát trong phiên hiện tại.")


# ---------- TRANG 5: GIỚI THIỆU ----------
elif page == "ℹ️ Về đề tài":
    st.title("ℹ️ Về đề tài nghiên cứu")

    st.markdown("""
    <div class="panel">
    <h3>🛡️ Social Sandbox AI</h3>
    <p><b>Tên đề tài:</b> Nghiên cứu hành vi xác thực thông tin số của học sinh
    trung học và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.</p>
    <p><b>Mục tiêu:</b> Hỗ trợ học sinh nhận biết dấu hiệu đáng nghi, thực hành
    kiểm chứng thông tin và rèn luyện tư duy phản biện.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Các chức năng")
    st.markdown("""
    - **Phân tích quy tắc:** nhận diện một số từ khóa và dấu hiệu đơn giản.
    - **Gemini AI:** giải thích nội dung, nêu rủi ro sơ bộ và đề xuất cách kiểm chứng.
    - **Phòng tình huống:** luyện tập lựa chọn cách xử lý an toàn.
    - **Khảo sát và thống kê:** lưu dữ liệu tạm thời trong phiên sử dụng.
    """)

    st.subheader("Giới hạn cần biết")
    st.warning("""
    AI có thể nhầm lẫn hoặc đưa ra nhận định chưa chính xác. Ứng dụng không
    tự động xác nhận một tin là thật hay giả, không tra cứu danh tiếng đường
    link trực tiếp và không thay thế việc kiểm chứng từ nguồn đáng tin cậy.
    Dữ liệu thống kê hiện chưa được lưu vào cơ sở dữ liệu lâu dài.
    """)

st.divider()
st.caption(
    "Social Sandbox AI • Công cụ giáo dục và nghiên cứu • "
    "Luôn kiểm chứng thông tin trước khi chia sẻ."
)
def get_api_key():
    try:
        return st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        return ""
