
# 📑 News2PDF Pro

**News2PDF Pro** é uma solução inteligente de curadoria de conteúdo que transforma URLs de notícias em documentos PDF limpos, traduzidos e enriquecidos com Inteligência Artificial. 

Desenvolvido por **Renato Benevenuto**, o projeto nasceu da necessidade de converter artigos poluídos por anúncios em materiais de leitura focada para fins acadêmicos e profissionais.

## 🌟 Funcionalidades Principais
- **Extração Inteligente:** Captura título, texto principal e a imagem de destaque da matéria.
- **Resumo Executivo (IA):** Gera um resumo automático dos pontos cruciais utilizando NLTK.
- **Tradução Global:** Converte automaticamente conteúdos estrangeiros para o Português.
- **Visualização Dinâmica:** Exibe uma prévia da notícia (texto e imagem) diretamente na interface.
- **PDF de Alta Qualidade:** Documentos formatados com cabeçalho personalizado e metadados de origem.

## 🛠️ Evolução do Projeto
O desenvolvimento seguiu um rigoroso processo de engenharia de software:
1. **MVP (Minimum Viable Product):** Script básico de extração via terminal.
2. **Integração UI:** Implementação da interface web com Streamlit.
3. **Camada de IA:** Adição de processamento de linguagem natural para resumos.
4. **Multimídia & Tradução:** Suporte a imagens e localização de idiomas.
5. **Estabilização:** Otimização para navegadores Chromium e correção de erros de memória binária.

## 📦 Instalação e Uso
1. Certifique-se de ter o Python 3.10+ instalado.
2. Instale as dependências:
   ```bash
   pip install streamlit newspaper3k fpdf2 lxml_html_clean nltk deep-translator requests

3. Execute a aplicação:

streamlit run app.py

## 🌐 Hospedagem
Este projeto está configurado para deploy contínuo no Streamlit Cloud, garantindo disponibilidade gratuita e atualizações automáticas via GitHub.

Focado em transformar ruído digital em conhecimento estruturado.
