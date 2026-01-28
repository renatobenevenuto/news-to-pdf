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

# --- CLASSE PDF CUSTOMIZADA ---
class PDF_Gerador(FPDF):
    def __init__(self, source_url):
        super().__init__()
        self.source_url = source_url

    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(100, 100, 100)
        # Título com seu nome
        self.cell(0, 5, 'Gerado via News2PDF Pro de Renato Benevenuto', 0, 1, 'R')
        # Linha com a URL de origem
        self.set_font('helvetica', 'I', 7)
        url_cortada = (self.source_url[:90] + '..') if len(self.source_url) > 90 else self.source_url
        self.cell(0, 5, f'Fonte: {url_cortada}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

# --- FUNÇÕES DE PROCESSAMENTO ---
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
    """Renderiza o PDF na tela. Caso o navegador bloqueie, exibe um aviso amigável."""
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf" style="border: none;"></iframe>'
    st.markdown("### 📖 Visualização Prévia")
    st.markdown("---")
    st.markdown(pdf_display, unsafe_allow_html=True)
    st.info("💡 Se a visualização acima estiver em branco, use o botão de download abaixo para ler o arquivo.")

# --- INTERFACE ---
st.title("📑 News2PDF Pro")
st.markdown("Extração inteligente de notícias e conversão para PDF com tradução e resumo.")

with st.sidebar:
    st.header("Preferências")
    traduzir = st.checkbox("Traduzir para Português", value=True)

url_input = st.text_input("Cole a URL da notícia aqui:", placeholder="https://...")

if st.button("🚀 Processar Notícia"):
    if url_input:
        try:
            with st.spinner("Extraindo e formatando conteúdo..."):
                # 1. Extração
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0'
                artigo = Article(url_input, config=config)
                artigo.download()
                artigo.parse()
                artigo.nlp()
                
                titulo, resumo, corpo = artigo.title, artigo.summary, artigo.text

                # 2. Tradução
                if traduzir:
                    titulo = traduzir_conteudo(titulo)
                    resumo = traduzir_conteudo(resumo)
                    corpo = traduzir_conteudo(corpo)

                # 3. Geração do PDF
                pdf = PDF_Gerador(source_url=url_input)
                pdf.add_page()
                
                # Título Principal
                pdf.set_font('helvetica', 'B', 16)
                pdf.multi_cell(0, 10, tratar_texto_pdf(titulo))
                pdf.ln(5)
                
                # Seção de Resumo
                pdf.set_font('helvetica', 'B', 12)
                pdf.set_fill_color(245, 245, 245)
                pdf.cell(0, 10, "RESUMO EXECUTIVO (IA)", 0, 1, 'L', fill=True)
                pdf.set_font('helvetica', 'I', 10)
                pdf.multi_cell(0, 7, tratar_texto_pdf(resumo))
                pdf.ln(10)

                # Seção de Conteúdo
                pdf.set_font('helvetica', 'B', 12)
                pdf.cell(0, 10, "CONTEÚDO COMPLETO", 0, 1, 'L')
                pdf.set_font('helvetica', '', 11)
                pdf.multi_cell(0, 8, tratar_texto_pdf(corpo))

                # Conversão Final
                pdf_bytes = bytes(pdf.output()) 
                
                # 4. Saída
                exibir_pdf(pdf_bytes)
                
                nome_arq = f"{datetime.now().strftime('%Y%m%d')}_{limpar_nome_arquivo(titulo)}.pdf"
                st.download_button(
                    label="📥 Baixar Documento PDF",
                    data=pdf_bytes,
                    file_name=nome_arq,
                    mime="application/pdf"
                )

        except Exception as e:
            st.error(f"Ocorreu um erro no processamento: {e}")
    else:
        st.warning("Por favor, insira um link.")
