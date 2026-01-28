# news-to-pdf
transforma noticias de sites em pdf para serem lidos

# 📑 News2PDF Pro

O **News2PDF Pro** é uma ferramenta de engenharia de dados e automação desenvolvida para transformar notícias poluídas da web em documentos PDF organizados, resumidos e traduzidos. Ideal para acadêmicos, professores e profissionais que buscam uma leitura focada e produtiva.

## 🚀 Funcionalidades
- **Extração Limpa:** Remove anúncios, barras laterais e pop-ups.
- **Resumo Inteligente:** Utiliza NLP (Natural Language Processing) para gerar um resumo executivo.
- **Tradução Automática:** Traduz notícias de qualquer idioma para o Português.
- **Organização Cronológica:** Nomenclatura automática de arquivos com data e título.
- **Visualização Integrada:** Leitura direta no navegador antes do download.

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Streamlit**: Interface web responsiva.
- **Newspaper3k**: Engine de extração e processamento de linguagem natural.
- **FPDF2**: Motor de geração de documentos PDF de alta fidelidade.
- **Deep Translator**: Tradução via Google Translate API.

## 📈 Jornada de Desenvolvimento (Stages)

O projeto evoluiu através de etapas de refinamento técnico:

1.  **Stage 1: Script de Extração:** Protótipo inicial focado apenas em extrair texto puro via terminal.
2.  **Stage 2: Interface Web:** Implementação da UI com Streamlit para facilitar o uso por terceiros.
3.  **Stage 3: Inteligência Artificial:** Integração do NLTK para geração de resumos automáticos e tradução de textos longos.
4.  **Stage 4: UX & Organização:** Adição de visualização prévia, cabeçalhos personalizados com metadados e sanitização de arquivos.
5.  **Stage 5: Estabilidade:** Correções de compatibilidade com navegadores Chromium (Bypass de erros binários e CSP).

## 📥 Como Rodar este Projeto
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install streamlit newspaper3k fpdf2 lxml_html_clean nltk deep-translator
3. Execute a aplicação:
streamlit run app.py
Desenvolvido por Renato Benevenuto.
