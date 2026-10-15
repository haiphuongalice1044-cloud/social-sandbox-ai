
import streamlit as st
import pandas as pd
import re
import random
from datetime import datetime

# =========================
# SOCIAL SANDBOX AI 2.0
# =========================
st.set_page_config(
    page_title="Social Sandbox AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- STYLE ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #19264b 0%, transparent 38%),
        radial-gradient(ellipse at 90% 10%, #25204a 0%, transparent 35%),
        #080d1a;
    color: #edf2ff;
}
[data-testid="stSidebar"] {
    background: #0d1426;
    border-right: 1px solid #263451;
}
[data-testid="stSidebar"] * { color: #e5ecff; }
h1, h2, h3 { color: #f4f7ff !important; }
p, label, span { color: #d4def5; }
.hero {
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(120deg, #17294a, #242044);
    border: 1px solid #35476c;
    margin-bottom: 24px;
}
.hero h1 { font-size: 35px; margin: 0; }
.hero p { color: #b8c9ee; margin-top: 10px; }
.eyebrow {
    color: #78e8f4;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}
.metric {
    background: linear-gradient(145deg, #151f36, #10172a);
    border: 1px solid #2a3958;
    padding: 20px;
    border-radius: 17px;
    min-height: 130px;
}
.metric-label { color: #9eafd0; font-size: 13px; }
.metric-value { font-size: 30px; font-weight: 800; margin: 8px 0; }
.metric-note { color: #77e6c3; font-size: 12px; }
.panel {
    background: #111a2d;
    border: 1px solid #283854;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
}
.tag {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 8px;
    background: #202e4a;
    color: #8fe9f5;
    font-size: 12px;
    font-weight: 700;
}
div.stButton > button {
    border-radius: 10px;
    border: 1px solid #536ee7;
    background: linear-gradient(90deg, #465fe0, #7654db);
    color: white;
    font-weight: 700;
    min-height: 43px;
}
div.stButton > button:hover {
    border-color: #9cecf5;
    color: white;
}
.stTextArea textarea, .stTextInput input {
    background: #0c1425 !important;
    color: #f1f5ff !important;
    border: 1px solid #334462 !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background: #101a2d;
    border-color: #334462;
}
hr { border-color: #293750; }
.small-muted { color: #91a2c2; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE ----------
defaults = {
    "records": [],
    "analysis": None,
    "post_text": "",
    "quiz_before": None,
    "quiz_after": None,
    "verified_steps": [],
    "feedback_history": []
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- ANALYSIS ENGINE ----------
RISK_RULES = {
    "Ngôn ngữ gây hoảng sợ": [
        "khẩn cấp", "ngay lập tức", "sắp tận thế", "kinh hoàng",
        "cực sốc", "không thể tin", "nguy hiểm chết người"
    ],
    "Kêu gọi chia sẻ gấp": [
        "chia sẻ ngay", "share ngay", "gửi cho tất cả",
        "lan truyền", "đừng bỏ lỡ", "tag bạn bè"
    ],
    "Thiếu nguồn kiểm chứng": [
        "nghe nói", "người ta bảo", "theo nguồn tin riêng",
        "một người bạn nói", "không rõ nguồn"
    ],
    "Khẳng định tuyệt đối": [
        "100% chính xác", "chắc chắn đúng", "ai cũng biết",
        "không thể sai", "sự thật tuyệt đối"
    ],
    "Lời hứa hoặc quà tặng bất thường": [
        "trúng thưởng", "nhận tiền miễn phí", "quà miễn phí",
        "bấm vào link", "nhập mật khẩu", "xác minh tài khoản"
    ],
    "Nội dung sức khỏe cần kiểm tra": [
        "chữa khỏi hoàn toàn", "thuốc thần kỳ", "không cần bác sĩ",
        "bí quyết chữa bệnh", "khỏi bệnh ngay"
    ]
}

def analyze_text(text):
    text_lower = text.lower()
    findings = []
    score = 0

    for category, words in RISK_RULES.items():
        matched = [word for word in words if word in text_lower]
        if matched:
            findings.append({
                "category": category,
                "words": matched
            })
            score += min(22, 8 + len(matched) * 4)

    if re.search(r"https?://|www\.", text_lower):
        findings.append({
            "category": "Có đường liên kết",
            "words": ["URL/link"]
        })
        score += 8

    if text.count("!") >= 3 or text.count("?") >= 4:
        findings.append({
            "category": "Dấu câu gây chú ý mạnh",
            "words": ["nhiều dấu chấm than hoặc hỏi"]
        })
        score += 6

    score = min(score, 100)

    if score >= 60:
        level = "Cao"
        advice = "Tạm dừng chia sẻ và kiểm tra nhiều nguồn độc lập trước khi tin."
    elif score >= 30:
        level = "Trung bình"
        advice = "Cần xác minh tác giả, thời gian đăng và bằng chứng."
    else:
        level = "Thấp theo quy tắc hiện tại"
        advice = "Chưa phát hiện nhiều dấu hiệu trong danh sách; điều này không chứng minh thông tin đúng."

    return {
        "score": score,
        "level": level,
        "findings": findings,
        "advice": advice,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": text
    }

def save_record(result):
    st.session_state.records.append({
        "Thời gian": result["timestamp"],
        "Điểm rủi ro": result["score"],
        "Mức cảnh báo": result["level"],
        "Số dấu hiệu": len(result["findings"]),
        "Nội dung": result["text"][:500]
    })

def metric_card(label, value, note):
    st.markdown(
        f"""<div class="metric">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
        </div>""",
        unsafe_allow_html=True
    )

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("## 🛡️ SOCIAL SANDBOX")
    st.markdown('<span class="tag">RESEARCH LAB · v2.0</span>',
                unsafe_allow_html=True)
    st.write("")
    page = st.radio(
        "ĐIỀU HƯỚNG",
        [
            "01 · Dashboard",
            "02 · Phân tích nội dung",
            "03 · Phòng kiểm chứng",
            "04 · Phản hồi thích ứng",
            "05 · Thống kê nghiên cứu",
            "06 · Giới thiệu đề tài"
        ],
        label_visibility="visible"
    )
    st.divider()
    st.markdown("### Trạng thái hệ thống")
    st.write("🟢 Ứng dụng đang hoạt động")
    st.write("🔎 Phân tích theo quy tắc")
    st.markdown(
        '<p class="small-muted">Môi trường mô phỏng phục vụ học tập '
        'và nghiên cứu năng lực xác thực thông tin số.</p>',
        unsafe_allow_html=True
    )

# ---------- HERO ----------
def hero(title, subtitle, eyebrow="DIGITAL LITERACY · AI LAB"):
    st.markdown(
        f"""<div class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
        </div>""",
        unsafe_allow_html=True
    )

# ---------- PAGE 1 ----------
if page.startswith("01"):
    hero("Digital Intelligence Dashboard",
         "Không gian mô phỏng giúp học sinh đánh giá thông tin trước khi chia sẻ.")

    records = st.session_state.records
    total = len(records)
    avg_risk = round(sum(r["Điểm rủi ro"] for r in records) / total, 1) if total else 0
    high = sum(1 for r in records if r["Mức cảnh báo"] == "Cao")
    verified = len(st.session_state.verified_steps)

    cols = st.columns(4)
    with cols[0]:
        metric_card("LƯỢT PHÂN TÍCH", total, "Lượt trong phiên hiện tại")
    with cols[1]:
        metric_card("RỦI RO TRUNG BÌNH", f"{avg_risk}/100", "Điểm theo quy tắc")
    with cols[2]:
        metric_card("CẢNH BÁO CAO", high, "Cần kiểm chứng cẩn thận")
    with cols[3]:
        metric_card("BƯỚC KIỂM CHỨNG", verified, "Lượt đánh dấu hoàn thành")

    st.write("")
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("📈 Hoạt động phân tích")
        if records:
            df = pd.DataFrame(records)
            chart_df = df.reset_index()
            chart_df["Lượt"] = chart_df.index + 1
            st.line_chart(chart_df.set_index("Lượt")["Điểm rủi ro"])
        else:
            st.info("Chưa có dữ liệu. Hãy sang trang Phân tích nội dung để thử.")
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🧠 Quy trình tư duy")
        st.write("**01. Dừng lại** — Đừng vội tin hoặc chia sẻ.")
        st.write("**02. Kiểm tra** — Tìm tác giả và nguồn gốc.")
        st.write("**03. Đối chiếu** — So sánh nhiều nguồn độc lập.")
        st.write("**04. Quyết định** — Chỉ chia sẻ khi có đủ căn cứ.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.caption("Dữ liệu được lưu trong phiên Streamlit hiện tại; tải CSV tại trang Thống kê để lưu lại.")

# ---------- PAGE 2 ----------
elif page.startswith("02"):
    hero("AI Content Analysis",
         "Phân tích dấu hiệu ngôn ngữ có thể xuất hiện trong thông tin chưa được kiểm chứng.")

    examples = {
        "Tự nhập nội dung": "",
        "Ví dụ: Tin gây hoảng sợ": "KHẨN CẤP! Chia sẻ ngay thông tin này cho tất cả mọi người! Nghe nói có một nguy hiểm mới nhưng chưa rõ nguồn.",
        "Ví dụ: Quà tặng bất thường": "Bạn đã trúng thưởng! Bấm vào link ngay và nhập mật khẩu để nhận tiền miễn phí.",
        "Ví dụ: Thông tin cần nguồn": "Một bài đăng nói rằng phương pháp này chữa khỏi hoàn toàn bệnh mà không cần bác sĩ."
    }

    example_choice = st.selectbox("Chọn nội dung thử nghiệm", list(examples.keys()))
    if st.button("Nạp ví dụ vào ô phân tích"):
        st.session_state.post_text = examples[example_choice]
        st.rerun()

    text = st.text_area(
        "Nội dung bài đăng cần kiểm tra",
        key="post_text",
        height=190,
        placeholder="Dán nội dung bài đăng vào đây..."
    )

    col_a, col_b = st.columns([1, 1])
    with col_a:
        run_analysis = st.button("🔍 PHÂN TÍCH NỘI DUNG", use_container_width=True)
    with col_b:
        clear_text = st.button("Xóa nội dung", use_container_width=True)

    if clear_text:
        st.session_state.post_text = ""
        st.session_state.analysis = None
        st.rerun()

    if run_analysis:
        if len(text.strip()) < 10:
            st.warning("Em hãy nhập nội dung dài hơn để hệ thống phân tích.")
        else:
            result = analyze_text(text.strip())
            st.session_state.analysis = result
            save_record(result)

    result = st.session_state.analysis
    if result:
        st.divider()
        st.subheader("Kết quả phân tích")
        a, b, c = st.columns(3)
        with a:
            metric_card("ĐIỂM RỦI RO", f'{result["score"]}/100', "Điểm dựa trên dấu hiệu nhận diện")
        with b:
            metric_card("MỨC CẢNH BÁO", result["level"], "Không phải kết luận đúng/sai")
        with c:
            metric_card("DẤU HIỆU TÌM THẤY", len(result["findings"]), "Nhóm dấu hiệu được nhận diện")

        st.progress(result["score"] / 100)
        st.info(result["advice"])

        st.subheader("Các dấu hiệu cần xem xét")
        if result["findings"]:
            for finding in result["findings"]:
                with st.expander(f'⚠️ {finding["category"]}'):
                    st.write("Dấu hiệu khớp:", ", ".join(finding["words"]))
                    st.write("Gợi ý: kiểm tra ngữ cảnh, nguồn gốc và bằng chứng độc lập.")
        else:
            st.success("Không phát hiện từ khóa trong danh sách quy tắc hiện tại. Vẫn cần kiểm chứng nguồn và bằng chứng.")

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🧭 Bước tiếp theo")
        st.write("1. Tìm bài đăng hoặc thông tin gốc.")
        st.write("2. Kiểm tra ngày đăng, tác giả và bằng chứng.")
        st.write("3. Đối chiếu với nguồn đáng tin cậy.")
        st.write("4. Không chia sẻ nếu chưa đủ căn cứ.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.caption("Giới hạn: hệ thống sử dụng từ khóa và quy tắc đơn giản, không xác minh sự thật trên Internet, không phát hiện deepfake và có thể bỏ sót hoặc đánh dấu nhầm.")

# ---------- PAGE 3 ----------
elif page.startswith("03"):
    hero("Verification Center",
         "Thực hành kiểm chứng có hệ thống trước khi tin hoặc chia sẻ thông tin.")

    st.markdown("### Checklist xác thực thông tin")
    steps = [
        "Tìm được nguồn đăng ban đầu",
        "Kiểm tra tác giả và đơn vị xuất bản",
        "Kiểm tra ngày đăng và ngữ cảnh",
        "Tìm nguồn độc lập để đối chiếu",
        "Kiểm tra hình ảnh, số liệu và bằng chứng"
    ]

    for i, step in enumerate(steps):
        key = f"verify_{i}"
        checked = st.checkbox(step, key=key)
        if checked and step not in st.session_state.verified_steps:
            st.session_state.verified_steps.append(step)
        elif not checked and step in st.session_state.verified_steps:
            st.session_state.verified_steps.remove(step)

    completed = sum(1 for s in steps if s in st.session_state.verified_steps)
    st.progress(completed / len(steps))
    st.write(f"**Tiến độ:** {completed}/{len(steps)} bước")

    if completed == len(steps):
        st.success("Em đã hoàn thành checklist. Hãy ghi nhớ: hoàn thành checklist không tự động chứng minh thông tin là đúng.")

    st.divider()
    st.subheader("Công cụ tư duy phản biện")
    question = st.selectbox(
        "Chọn câu hỏi để tự đánh giá",
        [
            "Ai là người tạo ra thông tin này?",
            "Bằng chứng nào hỗ trợ cho khẳng định?",
            "Có nguồn độc lập nào xác nhận không?",
            "Thông tin có bị cắt khỏi ngữ cảnh không?",
            "Ai có thể hưởng lợi nếu mình tin hoặc chia sẻ?"
        ]
    )
    st.info(question)
    st.text_area("Ghi chú kiểm chứng của em", key="verification_notes", height=100)

    if st.button("Lưu kết quả kiểm chứng"):
        st.session_state.feedback_history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Kiểm chứng",
            "detail": f"Hoàn thành {completed}/5 bước. Câu hỏi: {question}"
        })
        st.success("Đã lưu ghi chú hoạt động trong phiên hiện tại.")

# ---------- PAGE 4 ----------
elif page.startswith("04"):
    hero("Adaptive Feedback Engine",
         "Câu hỏi gợi mở giúp người học chậm lại, đánh giá bằng chứng và đưa ra quyết định.")

    result = st.session_state.analysis

    if result:
        score = result["score"]
        st.write(f"Phân tích gần nhất: **{result['level']}** — {score}/100")
        if score >= 60:
            prompts = [
                "Điều gì khiến em muốn chia sẻ thông tin này ngay lập tức?",
                "Em có thể tìm nguồn gốc ban đầu trước khi quyết định không?",
                "Nếu thông tin sai, ai có thể bị ảnh hưởng?"
            ]
            st.warning("Mức hỗ trợ: Dừng lại và kiểm tra kỹ.")
        elif score >= 30:
            prompts = [
                "Nguồn nào có thể xác nhận khẳng định này?",
                "Có bằng chứng nào còn thiếu không?",
                "Em có thể so sánh với một nguồn độc lập nào?"
            ]
            st.info("Mức hỗ trợ: Đặt câu hỏi và đối chiếu.")
        else:
            prompts = [
                "Em đã kiểm tra tác giả và thời gian đăng chưa?",
                "Có bằng chứng độc lập nào hỗ trợ thông tin không?",
                "Em sẽ làm gì nếu chưa thể xác minh?"
            ]
            st.success("Mức hỗ trợ: Duy trì thói quen xác thực.")
    else:
        prompts = [
            "Ai là người tạo ra thông tin này?",
            "Bằng chứng nào có thể xác nhận thông tin?",
            "Em có nên chia sẻ khi chưa chắc chắn?"
        ]
        st.info("Hãy phân tích một nội dung trước để nhận gợi ý phù hợp hơn.")

    st.markdown("### Câu hỏi dành cho em")
    for i, prompt in enumerate(prompts, 1):
        st.markdown(f'<div class="panel"><b>Câu {i}</b><br>{prompt}</div>',
                    unsafe_allow_html=True)

    st.subheader("Quyết định của người học")
    decision = st.radio(
        "Sau khi suy nghĩ, em sẽ:",
        [
            "Tạm dừng và kiểm tra thêm",
            "Tìm nguồn độc lập để đối chiếu",
            "Chưa chia sẻ vì chưa đủ bằng chứng",
            "Đã có đủ căn cứ để tiếp tục đánh giá"
        ]
    )
    reflection = st.text_area(
        "Vì sao em chọn quyết định này?",
        placeholder="Viết ngắn gọn suy nghĩ của em..."
    )

    if st.button("Ghi nhận phản hồi"):
        st.session_state.feedback_history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Phản hồi thích ứng",
            "detail": f"{decision}. Lý do: {reflection}"
        })
        st.success("Đã ghi nhận phản hồi trong phiên hiện tại.")

# ---------- PAGE 5 ----------
elif page.startswith("05"):
    hero("Research & Analytics Lab",
         "Theo dõi hoạt động mô phỏng và xuất dữ liệu phục vụ phân tích nghiên cứu.")

    records = st.session_state.records
    if records:
        df = pd.DataFrame(records)
        a, b, c = st.columns(3)
        with a:
            metric_card("TỔNG LƯỢT", len(df), "Lượt phân tích")
        with b:
            metric_card("ĐIỂM TRUNG BÌNH", round(df["Điểm rủi ro"].mean(), 1), "Trên thang 100")
        with c:
            metric_card("DẤU HIỆU TRUNG BÌNH", round(df["Số dấu hiệu"].mean(), 1), "Mỗi nội dung")

        st.subheader("Phân bố mức cảnh báo")
        counts = df["Mức cảnh báo"].value_counts()
        st.bar_chart(counts)

        st.subheader("Nhật ký phân tích")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Tải dữ liệu phân tích CSV",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="social_sandbox_research.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("Chưa có lượt phân tích. Hãy sang trang 02 để thử nghiệm.")

    st.divider()
    st.subheader("Đánh giá trước và sau trải nghiệm")

    quiz = [
        {
            "q": "Nếu một bài đăng yêu cầu chia sẻ ngay nhưng không có nguồn, em nên làm gì?",
            "options": [
                "Chia sẻ ngay",
                "Kiểm tra nguồn và bằng chứng trước",
                "Tin vì nhiều người đăng"
            ],
            "answer": "Kiểm tra nguồn và bằng chứng trước"
        },
        {
            "q": "Một bài viết có nhiều lượt thích có nghĩa là thông tin chắc chắn đúng?",
            "options": ["Có", "Không"],
            "answer": "Không"
        },
        {
            "q": "Cách nào giúp kiểm chứng thông tin tốt hơn?",
            "options": [
                "Chỉ đọc tiêu đề",
                "Tin người quen",
                "Đối chiếu các nguồn độc lập"
            ],
            "answer": "Đối chiếu các nguồn độc lập"
        }
    ]

    mode = st.radio("Chọn lượt đánh giá", ["Trước trải nghiệm", "Sau trải nghiệm"], horizontal=True)
    answers = []
    for i, item in enumerate(quiz):
        choice = st.radio(item["q"], item["options"], key=f"{mode}_{i}")
        answers.append(choice)

    if st.button("Chấm điểm bài đánh giá"):
        correct = sum(1 for i, item in enumerate(quiz) if answers[i] == item["answer"])
        score = round(correct / len(quiz) * 100)
        if mode == "Trước trải nghiệm":
            st.session_state.quiz_before = score
        else:
            st.session_state.quiz_after = score
        st.success(f"Điểm của em: {score}/100")

    if st.session_state.quiz_before is not None or st.session_state.quiz_after is not None:
        q1, q2 = st.columns(2)
        with q1:
            metric_card("ĐIỂM TRƯỚC", f'{st.session_state.quiz_before if st.session_state.quiz_before is not None else "—"}',
                        "Phần trăm câu đúng")
        with q2:
            metric_card("ĐIỂM SAU", f'{st.session_state.quiz_after if st.session_state.quiz_after is not None else "—"}',
                        "Phần trăm câu đúng")

        if st.session_state.quiz_before is not None and st.session_state.quiz_after is not None:
            delta = st.session_state.quiz_after - st.session_state.quiz_before
            if delta > 0:
                st.success(f"Điểm sau trải nghiệm tăng {delta} điểm phần trăm.")
            elif delta < 0:
                st.info(f"Điểm sau trải nghiệm giảm {abs(delta)} điểm phần trăm. Hãy xem lại câu trả lời.")
            else:
                st.info("Điểm hai lần bằng nhau.")

    if st.session_state.feedback_history:
        st.divider()
        st.subheader("Nhật ký phản hồi và kiểm chứng")
        st.dataframe(pd.DataFrame(st.session_state.feedback_history),
                     use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Tải nhật ký phản hồi CSV",
            data=pd.DataFrame(st.session_state.feedback_history).to_csv(index=False).encode("utf-8-sig"),
            file_name="social_sandbox_feedback.csv",
            mime="text/csv"
        )

    st.caption("Lưu ý nghiên cứu: dữ liệu trong ứng dụng chỉ tồn tại trong phiên hiện tại. Đây là dữ liệu thử nghiệm, không tự động đại diện cho toàn bộ học sinh.")

# ---------- PAGE 6 ----------
elif page.startswith("06"):
    hero("About the Research",
         "Nghiên cứu hành vi xác thực thông tin số của học sinh trung học và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.")

    st.markdown("### 🎯 Mục tiêu")
    st.write(
        "Xây dựng môi trường mô phỏng để học sinh luyện tập nhận diện dấu hiệu đáng ngờ, "
        "kiểm chứng thông tin và suy nghĩ trước khi chia sẻ nội dung số."
    )

    st.markdown("### 🧩 Các thành phần chính")
    features = [
        ("Phân tích nội dung", "Nhận diện một số dấu hiệu ngôn ngữ cần kiểm tra."),
        ("Phòng kiểm chứng", "Hướng dẫn quy trình xác minh nguồn và bằng chứng."),
        ("Phản hồi thích ứng", "Đưa ra câu hỏi gợi mở theo mức cảnh báo."),
        ("Thống kê nghiên cứu", "Theo dõi hoạt động và hỗ trợ xuất dữ liệu."),
        ("Đánh giá trước/sau", "Hỗ trợ quan sát thay đổi điểm số trong bài kiểm tra mô phỏng.")
    ]
    for title, description in features:
        st.markdown(f'<div class="panel"><b>{title}</b><br>{description}</div>',
                    unsafe_allow_html=True)

    st.markdown("### ⚠️ Giới hạn và đạo đức nghiên cứu")
    st.write(
        "- Phiên bản hiện tại dùng bộ quy tắc từ khóa, chưa tích hợp mô hình AI được huấn luyện.\n"
        "- Điểm rủi ro không phải xác suất tin giả và không phải kết luận đúng/sai.\n"
        "- Không nhập thông tin cá nhân, mật khẩu hoặc dữ liệu nhạy cảm.\n"
        "- Khi thử nghiệm với học sinh, cần xin phép nhà trường và tuân thủ nguyên tắc bảo vệ dữ liệu.\n"
        "- Kết quả trước/sau cần được diễn giải thận trọng, không khẳng định quan hệ nhân quả chỉ từ một bài kiểm tra nhỏ."
    )

    st.markdown("### 🛠️ Công nghệ")
    st.write("Python · Streamlit · Pandas · Quy tắc phân tích văn bản · Biểu đồ thống kê")

    st.caption("Social Sandbox AI 2.0 — phiên bản mô phỏng phục vụ học tập và nghiên cứu.")

# ---------- FOOTER ----------
st.divider()
st.markdown(
    '<p class="small-muted" style="text-align:center;">'
    'SOCIAL SANDBOX AI · DIGITAL LITERACY RESEARCH · '
    'Hãy dừng lại, kiểm tra và suy nghĩ trước khi chia sẻ.'
    '</p>',
    unsafe_allow_html=True
)
