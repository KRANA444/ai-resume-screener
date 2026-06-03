import streamlit as st
import fitz
from sentence_transformers import SentenceTransformer, util
import spacy
nlp = spacy.load('en_core_web_sm')
model = SentenceTransformer('all-MiniLM-L6-v2')
SKILLS = ['python','java','javascript','react','sql','machine learning','tensorflow','docker','git','aws','flask','html','css','pandas','numpy']
def extract(f):
    return ''.join(p.get_text() for p in fitz.open(stream=f.read(),filetype='pdf'))
def analyze(r,j):
    s=round(float(util.cos_sim(model.encode(r,convert_to_tensor=True),model.encode(j,convert_to_tensor=True))[0][0])*100,1)
    rs=set(x for x in SKILLS if x in r.lower())
    js=set(x for x in SKILLS if x in j.lower())
    return s,rs&js,js-rs,rs-js
st.title('AI Resume Screener')
pdf=st.file_uploader('Resume Upload Karo',type=['pdf'])
jd=st.text_area('Job Description Paste Karo')
if st.button('Analyze'):
    if pdf and jd:
        score,matched,missing,extra=analyze(extract(pdf),jd)
        st.metric('Match Score',f'{score}%')
        c1,c2,c3=st.columns(3)
        with c1:
            st.write('Matched Skills')
            [st.success(x) for x in matched]
        with c2:
            st.write('Missing Skills')
            [st.error(x) for x in missing]
        with c3:
            st.write('Bonus Skills')
            [st.info(x) for x in extra]
