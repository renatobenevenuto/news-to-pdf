import streamlit as st
from newspaper import Article, Config
from fpdf import FPDF
from datetime import datetime
import re
import nltk
from deep_translator import GoogleTranslator
import base64

# --- CONFIGURAÇÃO NLTK ---
def setup_nltk():
    recursos = ['punkt', 'punkt_tab', 'stopwords']
    for r in recursos:
        try:
            nltk.download(r, quiet=True)
        except Exception:
            pass

setup_nltk()

st.set_page_config(page_title="News2PDF Pro", page_icon="📑", layout="wide")

class PDF_Gerador(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Gerado via News2PDF Pro', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def limpar_nome_arquivo(titulo):
    nome = re.sub(r'[\\/*?:"<>|]', "", titulo)
    return nome[:80].strip()

def tratar_texto_pdf(texto):
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def traduzir_conteudo(texto):
    if not texto: return ""
    translator = GoogleTranslator(source='auto', target='pt')
    passos = 4000
    blocos = [texto[i:i+passos] for i in range(0, len(texto), passos)]
    try:
        return " ".join([translator.translate(b) for b in blocos])
    except:
        return texto

def exibir_pdf(pdf_bytes):
    """Gera um frame HTML compatível com Chromium para visualizar o PDF."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    # Usar <embed> em vez de <iframe> aumenta a compatibilidade com Edge e Chrome
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700" type="application/pdf">'
    st.markdown("### 📖 Visualização Prévia")
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- INTERFACE ---
st.title("📑 News2PDF Pro: Extrator & Tradutor")

with st.sidebar:
    st.header("Opções")
    traduzir = st.checkbox("Traduzir para Português", value=True)

url = st.text_input("Link da notícia:", placeholder="Cole a URL aqui...")

if st.button("🚀 Processar"):
    if url:
        try:
            with st.spinner("Extraindo e processando..."):
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0'
                artigo = Article(url, config=config)
                artigo.download()
                artigo.parse()
                artigo.nlp()
                
                titulo, resumo, corpo = artigo.title, artigo.summary, artigo.text

                if traduzir:
                    titulo = traduzir_conteudo(titulo)
                    resumo = traduzir_conteudo(resumo)
                    corpo = traduzir_conteudo(corpo)

                # Geração do PDF
                pdf = PDF_Gerador()
                pdf.add_page()
                pdf.set_font('helvetica', 'B', 16)
                pdf.multi_cell(0, 10, tratar_texto_pdf(titulo))
                pdf.ln(10)

                pdf.set_font('helvetica', 'B', 12)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 10, "RESUMO EXECUTIVO", 0, 1, 'L', fill=True)
                pdf.set_font('helvetica', 'I', 10)
                pdf.multi_cell(0, 7, tratar_texto_pdf(resumo))
                pdf.ln(10)

                pdf.set_font('helvetica', 'B', 12)
                pdf.cell(0, 10, "CONTEÚDO COMPLETO", 0, 1, 'L')
                pdf.set_font('helvetica', '', 11)
                pdf.multi_cell(0, 8, tratar_texto_pdf(corpo))

                pdf_bytes = bytes(pdf.output()) 
                
                # Visualização e Download
                exibir_pdf(pdf_bytes)
                
                nome_arq = f"{datetime.now().strftime('%Y%m%d')}_{limpar_nome_arquivo(titulo)}.pdf"
                st.download_button("📥 Baixar PDF", data=pdf_bytes, file_name=nome_arq, mime="application/pdf")

        except Exception as e:
            st.error(f"Erro: {e}")
