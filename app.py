import streamlit as st
from newspaper import Article, Config
from fpdf import FPDF
from datetime import datetime
import re
import nltk
from deep_translator import GoogleTranslator

# --- CORREÇÃO DO ERRO NLTK ---
def baixar_recursos_nltk():
    recursos = ['punkt', 'punkt_tab', 'stopwords']
    for r in recursos:
        try:
            nltk.download(r, quiet=True)
        except:
            pass

baixar_recursos_nltk()

st.set_page_config(page_title="News2PDF + IA Translator", page_icon="🌍", layout="centered")

class PDF_Gerador(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'News2PDF: Extração, Resumo e Tradução', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def limpar_nome_arquivo(titulo):
    return re.sub(r'[\\/*?:"<>|]', "", titulo)[:80].strip()

def tratar_texto(texto):
    """Garante que o texto seja compatível com a codificação do PDF."""
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def traduzir_texto(texto, destino='pt'):
    """Divide o texto em blocos para evitar limites de tradução."""
    translator = GoogleTranslator(source='auto', target=destino)
    # Limite seguro de 4500 caracteres por bloco para o Google
    passos = 4500
    blocos = [texto[i:i+passos] for i in range(0, len(texto), passos)]
    try:
        traduzido = [translator.translate(b) for b in blocos]
        return " ".join(traduzido)
    except:
        return texto # Retorna original se falhar

# --- INTERFACE ---
st.title("📄 News2PDF + Resumo & Tradução")
st.write("Extraia notícias de qualquer idioma e transforme em um PDF limpo em Português.")

url_input = st.text_input("Link da notícia:")
idioma_original = st.toggle("Traduzir conteúdo para Português?", value=True)

if st.button("🚀 Processar Notícia"):
    if url_input:
        try:
            with st.spinner("Extraindo e processando (isso pode levar um minuto para textos longos)..."):
                # Configuração e extração
                config = Config()
                config.browser_user_agent = 'Mozilla/5.0'
                artigo = Article(url_input, config=config)
                artigo.download()
                artigo.parse()
                artigo.nlp()
                
                titulo = artigo.title
                resumo = artigo.summary
                corpo = artigo.text

                # Tradução se solicitado
                if idioma_original:
                    st.write("🔄 Traduzindo conteúdo...")
                    titulo = traduzir_texto(titulo)
                    resumo = traduzir_texto(resumo)
                    corpo = traduzir_texto(corpo)

                if len(corpo) > 100:
                    # Mostra na tela
                    st.subheader(f"📖 {titulo}")
                    with st.expander("Ver Resumo da IA"):
                        st.info(resumo)
                    
                    # Gera PDF
                    pdf = PDF_Gerador()
                    pdf.add_page()
                    
                    pdf.set_font('helvetica', 'B', 16)
                    pdf.multi_cell(0, 10, tratar_texto(titulo))
                    pdf.ln(10)
                    
                    # Seção Resumo no PDF
                    pdf.set_font('helvetica', 'B', 12)
                    pdf.set_fill_color(230, 230, 230)
                    pdf.cell(0, 10, "RESUMO EXECUTIVO", 0, 1, 'L', fill=True)
                    pdf.set_font('helvetica', 'I', 10)
                    pdf.multi_cell(0, 7, tratar_texto(resumo))
                    pdf.ln(10)
                    
                    # Conteúdo
                    pdf.set_font('helvetica', 'B', 12)
                    pdf.cell(0, 10, "CONTEÚDO COMPLETO", 0, 1, 'L')
                    pdf.set_font('helvetica', '', 11)
                    pdf.multi_cell(0, 8, tratar_texto(corpo))
                    
                    pdf_output = pdf.output(dest='S')
                    data_str = datetime.now().strftime("%Y%m%d")
                    nome_arq = f"{data_str}_{limpar_nome_arquivo(titulo)}.pdf"
                    
                    st.download_button(
                        label="📥 Baixar PDF em Português",
                        data=pdf_output,
                        file_name=nome_arq,
                        mime="application/pdf"
                    )
                else:
                    st.error("Falha ao extrair o texto. O site pode estar bloqueando o acesso.")
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
