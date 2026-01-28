# news-to-pdf
transforma noticias de sites em pdf para serem lidos

# 📄 News2PDF: Extrator de Notícias Limpas

Um conversor inteligente que extrai o conteúdo principal de portais de notícias, remove anúncios, pop-ups e poluição visual, gerando um documento PDF organizado e pronto para leitura.

## 🚀 Funcionalidades
- **Remoção de Paywalls Suaves:** Utiliza bibliotecas de extração que ignoram scripts de bloqueio visual.
- **Formatação Automática:** Gera PDFs com título, data e corpo de texto limpo.
- **Organização Cronológica:** Nomeia os arquivos automaticamente no formato `YYYYMMDD_Titulo.pdf`.
- **Interface Web:** Simples e intuitiva construída com Streamlit.

## 🛠️ Tecnologias Utilizadas
- **Python 3.x**
- **Streamlit**: Para a interface web.
- **Newspaper3k**: Para extração de conteúdo e Processamento de Linguagem Natural (NLP) básico.
- **FPDF2**: Para geração de documentos PDF.

## 💻 Como rodar localmente
Se você quiser rodar na sua própria máquina (com VS Code ou Anaconda):

1. Clone o repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_REPOSITORIO.git)

2. Instale as dependências:

Bash
pip install -r requirements.txt

3. Execute a aplicação:

Bash
streamlit run app.py

🌐 Deploy (Como colocar no ar)
Esta aplicação foi projetada para ser hospedada gratuitamente no Streamlit Cloud:

Suba os arquivos app.py e requirements.txt para o seu GitHub.

Acesse share.streamlit.io.

Conecte seu repositório e clique em Deploy.

Desenvolvido como projeto de automação e ciência de dados.
