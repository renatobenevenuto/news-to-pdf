import streamlit as st
from newspaper import Article, Config
from fpdf import FPDF
from datetime import datetime
import re
import nltk
from deep_translator import GoogleTranslator
import requests
from io import BytesIO

# --- SETUP NLTK ---
def setup_nltk():
    for r in ['punkt', 'punkt_tab', 'stopwords']:
        try: nltk.download(r, quiet=True)
        except: pass
setup_nltk()

st.set_page_config(page_title="News2PDF Pro", page_icon="📑", layout="wide")

class PDF_Gerador(FPDF):
    def __init__(self, source_url):
        super().__init__()
        self.source_url = source_url

    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, 'Gerado via News2PDF Pro de Renato Benevenuto', 0, 1, 'R')
        self.set_font('helvetica', 'I', 7)
        url_link = (self.source_url[:80] + '..') if len(self.source_url) > 80 else self.source_url
        self.cell(0, 5, f'Fonte: {url_link}', 0, 1, 'R')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def limpar_nome_arquivo(titulo):
    return re.sub(r'[\\/*?:"<>|]', "", titulo)[:80].strip()

def tratar_texto(texto):
    return texto.encode('latin-1', 'ignore').decode('latin-1')

# --- INTERFACE ---
st.title("📑 News2PDF Pro")
st.markdown("Extração de notícias com **Imagens**, **Tradução** e **Resumo**.")

with st.sidebar:
    st.header("Configurações")
    traduzir = st.checkbox("Traduzir para Português", value=True)

url_input = st.text_input("Cole a URL da notícia:")

if st.button("🚀 Processar Notícia"):
    if url_input:
        try:
            with st.spinner("Extraindo dados e imagens..."):
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0'
                artigo = Article(url_input, config=config)
                artigo.download()
                artigo.parse()
                artigo.nlp()
                
                titulo, resumo, corpo = artigo.title, artigo.summary, artigo.text
                img_url = artigo.top_image

                if traduzir:
                    translator = GoogleTranslator(source='auto', target='pt')
                    titulo = translator.translate(titulo)
                    resumo = " ".join([translator.translate(b) for b in [resumo[i:i+4000] for i in range(0, len(resumo), 4000)]])
                    corpo = " ".join([translator.translate(b) for b in [corpo[i:i+4000] for i in range(0, len(corpo), 4000)]])

                # --- EXIBIÇÃO NA TELA ---
                st.subheader(f"📖 {titulo}")
                if img_url:
                    st.image(img_url, use_container_width=True)
                
                with st.expander("🔍 Ver Resumo Executivo"):
                    st.info(resumo)
                
                st.markdown("### 📝 Conteúdo Completo")
                st.write(corpo) # <--- ISSO GARANTE A EXIBIÇÃO NA TELA

                # --- GERAÇÃO DO PDF ---
                pdf = PDF_Gerador(source_url=url_input)
                pdf.add_page()
                pdf.set_font('helvetica', 'B', 18)
                pdf.multi_cell(0, 10, tratar_texto(titulo))
                pdf.ln(5)

                if img_url:
                    try:
                        response = requests.get(img_url, timeout=10)
                        img = BytesIO(response.content)
                        pdf.image(img, x=20, w=170)
                        pdf.ln(10)
                    except: pass

                pdf.set_font('helvetica', 'B', 12)
                pdf.set_fill_color(240, 240, 240)
                pdf.cell(0, 10, "RESUMO DA IA", 0, 1, 'L', fill=True)
                pdf.set_font('helvetica', 'I', 10)
                pdf.multi_cell(0, 7, tratar_texto(resumo))
                pdf.ln(10)

                pdf.set_font('helvetica', 'B', 12)
                pdf.cell(0, 10, "CONTEÚDO COMPLETO", 0, 1, 'L')
                pdf.set_font('helvetica', '', 11)
                pdf.multi_cell(0, 8, tratar_texto(corpo))

                pdf_bytes = bytes(pdf.output())
                nome_arq = f"{datetime.now().strftime('%Y%m%d')}_{limpar_nome_arquivo(titulo)}.pdf"
                
                st.download_button("📥 Baixar PDF com Imagens", data=pdf_bytes, file_name=nome_arq, mime="application/pdf")
                st.success("PDF gerado com sucesso!")

        except Exception as e:
            st.error(f"Erro: {e}")
