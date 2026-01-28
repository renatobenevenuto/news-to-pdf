import streamlit as st
from newspaper import Article, Config
from fpdf import FPDF
from datetime import datetime
import re

# Configuração da página do Streamlit
st.set_page_config(page_title="News2PDF - Extrator Limpo", page_icon="📄", layout="centered")

class PDF_Gerador(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Documento gerado automaticamente via News2PDF', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def limpar_nome_arquivo(titulo):
    """Remove caracteres proibidos em nomes de arquivos."""
    return re.sub(r'[\\/*?:"<>|]', "", titulo)[:80].strip()

def tratar_texto(texto):
    """Trata encoding para evitar erros no FPDF."""
    return texto.encode('latin-1', 'ignore').decode('latin-1')

def extrair_conteudo(url):
    """Extrai título e texto usando Newspaper3k."""
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    
    article = Article(url, config=config)
    article.download()
    article.parse()
    return article.title, article.text

# --- INTERFACE ---
st.title("📄 News2PDF")
st.subheader("Transforme notícias em PDFs limpos para leitura")

url_input = st.text_input("Cole a URL da notícia aqui:", placeholder="https://exemplo.com/noticia-importante")

if st.button("🚀 Gerar PDF"):
    if url_input:
        try:
            with st.spinner("Extraindo conteúdo e limpando anúncios..."):
                titulo, texto = extrair_conteudo(url_input)
                
                if len(texto) > 100:
                    # Preparação do PDF
                    pdf = PDF_Gerador()
                    pdf.add_page()
                    
                    # Título
                    pdf.set_font('helvetica', 'B', 16)
                    pdf.multi_cell(0, 10, tratar_texto(titulo))
                    pdf.ln(5)
                    
                    # Data e URL original
                    pdf.set_font('helvetica', 'I', 8)
                    pdf.cell(0, 5, f"Data da extração: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=1)
                    pdf.cell(0, 5, f"Fonte original: {url_input[:80]}...", ln=1)
                    pdf.ln(10)
                    
                    # Corpo
                    pdf.set_font('helvetica', '', 11)
                    pdf.multi_cell(0, 8, tratar_texto(texto))
                    
                    # Saída
                    pdf_output = pdf.output(dest='S')
                    
                    data_str = datetime.now().strftime("%Y%m%d")
                    nome_arquivo = f"{data_str}_{limpar_nome_arquivo(titulo)}.pdf"
                    
                    st.success("Tudo pronto!")
                    st.download_button(
                        label="📥 Baixar PDF Agora",
                        data=pdf_output,
                        file_name=nome_arquivo,
                        mime="application/pdf"
                    )
                else:
                    st.error("O conteúdo extraído parece ser muito curto ou bloqueado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, insira um link válido.")
