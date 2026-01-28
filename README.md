📑 News2PDF Pro: Inteligência em Leitura
O News2PDF Pro é uma solução de Engenharia de Dados e NLP (Processamento de Linguagem Natural) desenvolvida para otimizar o consumo de informações técnicas e acadêmicas. A ferramenta extrai o conteúdo essencial de portais de notícias globais, eliminando distrações, traduzindo idiomas e gerando resumos executivos automáticos em documentos PDF de alta qualidade.

🌟 Proposta de Valor
Em um cenário de excesso de informação e interfaces poluídas por anúncios e paywalls, o News2PDF Pro atua como um filtro inteligente. Ele permite que pesquisadores, professores e estudantes foquem no que realmente importa: o conteúdo.

🚀 Etapas de Evolução (Development Stages)
A construção deste projeto seguiu um ciclo de desenvolvimento incremental, demonstrando um pensamento de engenharia estruturado:

Stage 1: Ingestão de Dados (Scraping): Implementação do motor de extração utilizando newspaper3k com cabeçalhos de navegador real para contornar bloqueios básicos.

Stage 2: Interface e Acessibilidade: Desenvolvimento da interface web com Streamlit, permitindo que o processamento de scripts complexos seja acessível via navegador.

Stage 3: Camada de Inteligência (NLP): Integração com o NLTK para análise semântica, identificando as sentenças mais relevantes para a criação de um resumo executivo automático.

Stage 4: Localização e Multimídia: Implementação de suporte a tradução via deep-translator e captura de imagens dinâmicas para enriquecer o documento final.

Stage 5: Estabilização de UX: Refinamento da saída binária para PDF (fpdf2) e correção de compatibilidade com navegadores Chromium (Edge/Chrome), resolvendo desafios de renderização de memória.

🛠️ Tecnologias e Bibliotecas
Python 3.10+: Linguagem base do pipeline.

Streamlit: Framework para a criação da interface web interativa.

Newspaper3k: Biblioteca líder para extração e curadoria de artigos web.

FPDF2: Motor de geração de PDFs que permite controle total sobre o layout e metadados.

NLTK (Natural Language Toolkit): Utilizado para a tokenização e análise estatística do texto.

Deep Translator: Integração com serviços de tradução global para suporte multi-idiomas.

📋 Funcionalidades
Remoção de Ruído: Extração apenas do título, imagem de destaque e texto principal.

Resumo por IA: Visualização imediata dos pontos-chave da matéria.

Tradução Automática: Conversão instantânea de qualquer fonte internacional para o Português.

PDF Assinado: Geração de arquivos formatados com a marca do autor e link para a fonte original.

Nomenclatura Organizada: Arquivos salvos automaticamente no padrão YYYYMMDD_Titulo_da_Materia.pdf.

⚙️ Instalação e Uso Local
Clone este repositório:

Bash
git clone https://github.com/renatobenevenuto/news2pdf-pro.git
Instale as dependências necessárias:

Bash
pip install streamlit newspaper3k fpdf2 lxml_html_clean nltk deep-translator requests
Execute a aplicação:

Bash
streamlit run app.py
🌐 Deploy
A aplicação está hospedada no Streamlit Cloud, integrada diretamente a este repositório para atualizações contínuas (CI/CD).

Desenvolvido por Renato Benevenuto Engenheiro Civil e entusiasta de Ciência de Dados, focado em transformar dados brutos em conhecimento estruturado.
