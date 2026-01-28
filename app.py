import streamlit as st
from newspaper import Article, Config
from fpdf import FPDF
from datetime import datetime
import re
import nltk

# Baixa os recursos necessários para o resumo (NLP)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

st.set_page_config(page_title="News2PDF + IA Summary", page_icon="📝", layout="centered")

class PDF_Gerador(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Gerado por News2PDF com Resumo Automático', 0, 1, 'C')

def tratar_texto(texto):
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def extrair_completo(url):
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0'
    article = Article(url, config=config)
    article.download()
    article.parse()
    # Ativa o processamento de linguagem natural
    article.nlp() 
    return article

# --- INTERFACE ---
st.title("📄 News2PDF + Resumo IA")
st.write("Extraia o conteúdo e receba um resumo automático dos pontos principais.")

url_input = st.text_input("Link da notícia:")

if st.button("🚀 Processar Notícia"):
    if url_input:
        try:
            with st.spinner("Analisando texto e gerando resumo..."):
                artigo = extrair_completo(url_input)
                
                if len(artigo.text) > 100:
                    # Exibe o Resumo na Tela
                    st.subheader("🤖 Resumo da IA")
                    st.info(artigo.summary)
                    
                    # Preparação do PDF
                    pdf = PDF_Gerador()
                    pdf.add_page()
                    
                    # Título
                    pdf.set_font('helvetica', 'B', 16)
                    pdf.multi_cell(0, 10, tratar_texto(artigo.title))
                    pdf.ln(5)
                    
                    # Seção de Resumo no PDF
                    pdf.set_font('helvetica', 'B', 12)
                    pdf.set_fill_color(240, 240, 240)
                    pdf.cell(0, 10, "RESUMO EXECUTIVO", 0, 1, 'L', fill=True)
                    pdf.set_font('helvetica', 'I', 10)
                    pdf.multi_cell(0, 7, tratar_texto(artigo.summary))
                    pdf.ln(10)
                    
                    # Conteúdo Completo
                    pdf.set_font('helvetica', 'B', 12)
                    pdf.cell(0, 10, "CONTEÚDO COMPLETO", 0, 1, 'L')
                    pdf.set_font('helvetica', '', 11)
                    pdf.multi_cell(0, 8, tratar_texto(artigo.text))
                    
                    pdf_output = pdf.output(dest='S')
                    nome_arq = f"{datetime.now().strftime('%Y%m%d')}_artigo_resumido.pdf"
                    
                    st.download_button(
                        label="📥 Baixar PDF com Resumo",
                        data=pdf_output,
                        file_name=nome_arq,
                        mime="application/pdf"
                    )
                else:
                    st.error("Conteúdo insuficiente para análise.")
        except Exception as e:
            st.error(f"Erro: {e}")
