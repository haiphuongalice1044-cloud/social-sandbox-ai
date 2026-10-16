import streamlit as st
import csv
import io
from datetime import datetime

st.set_page_config(page_title="Social Sandbox AI | Digital Trust Lab", page_icon="🧬", layout="wide", initial_sidebar_state="expanded")

# ---------------- SESSION STATE ----------------
DEFAULTS = {
    "records": [], "analysis_result": None, "analysis_count": 0,
    "verified_count": 0, "reflection_count": 0,
    "pre_score": None, "post_score": None,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- VISUAL SYSTEM ----------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root { --bg:#070a16; --panel:rgba(17,23,46,.78); --line:rgba(148,163,255,.17); --text:#f2f5ff; --muted:#a4afcf; --violet:#a78bfa; --cyan:#67e8f9; }
html, body, [class*="css"], [data-testid="stAppViewContainer"] { font-family:'Be Vietnam Pro',sans-serif; }
.stApp { background: radial-gradient(ellipse at 10% 0%, rgba(109,40,217,.24), transparent 35%), radial-gradient(ellipse at 88% 12%, rgba(6,182,212,.15), transparent 31%), radial-gradient(ellipse at 50% 100%, rgba(76,29,149,.13), transparent 40%), var(--bg); color:var(--text); }
[data-testid="stHeader"] { background:rgba(7,10,22,.7); }
[data-testid="stToolbar"] { right:1rem; }
[data-testid="stSidebar"] { background:linear-gradient(180deg,rgba(13,17,39,.98),rgba(8,12,29,.98)); border-right:1px solid var(--line); }
[data-testid="stSidebar"] * { color:#e8edff; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { border:1px solid transparent; border-radius:13px; padding:10px 12px; margin:3px 0; transition:all .2s ease; background:rgba(255,255,255,.025); }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(139,92,246,.14); border-color:rgba(167,139,250,.3); }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 { font-family:'Space Grotesk',sans-serif; letter-spacing:-1px; }
[data-testid="stSidebar"] hr { border-color:var(--line); }
.block-container { padding-top:2rem; padding-bottom:3rem; max-width:1450px; }
h1,h2,h3 { font-family:'Space Grotesk','Be Vietnam Pro',sans-serif !important; letter-spacing:-.5px; }
p,li,label { line-height:1.65; }
.hero { position:relative; overflow:hidden; padding:clamp(25px,4vw,46px); border-radius:28px; border:1px solid rgba(167,139,250,.28); background:linear-gradient(120deg,rgba(26,22,64,.94),rgba(18,29,68,.88) 54%,rgba(8,54,78,.82)); box-shadow:0 22px 70px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.07); margin-bottom:22px; }
.hero:before { content:''; position:absolute; width:330px; height:330px; right:-80px; top:-160px; border-radius:50%; background:radial-gradient(circle,rgba(103,232,249,.22),rgba(167,139,250,.08) 45%,transparent 70%); pointer-events:none; }
.hero:after { content:''; position:absolute; width:220px; height:220px; right:18%; bottom:-180px; border-radius:50%; background:radial-gradient(circle,rgba(139,92,246,.24),transparent 68%); pointer-events:none; }
.eyebrow { display:inline-flex; align-items:center; gap:8px; color:#c4b5fd; border:1px solid rgba(167,139,250,.35); background:rgba(139,92,246,.12); padding:7px 12px; border-radius:999px; font-size:10px; font-weight:800; letter-spacing:1.6px; text-transform:uppercase; }
.eyebrow-dot { width:7px; height:7px; display:inline-block; border-radius:50%; background:#67e8f9; box-shadow:0 0 14px #67e8f9; }
.hero h1 { color:#fff !important; font-size:clamp(30px,4.3vw,52px); line-height:1.12; margin:19px 0 12px; max-width:850px; letter-spacing:-1.8px; }
.gradient-text { background:linear-gradient(95deg,#c4b5fd,#67e8f9); -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero p { color:#c5d0ef; font-size:15px; max-width:780px; margin:0; }
.hero-meta { display:flex; flex-wrap:wrap; gap:9px; margin-top:23px; }
.hero-tag { display:inline-block; padding:7px 11px; border-radius:10px; background:rgba(255,255,255,.055); border:1px solid rgba(255,255,255,.09); color:#dbeafe; font-size:11px; }
.section-kicker { color:#8ee9f6; font-size:10px; font-weight:800; letter-spacing:1.8px; text-transform:uppercase; margin-bottom:6px; }
.glass { background:linear-gradient(145deg,rgba(23,29,57,.86),rgba(12,18,39,.84)); border:1px solid var(--line); border-radius:20px; padding:20px; box-shadow:0 12px 35px rgba(0,0,0,.14),inset 0 1px 0 rgba(255,255,255,.035); }
.glass h3 { margin-top:2px; }
.mini-label { color:var(--muted); text-transform:uppercase; letter-spacing:1.1px; font-size:10px; font-weight:800; }
.metric-card { background:linear-gradient(145deg,rgba(24,31,62,.88),rgba(13,19,41,.9)); border:1px solid var(--line); border-radius:18px; padding:18px 19px; min-height:122px; box-shadow:0 10px 30px rgba(0,0,0,.12); }
.metric-icon { font-size:20px; margin-bottom:10px; }
.metric-value { font-family:'Space Grotesk',sans-serif; font-size:30px; font-weight:700; color:#fff; line-height:1.1; }
.metric-name { color:#aab6d7; font-size:12px; margin-top:7px; }
div[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(24,31,62,.9),rgba(13,19,41,.9)); border:1px solid var(--line); padding:16px 18px; border-radius:18px; box-shadow:0 10px 30px rgba(0,0,0,.13); }
div[data-testid="stMetricLabel"] { color:#aab6d7; }
div[data-testid="stMetricValue"] { color:#fff; font-family:'Space Grotesk',sans-serif; }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button { border-radius:12px; min-height:44px; font-weight:700; border:1px solid rgba(167,139,250,.32); transition:all .18s ease; }
.stButton > button[kind="primary"], [data-testid="stFormSubmitButton"] button[kind="primary"] { background:linear-gradient(100deg,#7c3aed,#2563eb); color:#fff; box-shadow:0 8px 25px rgba(99,102,241,.22); }
.stButton > button:hover, .stDownloadButton > button:hover { border-color:#67e8f9; transform:translateY(-1px); box-shadow:0 7px 24px rgba(103,232,249,.1); }
.stTextArea textarea, .stTextInput input { background:rgba(7,12,29,.78) !important; border:1px solid rgba(148,163,255,.23) !important; color:#f1f5ff !important; border-radius:12px !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color:#8b5cf6 !important; box-shadow:0 0 0 1px #8b5cf6 !important; }
[data-baseweb="select"] > div, [data-testid="stRadio"] { border-color:var(--line); }
[data-testid="stExpander"] { border:1px solid var(--line); border-radius:15px; background:rgba(15,21,44,.62); }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; }
.stAlert { border-radius:14px; }
hr { border-color:var(--line); }
.step-num { font-family:'Space Grotesk',sans-serif; font-size:27px; font-weight:700; color:#a78bfa; }
.result-badge { display:inline-block; padding:7px 11px; border-radius:10px; background:rgba(103,232,249,.08); border:1px solid rgba(103,232,249,.2); color:#a5f3fc; font-size:11px; font-weight:800; letter-spacing:.5px; }
.footer { border-top:1px solid var(--line); padding-top:18px; color:#7f8bad; font-size:11px; margin-top:38px; }
.stCaption, [data-testid="stCaptionContainer"] { color:#98a5c8 !important; }
@media (max-width: 700px) { .hero { padding:23px; border-radius:21px; } .hero h1 { letter-spacing:-1px; } .block-container { padding-top:1rem; } }
</style>
""", unsafe_allow_html=True)

# ---------------- ANALYSIS RULES ----------------
CUES = {
    "Ngôn ngữ giật gân": ["kinh hoàng", "chấn động", "sốc toàn tập", "không thể tin nổi", "rúng động", "gây sốc", "bí mật động trời"],
    "Thúc giục chia sẻ": ["chia sẻ ngay", "share ngay", "gửi cho tất cả", "truyền đi ngay", "chia sẻ gấp", "hãy lan truyền", "chuyển tiếp ngay"],
    "Nguồn tin chưa rõ": ["nghe nói", "người ta bảo", "tin nội bộ", "nguồn tin cho biết", "một người bạn nói", "theo thông tin chưa xác nhận"],
    "Khẳng định tuyệt đối": ["100% chắc chắn", "chắc chắn đúng", "không thể sai", "đảm bảo tuyệt đối", "ai cũng biết", "sự thật chắc chắn"],
    "Gây sợ hãi hoặc áp lực": ["nếu không sẽ", "cơ hội cuối cùng", "bạn sẽ phải hối hận", "nguy hiểm cho tất cả", "đừng để quá muộn"],
}
URGENCY_WORDS = ["khẩn cấp", "ngay lập tức", "trong 5 phút", "càng nhanh càng tốt", "làm ngay", "trước khi quá muộn"]


def analyze_text(content: str) -> dict:
    normalized = content.casefold()
    findings = []
    for category, keywords in CUES.items():
        matched = [word for word in keywords if word.casefold() in normalized]
        if matched:
            findings.append({"category": category, "examples": matched})
    urgency = [word for word in URGENCY_WORDS if word.casefold() in normalized]
    score = len(findings) + (1 if urgency else 0)
    if score >= 4:
        level, color = "Nhiều dấu hiệu cần xem xét", "🔴"
    elif score >= 2:
        level, color = "Có một số dấu hiệu cần kiểm tra", "🟠"
    elif score >= 1:
        level, color = "Có dấu hiệu nên chú ý", "🟡"
    else:
        level, color = "Chưa phát hiện dấu hiệu theo bộ quy tắc", "🟢"
    return {"findings": findings, "urgency": urgency, "score": score, "level": level, "color": color, "word_count": len(content.split())}


def adaptive_feedback(result: dict) -> dict:
    score = result["score"]
    if score >= 4:
        return {"title": "⏸️ Tạm dừng và kiểm tra kỹ", "message": "Có nhiều dấu hiệu ngôn ngữ đáng xem xét. Hãy tạm hoãn chia sẻ cho đến khi kiểm tra nguồn gốc và bằng chứng.", "questions": ["Ai là nguồn đăng đầu tiên? Có xác định được đơn vị phát hành không?", "Có ít nhất hai nguồn đáng tin cậy độc lập xác nhận không?", "Bài đăng có tạo áp lực khiến người đọc sợ hãi hoặc vội vàng không?"]}
    if score >= 1:
        return {"title": "🤔 Hãy đặt câu hỏi trước khi tin", "message": "Một vài dấu hiệu xuất hiện. Điều này không chứng minh bài đăng sai, nhưng là lý do để kiểm tra thêm.", "questions": ["Bài đăng có dẫn nguồn cụ thể, có thể mở và kiểm tra được không?", "Em có thể tìm thông tin này ở trang chính thức nào?", "Ngày đăng, hình ảnh và bối cảnh có phù hợp với nội dung không?"]}
    return {"title": "🔎 Tiếp tục kiểm chứng", "message": "Bộ quy tắc chưa phát hiện dấu hiệu nổi bật. Điều đó không có nghĩa bài đăng chắc chắn đúng hoặc an toàn.", "questions": ["Ai tạo ra nội dung này và họ có chuyên môn liên quan không?", "Có nguồn độc lập nào xác nhận thông tin không?", "Em có tìm được bài gốc hoặc bằng chứng trực tiếp không?"]}


def record_activity(activity_type: str, score, details: str):
    st.session_state.records.append({"Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Hoạt động": activity_type, "Điểm/dấu hiệu": score, "Ghi chú": details})


def show_hero(eyebrow: str, title: str, subtitle: str):
    st.markdown(f'<div class="hero"><span class="eyebrow"><span class="eyebrow-dot"></span>{eyebrow}</span><h1>{title}</h1><p>{subtitle}</p><div class="hero-meta"><span class="hero-tag">✦ Digital literacy</span><span class="hero-tag">⌁ Adaptive learning</span><span class="hero-tag">◈ Research prototype</span></div></div>', unsafe_allow_html=True)


def section_heading(kicker: str, title: str, subtitle: str = ""):
    st.markdown(f'<div class="section-kicker">{kicker}</div><h2 style="margin-top:0;margin-bottom:4px">{title}</h2><p style="color:#9eaccd;margin-top:0">{subtitle}</p>', unsafe_allow_html=True)


def metric_card(icon: str, value: str, label: str):
    st.markdown(f'<div class="metric-card"><div class="metric-icon">{icon}</div><div class="metric-value">{value}</div><div class="metric-name">{label}</div></div>', unsafe_allow_html=True)


def export_csv(records):
    output = io.StringIO()
    fields = ["Thời gian", "Hoạt động", "Điểm/dấu hiệu", "Ghi chú"]
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    writer.writerows(records)
    return output.getvalue().encode("utf-8-sig")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("# ◈ Social Sandbox")
st.sidebar.markdown("<span style='color:#8ee9f6;font-size:10px;font-weight:800;letter-spacing:2px'>DIGITAL TRUST LAB · v3.0</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='color:#a7b4d5;font-size:10px;font-weight:800;letter-spacing:1.4px;margin-bottom:8px'>KHÔNG GIAN THỰC HÀNH</div>", unsafe_allow_html=True)
page = st.sidebar.radio("Chọn khu vực", ["✦ Tổng quan & phân tích", "⌕ Phòng kiểm chứng", "◉ Phản hồi thích ứng", "▦ Thống kê nghiên cứu", "◇ Giới thiệu đề tài"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='padding:14px;border:1px solid rgba(103,232,249,.18);background:rgba(103,232,249,.045);border-radius:14px'><div style='color:#67e8f9;font-size:10px;font-weight:800;letter-spacing:1.2px'>MISSION</div><div style='font-size:13px;line-height:1.7;margin-top:7px'>Suy nghĩ trước khi tin.<br>Kiểm chứng trước khi chia sẻ.</div></div>", unsafe_allow_html=True)
st.sidebar.caption("Nguyên mẫu giáo dục · Dữ liệu chỉ lưu trong phiên đang mở")

# ---------------- PAGE 1 ----------------
if page == "✦ Tổng quan & phân tích":
    show_hero("SOCIAL SANDBOX AI / INTERACTIVE LAB", "Đừng chỉ lướt qua thông tin. <span class='gradient-text'>Hãy đọc có tư duy.</span>", "Không gian mô phỏng giúp học sinh nhận diện dấu hiệu đáng nghi, kiểm tra nguồn và thực hành phản hồi trước khi chia sẻ thông tin trên môi trường số.")
    m1, m2, m3 = st.columns(3)
    with m1: metric_card("⌁", str(st.session_state.analysis_count), "LƯỢT PHÂN TÍCH")
    with m2: metric_card("◈", str(st.session_state.verified_count), "PHIẾU KIỂM CHỨNG")
    with m3: metric_card("▤", str(len(st.session_state.records)), "HOẠT ĐỘNG ĐÃ GHI NHẬN")
    st.write("")
    section_heading("01 / CONTENT INTELLIGENCE", "Phân tích dấu hiệu trong bài đăng", "Dán nội dung mô phỏng để quan sát những tín hiệu ngôn ngữ cần kiểm tra.")
    st.info("Lưu ý nghiên cứu: phiên bản hiện tại sử dụng bộ quy tắc từ khóa minh họa, chưa phải mô hình AI ngôn ngữ và không thể tự kết luận thông tin đúng hay sai.")
    with st.expander("✧ Nạp bài đăng mô phỏng để thử nhanh", expanded=False):
        example = "KHẨN CẤP! Nghe nói trường sẽ cho nghỉ học cả tuần. Chia sẻ ngay cho tất cả mọi người trước khi quá muộn!"
        st.write(example)
        if st.button("Dùng nội dung mẫu", key="use_example"):
            st.session_state.analysis_input = example
    content = st.text_area("NỘI DUNG CẦN PHÂN TÍCH", key="analysis_input", placeholder="Dán nội dung bài đăng giả lập vào đây…", height=175, help="Không nhập họ tên, số điện thoại, tài khoản hoặc thông tin cá nhân.")
    if st.button("⌕  PHÂN TÍCH DẤU HIỆU", type="primary", use_container_width=True):
        if not content.strip():
            st.warning("Em hãy nhập nội dung trước nhé.")
        else:
            result = analyze_text(content)
            feedback = adaptive_feedback(result)
            st.session_state.analysis_result = {"content": content, "result": result, "feedback": feedback}
            st.session_state.analysis_count += 1
            record_activity("Phân tích bài đăng", result["score"], result["level"])
    saved = st.session_state.analysis_result
    if saved:
        result, feedback = saved["result"], saved["feedback"]
        st.markdown("---")
        section_heading("02 / SIGNAL REPORT", "Báo cáo phân tích", "Kết quả từ bộ quy tắc hiện có — không phải kết luận xác thực sự thật.")
        left, right = st.columns([1, 2], gap="large")
        with left:
            with st.container(border=True):
                st.markdown("<div class='mini-label'>SIGNAL SCORE</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font:700 52px Space Grotesk;color:#c4b5fd'>{result['color']} {result['score']}</div>", unsafe_allow_html=True)
                st.markdown(f"<span class='result-badge'>{result['level']}</span>", unsafe_allow_html=True)
                st.write("")
                st.metric("Số từ trong nội dung", result["word_count"])
        with right:
            with st.container(border=True):
                st.markdown("**CÁC NHÓM DẤU HIỆU**")
                if result["findings"]:
                    for finding in result["findings"]:
                        st.markdown(f"**◈ {finding['category']}**")
                        st.caption("Cụm từ tìm thấy: " + ", ".join(finding["examples"]))
                else:
                    st.success("Chưa tìm thấy cụm từ thuộc các nhóm quy tắc hiện có.")
                if result["urgency"]:
                    st.warning("Ngôn ngữ thúc giục: " + ", ".join(result["urgency"]))
        st.warning("Một bài có dấu hiệu không nhất thiết là sai; một bài không có dấu hiệu cũng không chắc chắn đúng. Luôn kiểm tra nguồn và bằng chứng.")
        with st.container(border=True):
            st.markdown("<div class='section-kicker'>ADAPTIVE NEXT STEP</div>", unsafe_allow_html=True)
            st.subheader(feedback["title"])
            st.write(feedback["message"])
            for i, question in enumerate(feedback["questions"], 1):
                st.markdown(f"**{i:02d}** · {question}")

# ---------------- PAGE 2 ----------------
elif page == "⌕ Phòng kiểm chứng":
    show_hero("VERIFY / DON'T AMPLIFY", "Phòng kiểm chứng <span class='gradient-text'>thông tin</span>", "Một quy trình có cấu trúc để chuyển từ cảm giác ‘có vẻ đúng’ sang kiểm tra nguồn gốc, bằng chứng và bối cảnh.")
    section_heading("THE 5-STEP METHOD", "Quy trình kiểm chứng 5 bước", "Thực hiện lần lượt trước khi tin hoặc chia sẻ một thông tin.")
    steps = [("01", "Xác định tuyên bố", "Thông tin chính xác nào đang được khẳng định? Tách sự kiện khỏi ý kiến."), ("02", "Tìm nguồn ban đầu", "Ai đăng đầu tiên? Có đường dẫn hoặc thông báo gốc không?"), ("03", "Đối chiếu nguồn", "Kiểm tra nguồn chính thức và nguồn độc lập đáng tin cậy."), ("04", "Kiểm tra bối cảnh", "Xem ngày đăng, địa điểm, hình ảnh và nội dung có bị cắt ghép không."), ("05", "Quyết định thận trọng", "Chỉ chia sẻ khi có đủ căn cứ; nếu chưa rõ, đừng lan truyền.")]
    for number, title, description in steps:
        with st.container(border=True):
            a, b = st.columns([1, 8])
            with a: st.markdown(f"<div class='step-num'>{number}</div>", unsafe_allow_html=True)
            with b:
                st.markdown(f"**{title}**")
                st.caption(description)
    st.write("")
    section_heading("PRACTICE / FIELD NOTE", "Phiếu thực hành kiểm chứng", "Ghi lại quá trình kiểm tra của em để hình thành thói quen tư duy có căn cứ.")
    claim = st.text_input("1. Tuyên bố cần kiểm tra", placeholder="Ví dụ: Trường sẽ nghỉ học vào ngày mai")
    source = st.text_input("2. Nguồn ban đầu hoặc người phát hành", placeholder="Ví dụ: Trang thông báo chính thức của trường")
    evidence = st.text_area("3. Bằng chứng và nguồn đối chiếu", placeholder="Ghi lại những gì em đã kiểm tra…", height=100)
    checks = ["Đã tìm nguồn đăng ban đầu", "Đã kiểm tra tác giả hoặc đơn vị phát hành", "Đã đối chiếu với nguồn độc lập đáng tin", "Đã kiểm tra ngày đăng và bối cảnh", "Đã xem xét bằng chứng thay vì chỉ đọc tiêu đề"]
    selected = []
    st.markdown("**CHECKLIST / TỰ ĐÁNH GIÁ**")
    for item in checks:
        if st.checkbox(item, key="verify_" + item): selected.append(item)
    if st.button("▤  GHI NHẬN PHIẾU THỰC HÀNH", type="primary", use_container_width=True):
        if not claim.strip():
            st.warning("Hãy nhập tuyên bố cần kiểm tra trước nhé.")
        else:
            details = f"Tuyên bố: {claim}; Nguồn: {source}; Bằng chứng: {evidence}; Checklist: {len(selected)}/5"
            record_activity("Thực hành kiểm chứng", len(selected), details)
            st.session_state.verified_count += 1
            st.success(f"Đã ghi nhận {len(selected)}/5 bước trong phiên hiện tại.")
    st.caption("Phiếu chỉ lưu trong phiên đang mở. Không nhập dữ liệu cá nhân hoặc thông tin nhạy cảm.")

# ---------------- PAGE 3 ----------------
elif page == "◉ Phản hồi thích ứng":
    show_hero("ADAPTIVE LEARNING ENGINE", "Dừng lại một nhịp. <span class='gradient-text'>Suy nghĩ sâu hơn.</span>", "Phản hồi gợi mở thay đổi theo số nhóm dấu hiệu mà bộ quy tắc phát hiện — nhằm khuyến khích người học tự đặt câu hỏi.")
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result["result"]
        feedback = adaptive_feedback(result)
        with st.container(border=True):
            st.markdown("<div class='section-kicker'>PERSONALIZED PROMPT</div>", unsafe_allow_html=True)
            st.subheader(feedback["title"])
            st.write(feedback["message"])
        section_heading("THINK / QUESTION / VERIFY", "Câu hỏi gợi mở", "Hãy trả lời bằng suy nghĩ của chính em, không cần tìm đáp án hoàn hảo.")
        for i, question in enumerate(feedback["questions"], 1):
            with st.container(border=True):
                st.markdown(f"<div class='step-num'>Q{i:02d}</div>", unsafe_allow_html=True)
                st.write(question)
        reflection = st.text_area("Em sẽ làm gì trước khi chia sẻ bài đăng?", key="reflection_input", placeholder="Viết ngắn gọn cách em sẽ kiểm tra thông tin…", height=120)
        if st.button("◈  GHI NHẬN SUY NGẪM", type="primary", use_container_width=True):
            if reflection.strip():
                record_activity("Suy ngẫm", result["score"], reflection)
                st.session_state.reflection_count += 1
                st.success("Đã ghi nhận câu trả lời trong phiên này.")
            else:
                st.warning("Em hãy nhập câu trả lời trước nhé.")
    else:
        st.info("Hãy sang mục ‘Tổng quan & phân tích’ và phân tích một bài đăng trước.")
        st.markdown("Mục tiêu là giúp người học dừng lại, tự đặt câu hỏi và tìm bằng chứng. Đây là bản minh họa theo quy tắc, chưa phải hệ thống AI học từ hành vi thực tế.")

# ---------------- PAGE 4 ----------------
elif page == "▦ Thống kê nghiên cứu":
    show_hero("RESEARCH / INSIGHTS", "Biến hoạt động thành <span class='gradient-text'>dữ liệu nghiên cứu.</span>", "Theo dõi hoạt động trong phiên, so sánh kết quả đánh giá trước và sau thực hành, rồi xuất CSV để tiếp tục phân tích.")
    st.warning("Bộ câu hỏi là bản minh họa, chưa được chuẩn hóa khoa học. Khi nghiên cứu với học sinh, cần có sự cho phép phù hợp và bảo vệ quyền riêng tư.")
    questions = [
        {"q": "Một bài đăng yêu cầu chia sẻ ngay nhưng không dẫn nguồn. Em nên:", "options": ["Chia sẻ ngay", "Kiểm tra nguồn và bằng chứng trước", "Tin vì nhiều người chia sẻ"], "answer": "Kiểm tra nguồn và bằng chứng trước"},
        {"q": "Công cụ không tìm thấy dấu hiệu đáng nghi. Điều đó có nghĩa:", "options": ["Thông tin chắc chắn đúng", "Thông tin chắc chắn sai", "Chưa đủ căn cứ để kết luận"], "answer": "Chưa đủ căn cứ để kết luận"},
        {"q": "Nguồn nào nên ưu tiên khi kiểm tra thông báo của trường?", "options": ["Tài khoản không rõ danh tính", "Thông báo chính thức của nhà trường", "Bình luận chưa xác minh"], "answer": "Thông báo chính thức của nhà trường"},
        {"q": "Khi hai nguồn đưa thông tin trái ngược, em nên:", "options": ["Chọn tiêu đề hấp dẫn hơn", "So sánh nguồn gốc, bằng chứng và thời điểm", "Chia sẻ cả hai ngay"], "answer": "So sánh nguồn gốc, bằng chứng và thời điểm"},
        {"q": "Ảnh chụp màn hình có thể thiếu ngữ cảnh không?", "options": ["Có, cần tìm bản gốc và ngữ cảnh", "Không, ảnh chụp luôn đầy đủ", "Không cần kiểm tra"], "answer": "Có, cần tìm bản gốc và ngữ cảnh"},
    ]
    mode = st.radio("LẦN ĐÁNH GIÁ", ["Trước khi sử dụng", "Sau khi sử dụng"], horizontal=True)
    with st.form("assessment_form"):
        answers = []
        for i, question in enumerate(questions):
            answers.append(st.radio(f"Câu {i + 1}. {question['q']}", question["options"], key=f"assessment_{mode}_{i}"))
        submitted = st.form_submit_button("⌁  CHẤM ĐIỂM ĐÁNH GIÁ", use_container_width=True)
    if submitted:
        raw_score = sum(answer == question["answer"] for answer, question in zip(answers, questions))
        percent = round(raw_score / len(questions) * 100)
        if mode == "Trước khi sử dụng": st.session_state.pre_score = percent
        else: st.session_state.post_score = percent
        record_activity("Đánh giá kiến thức", percent, mode)
        st.success(f"Kết quả: {raw_score}/{len(questions)} câu đúng — {percent}%")
    section_heading("PRE / POST COMPARISON", "Kết quả trước và sau", "So sánh điểm phần trăm để quan sát sự thay đổi trong phiên thử nghiệm.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Trước sử dụng", "Chưa có" if st.session_state.pre_score is None else f"{st.session_state.pre_score}%")
    c2.metric("Sau sử dụng", "Chưa có" if st.session_state.post_score is None else f"{st.session_state.post_score}%")
    if st.session_state.pre_score is not None and st.session_state.post_score is not None:
        difference = st.session_state.post_score - st.session_state.pre_score
        c3.metric("Chênh lệch", f"{difference:+d} điểm %")
        st.caption("Sự thay đổi điểm không tự chứng minh hệ thống là nguyên nhân gây ra thay đổi.")
    else:
        c3.metric("Chênh lệch", "Chưa đủ dữ liệu")
    if st.session_state.pre_score is not None or st.session_state.post_score is not None:
        st.bar_chart({"Điểm phần trăm": [st.session_state.pre_score or 0, st.session_state.post_score or 0]}, height=250)
        st.caption("Biểu đồ dùng 0 cho lần đánh giá chưa thực hiện; hãy xem cùng các nhãn kết quả phía trên.")
    st.write("")
    section_heading("SESSION LOG", "Nhật ký hoạt động", "Dữ liệu được ghi nhận trong phiên trình duyệt hiện tại.")
    st.write(f"Đã ghi nhận **{len(st.session_state.records)}** hoạt động.")
    if st.session_state.records:
        st.dataframe(st.session_state.records, use_container_width=True, hide_index=True)
        st.download_button("⬇  TẢI DỮ LIỆU CSV", data=export_csv(st.session_state.records), file_name="social_sandbox_records.csv", mime="text/csv", use_container_width=True)
    else:
        st.info("Chưa có dữ liệu. Hãy thử phân tích bài đăng hoặc làm bài kiểm tra.")

# ---------------- PAGE 5 ----------------
else:
    show_hero("ABOUT / PROJECT OVERVIEW", "Một môi trường nhỏ cho <span class='gradient-text'>tư duy số an toàn.</span>", "Social Sandbox AI là nguyên mẫu giáo dục hướng tới việc giúp học sinh rèn luyện kỹ năng xác thực thông tin số thông qua trải nghiệm tương tác.")
    section_heading("PROJECT IDENTITY", "Tên đề tài")
    with st.container(border=True):
        st.markdown("*Nghiên cứu hành vi xác thực thông tin số của học sinh trung học và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.*")
    section_heading("CORE OBJECTIVES", "Mục tiêu nghiên cứu")
    cols = st.columns(2)
    objectives = [("01", "Nhận diện dấu hiệu", "Phân tích một số dấu hiệu ngôn ngữ khiến người đọc cần kiểm tra thêm."), ("02", "Luyện kiểm chứng", "Hướng dẫn học sinh đối chiếu nguồn gốc, bằng chứng và bối cảnh."), ("03", "Phản hồi thích ứng", "Đưa ra câu hỏi gợi mở nhằm khuyến khích tư duy phản biện."), ("04", "Đánh giá thực hành", "Ghi nhận hoạt động và so sánh điểm đánh giá trước/sau trong phiên.")]
    for i, (num, title, desc) in enumerate(objectives):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"<div class='step-num'>{num}</div>", unsafe_allow_html=True)
                st.markdown(f"**{title}**")
                st.caption(desc)
    section_heading("TRANSPARENCY / LIMITATIONS", "Giới hạn hiện tại")
    st.markdown("- Bộ phân tích hiện dùng luật từ khóa, **chưa phải AI ngôn ngữ thực sự**.\n- Công cụ không tự xác minh tin đúng hay sai.\n- Dữ liệu chỉ giữ trong phiên sử dụng hiện tại; người dùng có thể tải CSV để lưu.\n- Bài kiểm tra là bản minh họa, chưa được chuẩn hóa khoa học.")
    section_heading("ROADMAP", "Lộ trình phát triển")
    roadmap = [("PHASE 01", "Bản mẫu tương tác", "Giao diện, phân tích dấu hiệu, checklist kiểm chứng và thống kê phiên."), ("PHASE 02", "Đánh giá nghiên cứu", "Xây dựng bộ dữ liệu thử nghiệm, đánh giá chất lượng phân tích và cải thiện câu hỏi."), ("PHASE 03", "Tích hợp AI có kiểm soát", "Tích hợp mô hình AI khi có phương pháp đánh giá, bảo vệ dữ liệu và giới hạn sử dụng rõ ràng.")]
    for phase, title, desc in roadmap:
        with st.container(border=True):
            st.markdown(f"<div class='section-kicker'>{phase}</div>", unsafe_allow_html=True)
            st.markdown(f"**{title}**")
            st.caption(desc)

st.markdown("<div class='footer'>◈ SOCIAL SANDBOX AI · DIGITAL TRUST LAB<br>Nguyên mẫu giáo dục phục vụ học tập và nghiên cứu. Không nhập thông tin cá nhân hoặc dữ liệu nhạy cảm. Phân tích từ khóa chỉ là gợi ý học tập, không phải kết luận xác thực sự thật.</div>", unsafe_allow_html=True)
