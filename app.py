import streamlit as st
import fitz
from sentence_transformers import SentenceTransformer, util
import spacy

nlp = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')
SKILLS = ['python','java','javascript','react','sql','mongodb','machine learning','tensorflow','docker','git','aws','flask','html','css','pandas','numpy','django','power bi']

def extract(f):
    return ''.join(p.get_text() for p in fitz.open(stream=f.read(),filetype='pdf'))

def analyze(r,j):
    s=round(float(util.cos_sim(model.encode(r,convert_to_tensor=True),model.encode(j,convert_to_tensor=True))[0][0])*100,1)
    rs=set(x for x in SKILLS if x in r.lower())
    js=set(x for x in SKILLS if x in j.lower())
    return s,rs&js,js-rs,rs-js

def tips(missing,score):
    t=[]
    if missing: t.append('Add these skills: '+', '.join(list(missing)[:3]))
    if score<40: t.append('Resume needs major improvement for this job')
    elif score<70: t.append('Add more keywords from job description')
    else: t.append('Great match! Quantify your achievements')
    t.append('Add measurable results like: Improved X by Y%')
    t.append('Use action verbs: Built, Developed, Implemented')
    return t

st.set_page_config(page_title='AI Resume Screener', page_icon='📄', layout='wide')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #050510;
    color: #e0e0ff;
}

/* Animated background */
.stApp {
    background: #050510;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(99,0,255,0.15) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(0,200,255,0.1) 0%, transparent 50%);
    min-height: 100vh;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Hero header */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    animation: fadeSlideDown 0.8s ease forwards;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #a78bfa);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s linear infinite;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #7c7caa;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.05em;
}

/* Animated divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #6300ff, #00c8ff, #6300ff, transparent);
    margin: 1.5rem auto;
    max-width: 600px;
    animation: glow 2s ease-in-out infinite alternate;
}

/* Upload card */
.upload-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 16px;
    padding: 1.5rem;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s, box-shadow 0.3s;
    animation: fadeSlideUp 0.6s ease forwards;
}
.upload-card:hover {
    border-color: rgba(167,139,250,0.5);
    box-shadow: 0 0 30px rgba(99,0,255,0.15);
}

.card-label {
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.15em;
    color: #a78bfa;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

/* Score display */
.score-container {
    text-align: center;
    padding: 2.5rem 1rem;
    border-radius: 20px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease forwards;
}
.score-container::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 50% 0%, rgba(99,0,255,0.1), transparent 70%);
    pointer-events: none;
}
.score-number {
    font-size: 6rem;
    font-weight: 800;
    line-height: 1;
    font-family: 'Space Mono', monospace;
    animation: countUp 0.8s ease forwards;
}
.score-label {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 0.5rem;
    letter-spacing: 0.05em;
}
.score-bar-wrap {
    margin: 1.2rem auto 0;
    max-width: 300px;
    height: 6px;
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 1s ease;
    animation: barGrow 1s ease forwards;
}

/* Skill tags */
.skill-tag {
    display: inline-block;
    padding: 0.35rem 0.9rem;
    border-radius: 99px;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
    margin: 0.3rem 0.2rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    animation: popIn 0.4s ease forwards;
    opacity: 0;
}
.skill-match {
    background: rgba(52,211,153,0.15);
    border: 1px solid rgba(52,211,153,0.4);
    color: #34d399;
}
.skill-missing {
    background: rgba(251,113,133,0.15);
    border: 1px solid rgba(251,113,133,0.4);
    color: #fb7185;
}
.skill-bonus {
    background: rgba(56,189,248,0.15);
    border: 1px solid rgba(56,189,248,0.4);
    color: #38bdf8;
}

/* Section headers */
.section-title {
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7c7caa;
    margin-bottom: 0.8rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* Tip cards */
.tip-card {
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #a78bfa;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.7rem;
    font-size: 0.92rem;
    color: #c4c4e8;
    animation: slideInLeft 0.5s ease forwards;
    opacity: 0;
}

/* Analyze button */
.stButton > button {
    background: linear-gradient(135deg, #6300ff, #38bdf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 2rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(99,0,255,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,0,255,0.5) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1.5px dashed rgba(167,139,250,0.3) !important;
    border-radius: 12px !important;
    transition: border-color 0.3s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(167,139,250,0.6) !important;
}

/* Textarea */
textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    border-radius: 12px !important;
    color: #e0e0ff !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}
textarea:focus {
    border-color: rgba(167,139,250,0.6) !important;
    box-shadow: 0 0 20px rgba(99,0,255,0.15) !important;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: #a78bfa !important;
}

/* Keyframes */
@keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
@keyframes fadeSlideDown {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes popIn {
    0% { opacity: 0; transform: scale(0.7); }
    80% { transform: scale(1.05); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}
@keyframes glow {
    from { opacity: 0.4; }
    to { opacity: 1; }
}
@keyframes barGrow {
    from { width: 0%; }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero">
    <div class="hero-title">AI Resume Screener</div>
    <div class="hero-sub">// powered by sentence transformers + spacy</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# Input Section
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<div class="card-label">📤 Upload Resume</div>', unsafe_allow_html=True)
    pdf = st.file_uploader('', type=['pdf'], label_visibility='collapsed')
    if pdf:
        st.markdown(f'<div style="color:#34d399;font-family:Space Mono,monospace;font-size:0.8rem;margin-top:0.5rem">✓ {pdf.name} loaded</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card-label">📋 Job Description</div>', unsafe_allow_html=True)
    jd = st.text_area('', height=180, placeholder='Paste the job description here...', label_visibility='collapsed')

st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)

col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    analyze_btn = st.button('⚡ Analyze Resume', use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Analysis
if analyze_btn:
    if not pdf or not jd.strip():
        st.markdown("""
        <div style="text-align:center;padding:1rem;background:rgba(251,113,133,0.1);
        border:1px solid rgba(251,113,133,0.3);border-radius:12px;color:#fb7185;
        font-family:'Space Mono',monospace;font-size:0.85rem">
        ⚠ Please upload a resume and enter a job description
        </div>""", unsafe_allow_html=True)
    else:
        with st.spinner('🔍 Analyzing your resume...'):
            rt = extract(pdf)
            score, matched, missing, extra = analyze(rt, jd)

        # Score color
        if score >= 70:
            color = '#34d399'
            verdict = '🚀 Strong Match'
            bar_color = 'linear-gradient(90deg, #34d399, #059669)'
        elif score >= 45:
            color = '#fbbf24'
            verdict = '⚡ Average Match'
            bar_color = 'linear-gradient(90deg, #fbbf24, #d97706)'
        else:
            color = '#fb7185'
            verdict = '⚠ Weak Match'
            bar_color = 'linear-gradient(90deg, #fb7185, #e11d48)'

        # Score Card
        st.markdown(f"""
        <div class="score-container">
            <div class="score-number" style="color:{color}">{score}%</div>
            <div class="score-label" style="color:{color}">{verdict}</div>
            <div class="score-bar-wrap">
                <div class="score-bar-fill" style="width:{score}%;background:{bar_color}"></div>
            </div>
            <div style="margin-top:1rem;font-family:'Space Mono',monospace;font-size:0.75rem;color:#7c7caa">
                COMPATIBILITY SCORE
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

        # Skills Section
        r1, r2, r3 = st.columns(3, gap="medium")

        with r1:
            st.markdown('<div class="section-title">✅ Matched Skills</div>', unsafe_allow_html=True)
            if matched:
                tags = ''.join([f'<span class="skill-tag skill-match" style="animation-delay:{i*0.1}s">{x}</span>' for i, x in enumerate(matched)])
                st.markdown(f'<div>{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#7c7caa;font-size:0.85rem;font-family:Space Mono,monospace">No matches found</div>', unsafe_allow_html=True)

        with r2:
            st.markdown('<div class="section-title">❌ Missing Skills</div>', unsafe_allow_html=True)
            if missing:
                tags = ''.join([f'<span class="skill-tag skill-missing" style="animation-delay:{i*0.1}s">{x}</span>' for i, x in enumerate(missing)])
                st.markdown(f'<div>{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#7c7caa;font-size:0.85rem;font-family:Space Mono,monospace">No missing skills 🎉</div>', unsafe_allow_html=True)

        with r3:
            st.markdown('<div class="section-title">💎 Bonus Skills</div>', unsafe_allow_html=True)
            if extra:
                tags = ''.join([f'<span class="skill-tag skill-bonus" style="animation-delay:{i*0.1}s">{x}</span>' for i, x in enumerate(extra)])
                st.markdown(f'<div>{tags}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="color:#7c7caa;font-size:0.85rem;font-family:Space Mono,monospace">No extra skills</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

        # Tips Section
        st.markdown('<div class="section-title">🤖 AI Suggestions</div>', unsafe_allow_html=True)
        for i, t in enumerate(tips(missing, score)):
            st.markdown(f'<div class="tip-card" style="animation-delay:{i*0.15}s">👉 {t}</div>', unsafe_allow_html=True)

        st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;font-family:'Space Mono',monospace;font-size:0.7rem;color:#3a3a5c;padding:1rem">
            AI Resume Screener • Built with Streamlit + Sentence Transformers
        </div>
        """, unsafe_allow_html=True)
