import streamlit as st
import google.generativeai as genai
import PyPDF2
import io

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def analyze_paper(api_key, paper_text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    다음 논문을 분석하고 아래 항목들을 요약해주세요:
    1. 논문의 주요 목적
    2. 연구 방법론
    3. 주요 발견점
    4. 결론
    
    논문 내용:
    {paper_text}
    """
    
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("📚 논문 분석 챗봇")

# API 키 입력
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

# PDF 파일 업로드
uploaded_file = st.file_uploader("PDF 논문을 업로드하세요", type="pdf")

if uploaded_file and api_key:
    try:
        # PDF에서 텍스트 추출
        paper_text = extract_text_from_pdf(uploaded_file)
        
        if st.button("논문 분석하기"):
            with st.spinner("논문을 분석중입니다..."):
                analysis = analyze_paper(api_key, paper_text)
                st.markdown("### 분석 결과")
                st.write(analysis)
                
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.info("API 키를 입력하고 PDF 파일을 업로드해주세요.")
