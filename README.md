# 📝 Guruja MD Editor

Editor Markdown online com templates customizados para criação de apostilas e materiais de estudo.

## ✨ Funcionalidades

- **Editor Markdown** com preview ao vivo em tempo real
- **Template Bizus**: Caixas coloridas com emojis, subtítulos em itálico, tabelas estilizadas
- **Template Spoilers**: Caixas de questão individuais com gabarito e explicação
- **Salvamento automático** a cada 10 segundos
- **Gerenciador de documentos** — crie, edite e exclua documentos
- **Download** em `.md` e `.html` standalone
- **Interface dark** com identidade visual Guruja

## 🚀 Deploy no Streamlit Cloud (Gratuito)

### Passo 1: Crie uma conta
1. Acesse [share.streamlit.io](https://share.streamlit.io)
2. Clique em **"Sign up"** e faça login com sua conta Google ou GitHub

### Passo 2: Crie um repositório no GitHub
1. Acesse [github.com](https://github.com) e crie um novo repositório
2. Nomeie como `guruja-md-editor` (ou qualquer nome)
3. Faça upload dos 3 arquivos desta pasta:
   - `guruja_md_editor.py` (o app principal)
   - `requirements.txt` (dependências)
   - `README.md` (este arquivo)

### Passo 3: Conecte ao Streamlit Cloud
1. No [share.streamlit.io](https://share.streamlit.io), clique em **"New app"**
2. Selecione seu repositório GitHub
3. O Streamlit detecta automaticamente o arquivo `.py`
4. Clique em **"Deploy"**

Pronto! Seu app estará online em segundos com URL pública.

---

## 💻 Rodar Localmente

### Requisitos
- Python 3.8+
- pip

### Instalação

```bash
# 1. Clone ou baixe os arquivos
cd guruja-md-editor

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o app
streamlit run guruja_md_editor.py
```

O app abrirá automaticamente no navegador em `http://localhost:8501`

---

## 📁 Estrutura do Projeto

```
guruja-md-editor/
├── guruja_md_editor.py   # App principal (Streamlit)
├── requirements.txt      # Dependências Python
└── README.md            # Este arquivo
```

Os documentos são salvos automaticamente na pasta `./data/` (criada automaticamente).

---

## 🎨 Templates

### Template Bizus
Ideal para apostilas e resumos. Use emojis no início de parágrafos para criar caixas coloridas:
- 💡 Dica (amarelo)
- ✅ Regra (verde)
- ⚠️ Alerta (vermelho)
- ℹ️ Informação (azul)
- ⚖️ Base legal (laranja)
- 📝 Observação (roxo)

### Template Spoilers
Ideal para listas de exercícios. Cada questão começa com `**N.` e o sistema cria caixas automáticas com gabarito e explicação.

---

## 🛠️ Atalhos do Editor

| Atalho | Ação |
|---|---|
| **Ctrl+B** | Negrito |
| **Ctrl+I** | Itálico |
| **Ctrl+K** | Link |

---

## 📄 Licença

Uso livre para fins pessoais e educacionais.
