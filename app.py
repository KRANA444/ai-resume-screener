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
st.set_page_config(page_title='AI Resume Screener',page_icon='📄',layout='wide')
st.title('📄 AI Resume Screener')
st.markdown('---')
c1,c2=st.columns(2)
with c1:
    pdf=st.file_uploader('📤 Resume Upload Karo',type=['pdf'])
with c2:
    jd=st.text_area('📋 Job Description',height=200)
if st.button('Analyze',type='primary',use_container_width=True):
    if not pdf or not jd.strip():
        st.warning('Dono fields bharо!')
    else:
        with st.spinner('Analyzing...'):
            rt=extract(pdf)
            score,matched,missing,extra=analyze(rt,jd)
        color='#00C851' if score>=70 else '#FF8800' if score>=45 else '#ff4444'
        verdict='Strong Match!' if score>=70 else 'Average Match' if score>=45 else 'Weak Match'
        st.markdown(f'<div style="text-align:center;padding:20px;border-radius:10px;background:#1e1e2e"><h1 style="color:{color}">{score}%</h1><h3 style="color:white">{verdict}</h3></div>',unsafe_allow_html=True)
        st.markdown('---')
        a,b,c=st.columns(3)
        with a:
            st.markdown('### Matched')
            for x in matched: st.success(x)
        with b:
            st.markdown('### Missing')
            for x in missing: st.error(x)
        with c:
            st.markdown('### Bonus')
            for x in extra: st.info(x)
        st.markdown('---')
        st.markdown('### AI Suggestions')
        for t in tips(missing,score): st.warning('👉 '+t)
