import streamlit as st
import pandas as pd
import requests
import json
import re
from datetime import datetime

# ============================================================
# SOCIAL SANDBOX AI | LEAF GREEN EDITION
# Educational prototype: AI assistance + transparent rule-based
# signals. It does NOT independently verify whether a claim is true.
# ============================================================

st.set_page_config(
    page_title="Social Sandbox AI | Digital Literacy Lab",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- SESSION ---------------------------
DEFAULTS = {
    "history": [],
    "activities": [],
    "survey_pre": None,
    "survey_post": None,
    "last_analysis": None,
    "scenario_answers": [],
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------- THEME -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');
:root {
  --leaf-50:#F4FAF2; --leaf-100:#EAF5E9; --leaf-200:#D6EBD3;
  --leaf-300:#B8DDB2; --leaf-500:#75B982; --leaf-600:#4D985F;
  --leaf-700:#367448; --leaf-900:#285B35; --ink:#24352A;
  --muted:#6B7D70; --line:#DFEADF;
}
html, body, [class*="css"] {font-family:'Be Vietnam Pro',sans-serif;}
.stApp {background:linear-gradient(145deg,#F7FBF5 0%,#F1F8EF 48%,#FAFCF8 100%);color:var(--ink);}
[data-testid="stHeader"] {background:rgba(247,251,245,.88);}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#EAF5E9 0%,#DDEFD9 100%);border-right:1px solid #D5E8D2;}
[data-testid="stSidebar"] * {color:#285B35;}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  background:rgba(255,255,255,.68);border:1px solid #D8E9D5;
  border-radius:13px;padding:9px 12px;margin:4px 0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {background:#FFFFFF;border-color:#75B982;}
.hero {
  background:linear-gradient(115deg,#285B35 0%,#438B55 58%,#75B982 100%);
  border-radius:24px;padding:30px 32px;color:#fff;margin:4px 0 22px 0;
  box-shadow:0 14px 34px rgba(40,91,53,.13);
}
.hero .eyebrow {display:inline-block;background:rgba(255,255,255,.17);border:1px solid rgba(255,255,255,.25);
  padding:6px 11px;border-radius:30px;font-size:11px;font-weight:800;letter-spacing:.8px;}
.hero h1 {color:white!important;font-size:clamp(27px,4vw,39px);line-height:1.2;margin:12px 0 8px;}
.hero p {color:#EAF7E8!important;font-size:14px;margin:0;max-width:850px;}
.section-card {background:#fff;border:1px solid var(--line);border-radius:18px;padding:18px 20px;box-shadow:0 5px 18px rgba(40,91,53,.035);}
div[data-testid="stMetric"] {background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;box-shadow:0 4px 14px rgba(40,91,53,.035);}
.stButton>button,.stDownloadButton>button {border-radius:12px;border:1px solid #CFE4CB;font-weight:700;min-height:42px;}
.stButton>button[kind="primary"] {background:#367448;color:white;border-color:#367448;}
.stButton>button[kind="primary"]:hover {background:#285B35;border-color:#285B35;color:white;}
div[data-testid="stAlert"] {border-radius:13px;}
[data-testid="stExpander"] {background:rgba(255,255,255,.78);border:1px solid var(--line);border-radius:14px;}
h1,h2,h3 {color:#285B35;}
.small-note {color:#6B7D70;font-size:12px;}
.pill {display:inline-block;background:#EAF5E9;color:#367448;padding:5px 10px;border-radius:20px;font-size:11px;font-weight:700;}
.footer {border-top:1px solid #DFEADF;margin-top:30px;padding:16px 0;color:#718276;font-size:12px;}
</style>
""", unsafe_allow_html=True)

# ---------------------- ANALYSIS ENGINE -------------------------
CUE_GROUPS = {
    "Ngôn ngữ giật gân": [
        "kinh hoàng", "chấn động", "sốc toàn tập", "không thể tin nổi",
        "rúng động", "gây sốc", "bí mật động trời"
    ],
    "Thúc giục chia sẻ": [
        "chia sẻ ngay", "share ngay", "gửi cho tất cả", "truyền đi ngay",
        "chia sẻ gấp", "hãy lan truyền", "chuyển tiếp ngay"
    ],
    "Nguồn tin chưa rõ": [
        "nghe nói", "người ta bảo", "tin nội bộ", "nguồn tin cho biết",
        "một người bạn nói", "theo thông tin chưa xác nhận"
    ],
    "Khẳng định tuyệt đối": [
        "100% chắc chắn", "chắc chắn đúng", "không thể sai",
        "đảm bảo tuyệt đối", "ai cũng biết", "sự thật chắc chắn"
    ],
    "Gây sợ hãi hoặc áp lực": [
        "nếu không sẽ", "cơ hội cuối cùng", "bạn sẽ phải hối hận",
        "nguy hiểm cho tất cả", "đừng để quá muộn"
    ],
}
URGENCY = ["khẩn cấp", "ngay lập tức", "trong 5 phút", "càng nhanh càng tốt",
           "làm ngay", "trước khi quá muộn"]

def rule_analysis(text):
    normalized = text.casefold()
    findings = []
    for category, terms in CUE_GROUPS.items():
        hits = [term for term in terms if term.casefold() in normalized]
        if hits:
            findings.append({"category": category, "matched": hits})
    urgency_hits = [term for term in URGENCY if term.casefold() in normalized]
    score = min(100, len(findings) * 18 + (10 if urgency_hits else 0))
    if score >= 65:
        level = "Nhiều dấu hiệu cần xem xét"
    elif score >= 30:
        level = "Có một số dấu hiệu cần kiểm tra"
    elif score > 0:
        level = "Có dấu hiệu nên chú ý"
    else:
        level = "Chưa phát hiện dấu hiệu theo bộ quy tắc"
    return {
        "score": score, "level": level, "findings": findings,
        "urgency": urgency_hits, "word_count": len(text.split())
    }

def get_secret(key):
    try:
        return st.secrets.get(key, "")
    except Exception:
        return ""

def gemini_analysis(text):
    api_key = get_secret("GEMINI_API_KEY")
    if not api_key:
        return None, "Chưa cấu hình GEMINI_API_KEY. Ứng dụng sẽ dùng bộ quy tắc dự phòng."
    prompt = f"""
Bạn là trợ lý giáo dục về hiểu biết thông tin số cho học sinh trung học.
Phân tích văn bản sau theo hướng thận trọng, không khẳng định thật/giả khi không có bằng chứng.
Nêu: (1) các dấu hiệu ngôn ngữ hoặc thao túng nếu có, (2) thông tin còn thiếu,
(3) 3 câu hỏi kiểm chứng, (4) gợi ý hành động an toàn.
Nhắc rằng chỉ đọc văn bản thì không thể xác minh sự thật.
Trả lời bằng tiếng Việt, rõ ràng, phù hợp học sinh.
Văn bản cần phân tích:
{text[:7000]}
"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    try:
        response = requests.post(
            url,
            params={"key": api_key},
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}],
                  "generationConfig": {"temperature": 0.25, "maxOutputTokens": 900}},
            timeout=35,
        )
        if response.status_code != 200:
            try:
                detail = response.json().get("error", {}).get("message", "")
            except Exception:
                detail = ""
            return None, f"Gemini phản hồi HTTP {response.status_code}. {detail[:250]}"
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        return answer, None
    except requests.Timeout:
        return None, "Gemini phản hồi quá thời gian chờ. Hãy thử lại."
    except requests.RequestException:
        return None, "Không kết nối được Gemini. Kiểm tra Internet."
    except (KeyError, IndexError, TypeError, ValueError):
        return None, "Phản hồi Gemini không đúng định dạng dự kiến."

def adaptive_message(score):
    if score >= 65:
        return ("⏸️ Tạm dừng và kiểm tra kỹ",
                "Có nhiều dấu hiệu ngôn ngữ cần xem xét. Hãy tạm hoãn chia sẻ và tìm nguồn gốc, bằng chứng.")
    if score >= 30:
        return ("🤔 Hãy đặt câu hỏi trước khi tin",
                "Một vài dấu hiệu xuất hiện. Điều này không chứng minh nội dung sai, nhưng nên kiểm tra thêm.")
    if score > 0:
        return ("🔎 Chú ý và kiểm chứng",
                "Có một dấu hiệu cần xem xét. Hãy kiểm tra tác giả, thời điểm và nguồn ban đầu.")
    return ("🌱 Tiếp tục kiểm chứng",
            "Chưa phát hiện dấu hiệu theo bộ quy tắc. Điều đó không có nghĩa nội dung chắc chắn đúng.")

def log_activity(kind, detail, score=None):
    st.session_state.activities.append({
        "Thời gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Hoạt động": kind, "Điểm tín hiệu": score, "Chi tiết": str(detail)[:500]
    })

def hero(eyebrow, title, subtitle):
    st.markdown(
        f'<div class="hero"><span class="eyebrow">{eyebrow}</span>'
        f'<h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True
    )

# --------------------------- SIDEBAR ----------------------------
PAGES = [
    "🏡 Trang chủ",
    "🔎 Phân tích thông tin",
    "🧪 Mô phỏng mạng xã hội",
    "🧭 Phòng kiểm chứng",
    "💬 Phản hồi thích ứng",
    "📝 Khảo sát nghiên cứu",
    "📊 Thống kê",
    "🌿 Giới thiệu đề tài",
]
with st.sidebar:
    st.markdown("# 🌿 Social Sandbox AI")
    st.caption("DIGITAL LITERACY LAB")
    st.markdown("---")
    page = st.radio("KHÔNG GIAN KHÁM PHÁ", PAGES, label_visibility="visible")
    st.markdown("---")
    if get_secret("GEMINI_API_KEY"):
        st.success("Gemini API đã được cấu hình")
    else:
        st.info("Đang dùng chế độ phân tích dự phòng")
    st.markdown("---")
    st.caption("Pause • Verify • Think • Share responsibly")
    st.caption("Leaf Green Edition · v2.0")

# ----------------------------- HOME -----------------------------
if page == "🏡 Trang chủ":
    hero("DIGITAL LITERACY • AI RESEARCH", "Suy nghĩ trước khi tin. 🌿",
         "Không gian học tập mô phỏng giúp học sinh nhận diện dấu hiệu đáng ngờ, kiểm chứng thông tin và đưa ra quyết định có trách nhiệm trên môi trường số.")
    a, b, c, d = st.columns(4)
    a.metric("Lượt phân tích", len(st.session_state.history))
    b.metric("Tình huống đã làm", len(st.session_state.scenario_answers))
    c.metric("Hoạt động ghi nhận", len(st.session_state.activities))
    d.metric("Khảo sát", sum(x is not None for x in [st.session_state.survey_pre, st.session_state.survey_post]))
    st.markdown("### 🌱 Khám phá các khu vực")
    cards = st.columns(3)
    card_data = [
        ("🔎 Phân tích thông tin", "Sàng lọc dấu hiệu ngôn ngữ và nhận gợi ý kiểm chứng."),
        ("🧪 Mô phỏng mạng xã hội", "Luyện ra quyết định qua những tình huống giả định."),
        ("📊 Thống kê nghiên cứu", "Theo dõi hoạt động và kết quả khảo sát trong phiên.")
    ]
    for col, (title, desc) in zip(cards, card_data):
        with col:
            st.markdown(f'<div class="section-card"><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.markdown("### 🍃 Quy trình 4 bước")
    steps = st.columns(4)
    for col, (num, title, desc) in zip(steps, [
        ("01", "Dừng lại", "Không vội tin hoặc chia sẻ."),
        ("02", "Kiểm tra", "Tìm tác giả và nguồn gốc."),
        ("03", "Đối chiếu", "So sánh bằng chứng độc lập."),
        ("04", "Quyết định", "Chia sẻ khi đủ căn cứ.")
    ]):
        with col:
            st.markdown(f'<div class="section-card"><span class="pill">{num}</span><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
    st.info("Lưu ý: AI và bộ quy tắc chỉ hỗ trợ học tập, không tự xác minh sự thật hoặc thay thế đánh giá của con người.")

# ------------------------ ANALYSIS ------------------------------
elif page == "🔎 Phân tích thông tin":
    hero("CONTENT CHECK", "Phân tích dấu hiệu thông tin", "Nhập một bài đăng hoặc tin nhắn giả lập để xem những điểm cần kiểm tra.")
    st.info("Không nhập họ tên, số điện thoại, mật khẩu, mã OTP hoặc dữ liệu cá nhân của người khác.")
    sample = "KHẨN CẤP! Nghe nói trường sẽ cho nghỉ học cả tuần. Chia sẻ ngay cho tất cả mọi người trước khi quá muộn!"
    with st.expander("✨ Dùng thử nội dung mẫu"):
        st.write(sample)
        if st.button("Chèn nội dung mẫu"):
            st.session_state.analysis_text = sample
    content = st.text_area("Nội dung cần phân tích", key="analysis_text", height=180,
                           placeholder="Dán nội dung cần phân tích tại đây...")
    mode = st.radio("Phương pháp phân tích", ["Tự động (Gemini nếu đã cấu hình)", "Chỉ dùng bộ quy tắc"], horizontal=True)
    if st.button("🌿 Phân tích nội dung", type="primary", use_container_width=True):
        if not content.strip():
            st.warning("Em hãy nhập nội dung trước nhé.")
        else:
            rules = rule_analysis(content)
            ai_text, ai_error = (None, None)
            if mode.startswith("Tự động"):
                ai_text, ai_error = gemini_analysis(content)
            result = {"content": content, "rules": rules, "ai_text": ai_text,
                      "ai_error": ai_error, "time": datetime.now().strftime("%d/%m/%Y %H:%M")}
            st.session_state.last_analysis = result
            st.session_state.history.insert(0, result)
            log_activity("Phân tích thông tin", rules["level"], rules["score"])
    result = st.session_state.last_analysis
    if result:
        rules = result["rules"]
        st.markdown("---")
        st.markdown("### 📌 Kết quả sàng lọc")
        x, y, z = st.columns(3)
        x.metric("Điểm tín hiệu", f'{rules["score"]}/100')
        y.metric("Số nhóm dấu hiệu", len(rules["findings"]))
        z.metric("Số từ", rules["word_count"])
        st.progress(rules["score"] / 100)
        st.write(f"**Nhận xét:** {rules['level']}")
        if rules["findings"]:
            for item in rules["findings"]:
                st.markdown(f'**{item["category"]}**')
                st.write("Cụm từ được nhận diện: " + ", ".join(item["matched"]))
        else:
            st.success("Chưa tìm thấy cụm từ thuộc các nhóm quy tắc hiện có.")
        if rules["urgency"]:
            st.warning("Dấu hiệu thúc giục: " + ", ".join(rules["urgency"]))
        st.warning("Điểm tín hiệu là chỉ số sàng lọc minh họa, KHÔNG phải xác suất tin giả hay kết luận đúng/sai.")
        if result["ai_text"]:
            st.markdown("### 🤖 Nhận xét hỗ trợ từ Gemini")
            st.markdown(result["ai_text"])
        elif result["ai_error"]:
            st.caption(result["ai_error"])
        title, message = adaptive_message(rules["score"])
        st.markdown("### 🧭 Gợi ý hành động")
        st.subheader(title)
        st.write(message)
        st.markdown("**Ba câu hỏi nên tự đặt ra:**")
        st.markdown("- Ai là người đăng đầu tiên và có xác định được nguồn không?\n- Có nguồn độc lập đáng tin cậy xác nhận không?\n- Ngày đăng, hình ảnh và bối cảnh có phù hợp không?")

# ---------------------- SOCIAL SIMULATOR -----------------------
elif page == "🧪 Mô phỏng mạng xã hội":
    hero("SAFE PRACTICE SPACE", "Mạng xã hội mô phỏng", "Thử đưa ra quyết định trong các tình huống giả định. Đây không phải bài đăng hoặc tài khoản thật.")
    scenarios = {
        "📩 Tin nhắn trúng thưởng": {
            "text": "Chúc mừng bạn đã trúng quà! Hãy gửi mã OTP và thông tin tài khoản ngay để nhận thưởng trong 5 phút.",
            "question": "Em nên làm gì?",
            "options": ["Gửi mã OTP ngay để không mất quà", "Không cung cấp mã; kiểm tra qua kênh chính thức", "Chuyển tiếp tin nhắn cho tất cả bạn bè"],
            "answer": 1,
            "why": "Mã OTP và thông tin tài khoản là dữ liệu bảo mật. Không chia sẻ chúng; hãy tự kiểm tra qua kênh chính thức."
        },
        "📰 Tin đồn nghỉ học": {
            "text": "Một tài khoản không rõ danh tính đăng: 'Nghe nói toàn trường được nghỉ tuần sau, chia sẻ ngay nhé!'",
            "question": "Bước nào phù hợp nhất?",
            "options": ["Chia sẻ ngay cho lớp", "Tin vì nhiều người bình luận", "Kiểm tra thông báo từ nhà trường"],
            "answer": 2,
            "why": "Thông tin lịch học cần được xác nhận từ kênh chính thức của nhà trường."
        },
        "🖼️ Hình ảnh gây tranh cãi": {
            "text": "Một bức ảnh được đăng lại với chú thích gây sốc nhưng không có ngày, địa điểm hoặc đường dẫn gốc.",
            "question": "Em nên kiểm tra điều gì?",
            "options": ["Tìm ảnh gốc, thời điểm và bối cảnh", "Chỉ đọc phần bình luận", "Chia sẻ vì ảnh trông chân thực"],
            "answer": 0,
            "why": "Hình ảnh có thể bị dùng sai bối cảnh. Cần tìm nguồn gốc và đối chiếu thông tin."
        },
        "🎁 Đường link nhận quà": {
            "text": "Bạn được mời bấm vào đường link lạ và đăng nhập để nhận phần quà miễn phí.",
            "question": "Lựa chọn an toàn là gì?",
            "options": ["Đăng nhập ngay", "Không nhập thông tin; tự truy cập trang chính thức để kiểm tra", "Gửi link cho bạn bè thử trước"],
            "answer": 1,
            "why": "Không nhập thông tin đăng nhập qua đường link không rõ nguồn. Tự mở ứng dụng hoặc trang chính thức."
        }
    }
    chosen = st.selectbox("Chọn tình huống", list(scenarios.keys()))
    item = scenarios[chosen]
    st.markdown(f'<div class="section-card"><span class="pill">TÌNH HUỐNG GIẢ LẬP</span><h3>{chosen}</h3><p>{item["text"]}</p></div>', unsafe_allow_html=True)
    st.markdown(f"**{item['question']}**")
    answer = st.radio("Chọn một phương án", item["options"], key="scenario_" + chosen)
    if st.button("Kiểm tra lựa chọn", type="primary"):
        idx = item["options"].index(answer)
        correct = idx == item["answer"]
        st.session_state.scenario_answers.append({"Tình huống": chosen, "Kết quả": "Đúng" if correct else "Cần xem lại"})
        log_activity("Làm tình huống", chosen, 100 if correct else 0)
        if correct:
            st.success("Chính xác! " + item["why"])
        else:
            st.warning("Em thử suy nghĩ lại nhé. " + item["why"])
    st.caption("Các tình huống chỉ nhằm rèn kỹ năng nhận diện và lựa chọn an toàn, không thu thập thông tin đăng nhập.")

# ---------------------- VERIFICATION ROOM ----------------------
elif page == "🧭 Phòng kiểm chứng":
    hero("VERIFY • DON'T AMPLIFY", "Phòng kiểm chứng thông tin", "Một quy trình thực hành để chuyển từ cảm giác sang kiểm tra nguồn và bằng chứng.")
    steps = [
        ("01", "Xác định tuyên bố", "Thông tin chính xác nào đang được khẳng định?"),
        ("02", "Tìm nguồn ban đầu", "Ai đăng đầu tiên? Có thông báo hoặc tài liệu gốc không?"),
        ("03", "Đối chiếu nguồn", "Kiểm tra nguồn chính thức và nguồn độc lập đáng tin."),
        ("04", "Kiểm tra bối cảnh", "Xem ngày đăng, địa điểm, hình ảnh và nội dung có bị cắt ghép không."),
        ("05", "Quyết định thận trọng", "Chỉ chia sẻ khi đủ căn cứ; nếu chưa rõ, đừng lan truyền.")
    ]
    for num, title, desc in steps:
        with st.container(border=True):
            st.markdown(f"**{num} · {title}**")
            st.caption(desc)
    st.markdown("### ✍️ Phiếu thực hành")
    with st.form("verification_form"):
        claim = st.text_input("Tuyên bố cần kiểm tra", placeholder="Ví dụ: Trường sẽ nghỉ học vào ngày mai")
        source = st.text_input("Nguồn ban đầu hoặc đơn vị phát hành")
        evidence = st.text_area("Bằng chứng và nguồn đối chiếu", height=100)
        checks = [
            "Đã tìm nguồn đăng ban đầu",
            "Đã kiểm tra tác giả hoặc đơn vị phát hành",
            "Đã đối chiếu với nguồn độc lập đáng tin",
            "Đã kiểm tra ngày đăng và bối cảnh",
            "Đã xem xét bằng chứng thay vì chỉ đọc tiêu đề"
        ]
        selected = [st.checkbox(x, key="check_" + str(i)) for i, x in enumerate(checks)]
        submitted = st.form_submit_button("Ghi nhận phiếu thực hành", use_container_width=True)
    if submitted:
        if not claim.strip():
            st.warning("Hãy nhập tuyên bố cần kiểm tra.")
        else:
            count = sum(selected)
            log_activity("Thực hành kiểm chứng", f"{claim[:120]} · {count}/5 bước", count * 20)
            st.success(f"Đã ghi nhận {count}/5 bước trong phiên hiện tại.")
    st.caption("Phiếu chỉ lưu trong phiên đang mở. Không nhập dữ liệu cá nhân hoặc thông tin nhạy cảm.")

# ---------------------- ADAPTIVE FEEDBACK ----------------------
elif page == "💬 Phản hồi thích ứng":
    hero("ADAPTIVE LEARNING", "Phản hồi thích ứng", "Lời nhắc và câu hỏi thay đổi theo dấu hiệu trong nội dung đã phân tích.")
    if st.session_state.last_analysis:
        rules = st.session_state.last_analysis["rules"]
        title, message = adaptive_message(rules["score"])
        st.subheader(title)
        st.write(message)
        questions = [
            "Ai là nguồn đăng đầu tiên? Có thể kiểm tra danh tính hoặc đơn vị phát hành không?",
            "Có nguồn độc lập đáng tin cậy xác nhận thông tin không?",
            "Bài đăng có tạo áp lực khiến người đọc sợ hãi hoặc vội vàng không?",
            "Em cần thêm bằng chứng nào trước khi đưa ra kết luận?"
        ]
        st.markdown("### 🌱 Câu hỏi gợi mở")
        for i, q in enumerate(questions, 1):
            st.markdown(f"**Câu {i}.** {q}")
        reflection = st.text_area("Em sẽ làm gì trước khi chia sẻ bài đăng?", height=120, key="reflection")
        if st.button("Ghi nhận suy ngẫm", type="primary"):
            if reflection.strip():
                log_activity("Suy ngẫm", reflection, rules["score"])
                st.success("Đã ghi nhận câu trả lời trong phiên này.")
            else:
                st.warning("Em hãy viết câu trả lời trước nhé.")
    else:
        st.info("Hãy phân tích một nội dung trước để nhận phản hồi phù hợp.")
        st.write("Mục tiêu của phản hồi thích ứng là giúp người học dừng lại, tự đặt câu hỏi và tìm bằng chứng.")

# ------------------------- SURVEY ------------------------------
elif page == "📝 Khảo sát nghiên cứu":
    hero("STUDENT RESEARCH", "Khảo sát kiến thức xác thực thông tin", "Bài đánh giá ngắn trước và sau khi trải nghiệm ứng dụng.")
    st.warning("Bộ câu hỏi là bản minh họa phục vụ thử nghiệm, chưa được chuẩn hóa khoa học. Khi khảo sát học sinh, cần có sự đồng ý phù hợp và bảo vệ quyền riêng tư.")
    questions = [
        ("Một bài đăng yêu cầu chia sẻ ngay nhưng không dẫn nguồn. Em nên:", ["Chia sẻ ngay", "Kiểm tra nguồn và bằng chứng trước", "Tin vì nhiều người chia sẻ"], 1),
        ("Công cụ không tìm thấy dấu hiệu đáng nghi. Điều đó có nghĩa:", ["Thông tin chắc chắn đúng", "Thông tin chắc chắn sai", "Chưa đủ căn cứ để kết luận"], 2),
        ("Nguồn nào nên ưu tiên khi kiểm tra thông báo của trường?", ["Tài khoản không rõ danh tính", "Thông báo chính thức của nhà trường", "Bình luận chưa xác minh"], 1),
        ("Khi hai nguồn đưa thông tin trái ngược, em nên:", ["Chọn tiêu đề hấp dẫn hơn", "So sánh nguồn gốc, bằng chứng và thời điểm", "Chia sẻ cả hai ngay"], 1),
        ("Ảnh chụp màn hình có thể thiếu ngữ cảnh không?", ["Có, cần tìm bản gốc và ngữ cảnh", "Không, ảnh chụp luôn đầy đủ", "Không cần kiểm tra"], 0)
    ]
    mode = st.radio("Lần đánh giá", ["Trước khi sử dụng", "Sau khi sử dụng"], horizontal=True)
    with st.form("survey_form"):
        answers = []
        for i, (question, options, correct) in enumerate(questions):
            answers.append(st.radio(f"Câu {i+1}. {question}", options, key=f"survey_{mode}_{i}"))
        submit = st.form_submit_button("Chấm điểm", use_container_width=True)
    if submit:
        score = sum(answers[i] == questions[i][1][questions[i][2]] for i in range(len(questions)))
        percent = round(score / len(questions) * 100)
        if mode == "Trước khi sử dụng":
            st.session_state.survey_pre = percent
        else:
            st.session_state.survey_post = percent
        log_activity("Khảo sát", mode, percent)
        st.success(f"Kết quả: {score}/{len(questions)} câu đúng ({percent}%).")
    p, q, r = st.columns(3)
    p.metric("Trước sử dụng", "Chưa có" if st.session_state.survey_pre is None else f"{st.session_state.survey_pre}%")
    q.metric("Sau sử dụng", "Chưa có" if st.session_state.survey_post is None else f"{st.session_state.survey_post}%")
    if st.session_state.survey_pre is not None and st.session_state.survey_post is not None:
        r.metric("Chênh lệch", f"{st.session_state.survey_post - st.session_state.survey_pre:+d} điểm %")
    else:
        r.metric("Chênh lệch", "Chưa đủ dữ liệu")

# --------------------------- STATS ------------------------------
elif page == "📊 Thống kê":
    hero("RESEARCH DASHBOARD", "Thống kê hoạt động", "Tổng hợp hoạt động trong phiên hiện tại và xuất dữ liệu để phục vụ phân tích.")
    total = len(st.session_state.activities)
    analyses = len(st.session_state.history)
    scenarios_done = len(st.session_state.scenario_answers)
    a, b, c = st.columns(3)
    a.metric("Hoạt động", total)
    b.metric("Lượt phân tích", analyses)
    c.metric("Tình huống đã làm", scenarios_done)
    st.markdown("### 📈 Nhật ký hoạt động")
    if st.session_state.activities:
        df = pd.DataFrame(st.session_state.activities)
        st.dataframe(df, use_container_width=True, hide_index=True)
        csv_data = df.to_csv(index=False).encode("utf-8-sig")
        st.download_button("⬇️ Tải dữ liệu hoạt động CSV", csv_data, "social_sandbox_activities.csv", "text/csv")
    else:
        st.info("Chưa có hoạt động. Hãy thử phân tích nội dung hoặc làm tình huống.")
    st.markdown("### 🧪 Kết quả tình huống mô phỏng")
    if st.session_state.scenario_answers:
        st.dataframe(pd.DataFrame(st.session_state.scenario_answers), use_container_width=True, hide_index=True)
    else:
        st.caption("Chưa có kết quả tình huống.")
    st.markdown("### 🗂️ Lịch sử phân tích")
    if st.session_state.history:
        history_rows = [{
            "Thời gian": x["time"], "Điểm tín hiệu": x["rules"]["score"],
            "Mức nhận xét": x["rules"]["level"], "Nội dung (rút gọn)": x["content"][:160]
        } for x in st.session_state.history]
        st.dataframe(pd.DataFrame(history_rows), use_container_width=True, hide_index=True)
    else:
        st.caption("Chưa có lịch sử phân tích.")
    st.caption("Dữ liệu hiện được giữ trong phiên Streamlit đang mở; tải CSV để lưu. Chưa có cơ sở dữ liệu dùng chung giữa nhiều người.")

# ---------------------------- ABOUT ----------------------------
elif page == "🌿 Giới thiệu đề tài":
    hero("ABOUT THE PROJECT", "Giới thiệu Social Sandbox AI", "Nguyên mẫu giáo dục hỗ trợ học sinh rèn luyện kỹ năng xác thực thông tin số.")
    st.markdown("### 🎓 Tên đề tài")
    st.markdown("*Nghiên cứu hành vi xác thực thông tin số của học sinh trung học và xây dựng hệ thống can thiệp thích ứng ứng dụng trí tuệ nhân tạo.*")
    st.markdown("### 🎯 Mục tiêu nghiên cứu")
    st.markdown("- Tìm hiểu cách học sinh đánh giá thông tin trên môi trường số.\n- Hỗ trợ nhận diện dấu hiệu đáng ngờ trong bài đăng và tin nhắn.\n- Khuyến khích kiểm tra nguồn trước khi chia sẻ.\n- Xây dựng tình huống mô phỏng và phản hồi thích ứng.")
    st.markdown("### 🧠 Công nghệ sử dụng")
    x, y = st.columns(2)
    with x:
        st.markdown('<div class="section-card"><h3>🐍 Python + Streamlit</h3><p>Xây dựng giao diện web, biểu mẫu khảo sát, mô phỏng và thống kê.</p></div>', unsafe_allow_html=True)
    with y:
        st.markdown('<div class="section-card"><h3>🤖 Gemini API (tùy chọn)</h3><p>Hỗ trợ phân tích ngôn ngữ và gợi ý kiểm chứng. Kết quả có thể sai và cần được đánh giá.</p></div>', unsafe_allow_html=True)
    st.markdown("### 🔒 Quyền riêng tư và giới hạn")
    st.markdown("- Ứng dụng không tự truy cập tài khoản mạng xã hội.\n- Ứng dụng không tự xác minh nguồn tin bên ngoài.\n- Không khóa nút chia sẻ trên nền tảng khác.\n- Dữ liệu hoạt động chỉ lưu trong phiên hiện tại và có thể tải CSV.\n- Không nhập thông tin cá nhân, mật khẩu hoặc mã OTP.")
    st.markdown("### 🌱 Hướng phát triển")
    st.markdown("- Đánh giá độ chính xác và giới hạn của mô hình AI.\n- Bổ sung lưu trữ bền vững có kiểm soát truy cập.\n- Phát triển thêm tình huống về deepfake và lừa đảo số.\n- Kiểm thử khả năng giải thích, thiên lệch và trải nghiệm người dùng.")

st.markdown("""
<div class="footer">
🌿 <b>Social Sandbox AI</b> · Leaf Green Edition · Bản thử nghiệm giáo dục v2.0<br>
Pause • Verify • Think • Share responsibly · Công cụ hỗ trợ học tập, không phải hệ thống xác minh sự thật.
</div>
""", unsafe_allow_html=True)
