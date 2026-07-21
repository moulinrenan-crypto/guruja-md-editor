import streamlit as st
import time
import json
import os
from datetime import datetime
import re

# ══════════════════════════════════════════════════════
#  CONFIGURAÇÃO DA PÁGINA
# ══════════════════════════════════════════════════════
st.set_page_config(
    page_title="Guruja MD Editor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════
#  CSS CUSTOMIZADO — Dark Theme (idêntico ao original)
# ══════════════════════════════════════════════════════
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Nunito:wght@400;600;700;800&display=swap');

/* Reset e base */
.stApp {
    background: #0a0a0a !important;
}
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Header customizado */
.gj-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 46px;
    padding: 0 14px;
    background: #0f0f0f;
    border-bottom: 1px solid #222;
    gap: 10px;
    position: sticky;
    top: 0;
    z-index: 100;
}
.gj-header-left, .gj-header-right { display:flex; align-items:center; gap:8px; }

.gj-logo { font-size:17px; font-weight:800; letter-spacing:-0.5px; color:#d0d0d0; font-family:'Syne',sans-serif; }
.gj-logo span { color:#C4D600; }

.gj-filename-wrap { display:flex; align-items:center; gap:4px; }
.gj-filename {
    background: none;
    border: none;
    color: #d0d0d0;
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 4px 8px;
    border-radius: 5px;
    max-width: 220px;
}
.gj-filename:focus { outline: 1px solid #C4D600; background: #1c1c1c; }
.gj-filename-ext { font-size:12px; color: #555; font-weight:400; font-family:'Syne',sans-serif; }

.gj-badge {
    font-size:10px; font-weight:600; color:#555;
    background: #1c1c1c; padding:2px 7px; border-radius:20px;
    border: 1px solid #222; font-family:'Syne',sans-serif;
}

.gj-btn {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    cursor: pointer;
    border-radius: 5px;
    border: none;
    transition: opacity 0.15s, background 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    text-decoration: none;
}
.gj-btn-primary   { background:#C4D600; color:#000; padding:6px 14px; }
.gj-btn-primary:hover { opacity:.88; }
.gj-btn-ghost {
    background: none;
    border: 1px solid #222;
    color: #555;
    padding: 5px 11px;
}
.gj-btn-ghost:hover { border-color: #C4D600; color: #C4D600; }

.gj-save-status {
    font-size:11px; font-weight:600; min-width:80px; text-align:right;
    color: transparent; font-family:'Syne',sans-serif;
}

/* Toolbar */
.gj-toolbar {
    display: flex;
    align-items: center;
    height: 38px;
    padding: 0 8px;
    background: #141414;
    border-bottom: 1px solid #181818;
    gap: 1px;
    overflow-x: auto;
    flex-shrink: 0;
}
.gj-toolbar::-webkit-scrollbar { display:none; }

.gj-tbr-sep {
    width: 1px; height: 16px;
    background: #222;
    margin: 0 5px; flex-shrink:0;
}

.gj-tbr-btn {
    background: none;
    border: none;
    color: #555;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    cursor: pointer;
    padding: 4px 7px;
    border-radius: 4px;
    white-space: nowrap;
    transition: color 0.1s, background 0.1s;
    flex-shrink: 0;
}
.gj-tbr-btn:hover { color: #d0d0d0; background: #1c1c1c; }

/* Editor */
.gj-editor {
    background: #0d0d0d !important;
    color: #beccba !important;
    border: none !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13.5px !important;
    line-height: 1.85 !important;
    padding: 22px 26px !important;
    outline: none !important;
    caret-color: #C4D600 !important;
    tab-size: 2 !important;
    resize: none !important;
    width: 100% !important;
    min-height: calc(100vh - 140px) !important;
}
.gj-editor::placeholder { color: #333 !important; }
.gj-editor::selection { background: rgba(196,214,0,0.18) !important; }

/* Statusbar */
.gj-statusbar {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 4px 16px;
    background: #141414;
    border-top: 1px solid #181818;
    font-size: 10px;
    color: #333;
    font-family: 'JetBrains Mono', monospace;
}

/* Preview bar */
.gj-preview-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 38px;
    padding: 0 14px;
    background: #141414;
    border-bottom: 1px solid #181818;
}
.gj-preview-label {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #333;
    font-family:'Syne',sans-serif;
}

/* Template pills */
.gj-pill {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 13px;
    border-radius: 20px;
    border: 1px solid #222;
    background: none;
    color: #555;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s;
    margin-right: 5px;
}
.gj-pill:hover { border-color: #C4D600; color: #C4D600; }
.gj-pill.active { background: #C4D600; color: #000; border-color: #C4D600; }

/* Preview content — Bizus */
.gj-preview-bizus {
    font-family: 'Nunito', sans-serif;
    color: #212121;
    line-height: 1.6;
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 30px 60px;
    background: #fff;
    min-height: 100%;
}
.gj-preview-bizus h1 {
    color: #4A4A4A; font-size: 24pt; font-weight: 800; text-align: left;
    margin: 20px 0 10px; text-transform: uppercase;
    border-bottom: 6px solid #C4D600; display: inline-block; padding-bottom: 5px;
}
.gj-preview-bizus h2 {
    background: #C4D600; color: white; padding: 18px 28px;
    border-radius: 25px; font-size: 17pt; font-weight: 800;
    text-align: center; margin: 30px 0 25px; text-transform: uppercase;
}
.gj-preview-bizus h3 {
    background: #4A4A4A; color: white; padding: 13px 22px;
    border-radius: 18px; font-size: 13pt; font-weight: 700; margin: 22px 0 14px;
}
.gj-preview-bizus h4 {
    color: #4A4A4A; font-size: 13pt; font-weight: 700;
    margin: 18px 0 8px; border-bottom: 2px solid #C4D600; padding-bottom: 4px;
}
.gj-preview-bizus p { margin-bottom: 18px; text-align: justify; }
.gj-preview-bizus ul, .gj-preview-bizus ol { margin: 12px 0 12px 56px; }
.gj-preview-bizus li { margin: 6px 0; }
.gj-preview-bizus table {
    width: auto; min-width: 55%; max-width: 100%;
    border-collapse: collapse; margin: 26px auto;
    border-radius: 10px; overflow: hidden; border: 1px solid #eee;
}
.gj-preview-bizus th {
    background: #C4D600; color: white; padding: 11px 22px;
    text-align: center; font-weight: 800; text-transform: uppercase;
}
.gj-preview-bizus td {
    padding: 10px 18px; border-bottom: 1px solid #f0f0f0; text-align: center;
}
.gj-preview-bizus tr:last-child td { border-bottom: none; }
.gj-preview-bizus code {
    background: #f4f4f4; padding: 2px 6px; border-radius: 4px;
    font-family: monospace; font-size: .9em;
}
.gj-preview-bizus pre {
    background: #f4f4f4; padding: 16px; border-radius: 8px;
    overflow-x: auto; margin: 18px 0;
}
.gj-preview-bizus pre code { background:none; padding:0; }
.gj-preview-bizus blockquote {
    border-left: 4px solid #C4D600; padding: 10px 18px;
    margin: 18px 0; color: #555;
}
.gj-preview-bizus a { color: #1a73e8; }
.gj-preview-bizus strong { font-weight: 800; }
.gj-preview-bizus hr { border:none; border-top:2px solid #eee; margin:24px 0; }

/* Auto-boxes */
.gj-preview-bizus .auto-box {
    padding: 18px 22px; margin: 14px 0; border-radius: 14px;
}
.gj-preview-bizus .auto-box > p { margin-bottom: 8px; }
.gj-preview-bizus .auto-box > p:last-child { margin-bottom: 0; }
.gj-preview-bizus .box-vermelho { background:rgba(255,23,68,.07); border-left:5px solid #FF1744; }
.gj-preview-bizus .box-amarelo  { background:rgba(255,214,0,.09); border-left:5px solid #FFD600; }
.gj-preview-bizus .box-azul     { background:rgba(33,150,243,.07); border-left:5px solid #2196F3; }
.gj-preview-bizus .box-verde    { background:rgba(0,200,83,.07); border-left:5px solid #00C853; }
.gj-preview-bizus .box-laranja  { background:rgba(255,152,0,.09); border-left:5px solid #FF9800; }
.gj-preview-bizus .box-roxo     { background:rgba(156,39,176,.07); border-left:5px solid #9C27B0; }

.gj-subtitulo-italico {
    display: block; text-align: center;
    margin-top: -14px !important; margin-bottom: 32px !important;
    font-style: italic; color: #666; font-size: 12pt;
}

/* Preview content — Spoilers */
.gj-preview-spoilers {
    font-family: 'Nunito', sans-serif;
    color: #212121; line-height: 1.6; max-width: 860px;
    margin: 0 auto; padding: 40px 30px 60px;
    background: #fff; min-height: 100%; text-align: justify;
}
.gj-preview-spoilers .instrucao-inicial {
    background: rgba(196, 214, 0, 0.12); padding: 20px;
    border-radius: 12px; margin-bottom: 30px;
    border: 1px solid rgba(196, 214, 0, 0.2);
    border-left: 6px solid #C4D600;
    font-weight: 600; color: #212121;
}
.gj-preview-spoilers .instrucao-inicial strong { color: #4A4A4A; }
.gj-preview-spoilers .questao-box {
    background: #fafafa; border: 1px solid #eeeeee;
    border-radius: 10px; padding: 18px 22px; margin-bottom: 14px;
}
.gj-preview-spoilers .questao-box p { margin: 14px 0 0 0; text-align: justify; }
.gj-preview-spoilers .questao-box p:first-child { margin-top: 0; }
.gj-preview-spoilers .questao-box p.bloco-destaque { margin-top: 24px; }
.gj-preview-spoilers p { margin: 10px 0; text-align: justify; }
.gj-preview-spoilers strong { color: #4A4A4A; font-weight: 700; }

/* Scrollbars */
::-webkit-scrollbar { width:6px; height:6px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:#2a2a2a; border-radius:3px; }

/* Esconder elementos do Streamlit */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none !important;}

/* Ajustes de layout */
.stTextArea textarea { border-radius: 0 !important; }
.stTextArea > div > div > div { background: transparent !important; }
</style>
"""

# ══════════════════════════════════════════════════════
#  MARKDOWN PARSER (Python — substitui o marked.js)
# ══════════════════════════════════════════════════════
import re

def parse_markdown(text):
    """Parser Markdown simplificado mas funcional"""
    if not text:
        return ""

    lines = text.split('\n')
    html_lines = []
    in_code = False
    code_buffer = []
    in_blockquote = False
    bq_buffer = []
    in_list = False
    list_buffer = []
    list_type = None

    def flush_code():
        nonlocal code_buffer
        if code_buffer:
            code = '\n'.join(code_buffer)
            html_lines.append(f'<pre><code>{escape_html(code)}</code></pre>')
            code_buffer = []

    def flush_bq():
        nonlocal bq_buffer
        if bq_buffer:
            inner = '\n'.join(bq_buffer)
            html_lines.append(f'<blockquote>{parse_inline(inner)}</blockquote>')
            bq_buffer = []

    def flush_list():
        nonlocal list_buffer, list_type
        if list_buffer:
            items = ''.join([f'<li>{parse_inline(li)}</li>' for li in list_buffer])
            tag = 'ol' if list_type == 'ol' else 'ul'
            html_lines.append(f'<{tag}>{items}</{tag}>')
            list_buffer = []
            list_type = None

    def escape_html(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def parse_inline(text):
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
        # Strikethrough
        text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
        # Code inline
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        return text

    for line in lines:
        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_bq()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_buffer.append(line)
            continue

        # Blockquote
        if line.startswith('> '):
            flush_list()
            bq_buffer.append(line[2:])
            in_blockquote = True
            continue
        elif in_blockquote:
            flush_bq()
            in_blockquote = False

        # Lists
        list_match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        ol_match = re.match(r'^(\s*)\d+\.\s+(.+)$', line)

        if list_match:
            flush_bq()
            if list_type and list_type != 'ul':
                flush_list()
            list_type = 'ul'
            list_buffer.append(list_match.group(2))
            in_list = True
            continue
        elif ol_match:
            flush_bq()
            if list_type and list_type != 'ol':
                flush_list()
            list_type = 'ol'
            list_buffer.append(ol_match.group(2))
            in_list = True
            continue
        elif in_list and line.strip() == '':
            flush_list()
            in_list = False
            continue
        elif in_list:
            flush_list()
            in_list = False

        # Headers
        h_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if h_match:
            flush_bq()
            level = len(h_match.group(1))
            html_lines.append(f'<h{level}>{parse_inline(h_match.group(2))}</h{level}>')
            continue

        # Horizontal rule
        if re.match(r'^---+\s*$', line):
            html_lines.append('<hr>')
            continue

        # Tables
        if '|' in line and not line.strip().startswith('>'):
            parts = [p.strip() for p in line.split('|')]
            parts = [p for p in parts if p]
            if parts and all(re.match(r'^[-:]+[-|:]*$', p) for p in parts):
                continue  # separator line
            if parts:
                flush_bq()
                flush_list()
                # Simple table handling
                if not html_lines or not html_lines[-1].startswith('<table>'):
                    html_lines.append('<table><thead><tr>' + ''.join([f'<th>{parse_inline(p)}</th>' for p in parts]) + '</tr></thead><tbody>')
                else:
                    html_lines[-1] = html_lines[-1].replace('</tbody>', '')
                    html_lines.append('<tr>' + ''.join([f'<td>{parse_inline(p)}</td>' for p in parts]) + '</tr>')
                continue

        # Empty line
        if line.strip() == '':
            flush_bq()
            flush_list()
            continue

        # Regular paragraph
        flush_bq()
        flush_list()
        html_lines.append(f'<p>{parse_inline(line)}</p>')

    flush_code()
    flush_bq()
    flush_list()

    # Close any open table
    result = '\n'.join(html_lines)
    if '<table>' in result and '</tbody>' not in result:
        result += '</tbody></table>'

    return result


# ══════════════════════════════════════════════════════
#  PROCESSADORES DE TEMPLATE
# ══════════════════════════════════════════════════════

def process_boxes_bizus(html):
    """Processa caixas coloridas com emojis para template Bizus"""
    EMOJI_MAP = [
        ('box-vermelho', ['⚠️','🚫','❌','🔥','🛑','🚨','⛔']),
        ('box-amarelo',  ['💡','⚡','⭐','✨','🔦']),
        ('box-azul',     ['ℹ️','ℹ','📘','📌','📎','🟦','🔎']),
        ('box-verde',    ['✅','✔️','🌿','🎯','🟢']),
        ('box-laranja',  ['⚖️','⚖','🏛️','📜','🔶']),
        ('box-roxo',     ['📝','🖊️','🟣']),
    ]

    # Split into top-level elements (simplified)
    # We'll use regex to find <p> tags and process them
    def replace_boxes(match):
        p_content = match.group(1)
        p_text = re.sub(r'<[^>]+>', '', p_content).strip()

        for cls, emojis in EMOJI_MAP:
            for em in emojis:
                if p_text.startswith(em):
                    return f'<div class="auto-box {cls}"><p>{p_content}</p></div>'
        return match.group(0)

    html = re.sub(r'<p>(.*?)</p>', replace_boxes, html, flags=re.DOTALL)
    return html


def process_h2_subtitles(html):
    """Processa subtítulos em itálico após H2 para template Bizus"""
    # Find H2 followed by <em> or <p><em>...</em></p>
    html = re.sub(
        r'(</h2>\s*)(<em>(.*?)</em>|<p>\s*<em>(.*?)</em>\s*</p>)',
        lambda m: m.group(1) + f'<p class="subtitulo-italico"><em>{m.group(3) or m.group(4)}</em></p>',
        html
    )
    return html


def process_spoilers(html):
    """Processa template Spoilers"""
    # Add instruction banner
    result = '<div class="instrucao-inicial">⭐ <strong>Tente responder as questões abaixo antes de identificar as respostas. Elas servem como um checklist dos principais pontos que você deve saber sobre o conteúdo estudado:</strong></div>'

    # Split content into elements
    # Find question patterns: <p><strong>1.</strong> or <p><strong>1.</p>
    parts = re.split(r'(<p>\s*<strong>\d+\.</strong>.*?</p>)', html, flags=re.DOTALL)

    current_box = None
    for part in parts:
        if re.match(r'<p>\s*<strong>\d+\.</strong>', part):
            if current_box:
                result += '</div>'
            result += '<div class="questao-box">' + part
            current_box = True
        elif current_box and re.search(r'<strong>(Gabarito|Explicação|Explicacao)</strong>', part, re.I):
            result += '<p class="bloco-destaque">' + re.sub(r'^<p>', '', part)
        elif current_box:
            result += part
        else:
            result += part

    if current_box:
        result += '</div>'

    return result


# ══════════════════════════════════════════════════════
#  CONTEÚDOS GUIA
# ══════════════════════════════════════════════════════

GUIDE_BIZUS = """# Guia do Template Guruja
*Referência completa de formatação — apague e comece seu documento*

## Títulos e hierarquia

Use `#` para o título principal da apostila (H1), `##` para seções temáticas (H2) e `###` para subseções (H3). O H4 serve para tópicos menores dentro de uma subseção.

### Exemplo de subseção (H3)

Texto normal com **negrito**, _itálico_ e ~~tachado~~. Para código inline use `backticks`.

#### Tópico menor (H4)

O H4 aparece com sublinhado verde e sem fundo, ideal para subdivisões internas.

---

## Caixas coloridas

Inicie qualquer parágrafo com um dos emojis abaixo para criar automaticamente uma caixa destacada. Basta colocar o emoji no início da linha — nenhuma sintaxe especial necessária.

💡 **Amarela — Dica ou insight** — `💡 ⚡ ⭐ ✨ 🔦` — conceitos-chave, macetes de prova e pontos de atenção relevantes.

✅ **Verde — Regra ou confirmação** — `✅ ✔️ 🌿 🎯 🟢` — regras, gabaritos corretos e afirmações que o candidato deve fixar.

⚠️ **Vermelha — Alerta ou cuidado** — `⚠️ 🚫 ❌ 🔥 🛑 🚨 ⛔` — erros comuns, pegadinhas de prova e pontos críticos.

ℹ️ **Azul — Informação neutra** — `ℹ️ 📘 📌 📎 🟦 🔎` — referências normativas, definições técnicas e contexto.

⚖️ **Laranja — Base legal** — `⚖️ 🏛️ 📜 🔶` — artigos de lei, decretos, portarias e fundamentos jurídicos.

📝 **Roxa — Nota ou observação** — `📝 🖊️ 🟣` — comentários adicionais, ressalvas e notas do professor.

### Caixa com lista interna

Se o parágrafo com emoji for imediatamente seguido de uma lista (com ou sem linha em branco entre eles), **a lista é absorvida para dentro da caixa**:

🎯 **Requisitos para não-cumulatividade do IBS:**
- Operação tributada na etapa anterior
- Crédito escriturado no prazo legal
- Documentação fiscal válida e idônea

---

## Subtítulo após seção

## Tributos na Reforma Tributária
*Como CBS, IBS e IS substituem os tributos atuais*

O parágrafo em itálico logo após um H2 é automaticamente formatado como subtítulo centralizado, ideal para complementar o título da seção.

---

## Listas

### Lista simples
- Item principal da lista
- Outro item com **destaque** em negrito
- Item com _itálico_ para termos técnicos

### Lista numerada
1. Primeiro passo do procedimento
2. Segundo passo com mais detalhes
3. Conclusão do processo

---

## Tabelas

| Tributo | Substitui | Competência | Base Legal |
|---|---|---|---|
| CBS | PIS + COFINS + IPI | Federal | LC 214/2025 |
| IBS | ICMS + ISS | Est./Mun. | LC 214/2025 |
| IS | IPI (seletivos) | Federal | EC 132/2023 |

---

## Citação e código

> Esta é uma citação em destaque, útil para transcrever trechos de lei ou doutrina com formatação especial.

Bloco de código para fórmulas, comandos ou texto técnico:

```
BC do ICMS-ST = (Valor da mercadoria + frete + IPI) × (1 + MVA)
```

---

## Atalhos do editor

| Atalho | Ação |
|---|---|
| **Ctrl+S** | Baixar .md |
| **Ctrl+B** | Negrito |
| **Ctrl+I** | Itálico |
| **Ctrl+K** | Inserir link |
| **Ctrl+Z** | Desfazer |
| **Ctrl+Y** | Refazer |
"""

GUIDE_SPOILERS = """# Guia do Template Spoilers
*Referência de formatação — apague e comece seu documento*

## Como funciona

O template **Spoilers** transforma seu Markdown em caixas de questão individuais. Um banner de instrução é inserido automaticamente no topo e cada questão recebe um box separado.

## Formato obrigatório

Cada questão deve começar com um parágrafo cujo texto inicia com o número em negrito no formato `**N.` (dois asteriscos + número + ponto). O sistema detecta esse padrão e abre um novo box.

Parágrafos iniciados com `**Gabarito` ou `**Explicação` recebem margem superior maior para separação visual dentro do box.

## Regras resumidas

| Elemento | Como escrever no MD | Efeito no template |
|---|---|---|
| Enunciado | `**1.` texto da questão | Abre novo box de questão |
| Alternativas | Texto livre após o enunciado | Absorvido no mesmo box |
| Gabarito | `**Gabarito:**` resposta | Margem superior maior |
| Explicação | `**Explicação:**` texto | Margem superior maior |

Qualquer parágrafo entre o enunciado e o próximo número é automaticamente incluído no mesmo box.

---

## Exemplo completo

**1.** De acordo com a LC 214/2025, o IBS é um imposto de competência:

A) Federal
B) Estadual e Municipal
C) Exclusivamente estadual
D) Municipal

**Gabarito:** Letra B

**Explicação:** O IBS é de competência compartilhada entre estados e municípios, conforme previsto na LC 214/2025. Ele substitui o ICMS e o ISS.


**2.** A CBS substitui quais tributos federais?

**Gabarito:** PIS e COFINS

**Explicação:** A CBS (Contribuição sobre Bens e Serviços) unifica o PIS e a COFINS, simplificando a tributação federal sobre o consumo.
"""


# ══════════════════════════════════════════════════════
#  FUNÇÕES DE PERSISTÊNCIA (SALVAMENTO AUTOMÁTICO)
# ══════════════════════════════════════════════════════

DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_doc_path(doc_id):
    return os.path.join(DATA_DIR, f"{doc_id}.json")

def load_document(doc_id):
    path = get_doc_path(doc_id)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_document(doc_id, data):
    path = get_doc_path(doc_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True

def list_documents():
    docs = []
    for f in os.listdir(DATA_DIR):
        if f.endswith('.json'):
            doc_id = f[:-5]
            data = load_document(doc_id)
            if data:
                docs.append({
                    'id': doc_id,
                    'name': data.get('filename', 'Sem nome'),
                    'updated': data.get('last_saved', ''),
                    'template': data.get('template', 'bizus')
                })
    return sorted(docs, key=lambda x: x['updated'], reverse=True)


# ══════════════════════════════════════════════════════
#  INICIALIZAÇÃO DO ESTADO
# ══════════════════════════════════════════════════════

if 'doc_id' not in st.session_state:
    st.session_state.doc_id = f"doc_{int(time.time())}"
if 'content' not in st.session_state:
    st.session_state.content = GUIDE_BIZUS
if 'filename' not in st.session_state:
    st.session_state.filename = "novo-documento"
if 'template' not in st.session_state:
    st.session_state.template = 'bizus'
if 'last_saved' not in st.session_state:
    st.session_state.last_saved = None
if 'save_status' not in st.session_state:
    st.session_state.save_status = ""
if 'show_guide' not in st.session_state:
    st.session_state.show_guide = True

# ══════════════════════════════════════════════════════
#  SALVAMENTO AUTOMÁTICO (a cada 10s via callback)
# ══════════════════════════════════════════════════════

def auto_save():
    """Salva o documento atual no disco"""
    data = {
        'filename': st.session_state.filename,
        'content': st.session_state.content,
        'template': st.session_state.template,
        'last_saved': datetime.now().isoformat()
    }
    save_document(st.session_state.doc_id, data)
    st.session_state.last_saved = datetime.now()
    st.session_state.save_status = "✓ Salvo"

# Timer de salvamento automático
if 'auto_save_timer' not in st.session_state:
    st.session_state.auto_save_timer = time.time()

# Verifica se passaram 10 segundos desde o último salvamento
if time.time() - st.session_state.auto_save_timer >= 10:
    auto_save()
    st.session_state.auto_save_timer = time.time()
    st.rerun()


# ══════════════════════════════════════════════════════
#  INTERFACE — HEADER
# ══════════════════════════════════════════════════════

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Header HTML
header_html = f"""
<div class="gj-header">
    <div class="gj-header-left">
        <span class="gj-logo">Guruja <span>MD</span> Editor</span>
        <div class="gj-filename-wrap">
            <input type="text" class="gj-filename" value="{st.session_state.filename}" 
                   id="filename-input" onchange="window.parent.postMessage({{type:'filename', value:this.value}}, '*')">
            <span class="gj-filename-ext">.md</span>
        </div>
        <span class="gj-badge">online</span>
    </div>
    <div class="gj-header-right">
        <span class="gj-save-status" id="save-status">{st.session_state.save_status}</span>
        <button class="gj-btn gj-btn-ghost" onclick="window.parent.postMessage({{type:'download_md'}}, '*')">↓ Salvar .md</button>
        <button class="gj-btn gj-btn-primary" onclick="window.parent.postMessage({{type:'download_html'}}, '*')">↓ Salvar HTML</button>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  INTERFACE — CORPO PRINCIPAL (2 colunas)
# ══════════════════════════════════════════════════════

col_editor, col_preview = st.columns([1, 1])

with col_editor:
    # Toolbar
    toolbar_html = """
    <div class="gj-toolbar">
        <button class="gj-tbr-btn" onclick="wrapText('**','**')" title="Negrito">B</button>
        <button class="gj-tbr-btn" style="font-style:italic" onclick="wrapText('_','_')" title="Itálico">I</button>
        <button class="gj-tbr-btn" onclick="wrapText('~~','~~')" title="Tachado">S̶</button>
        <button class="gj-tbr-btn" onclick="wrapText('`','`')" title="Código">&lt;/&gt;</button>
        <div class="gj-tbr-sep"></div>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n# ')" title="H1">H1</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n## ')" title="H2">H2</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n### ')" title="H3">H3</button>
        <div class="gj-tbr-sep"></div>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n> ')" title="Citação">❝</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n```\n')" title="Bloco de código">```</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n---\n')" title="Separador">—</button>
        <div class="gj-tbr-sep"></div>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n- ')" title="Lista">• Lista</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n1. ')" title="Lista numerada">1. Lista</button>
        <div class="gj-tbr-sep"></div>
        <button class="gj-tbr-btn" onclick="wrapText('[','](url)')" title="Link">🔗</button>
        <div class="gj-tbr-sep"></div>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n💡 ')" title="Box amarelo">💡</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\nℹ️ ')" title="Box azul">ℹ️</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n✅ ')" title="Box verde">✅</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n⚠️ ')" title="Box vermelho">⚠️</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n⚖️ ')" title="Box laranja">⚖️</button>
        <button class="gj-tbr-btn" onclick="insertAtCursor('\n📝 ')" title="Box roxo">📝</button>
    </div>

    <script>
    function wrapText(before, after) {
        const ta = window.parent.document.querySelector('textarea[data-testid="stTextArea"], .stTextArea textarea');
        if (!ta) return;
        const start = ta.selectionStart;
        const end = ta.selectionEnd;
        const sel = ta.value.slice(start, end) || 'texto';
        ta.value = ta.value.slice(0, start) + before + sel + after + ta.value.slice(end);
        ta.focus();
        ta.setSelectionRange(start + before.length, start + before.length + sel.length);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    function insertAtCursor(text) {
        const ta = window.parent.document.querySelector('textarea[data-testid="stTextArea"], .stTextArea textarea');
        if (!ta) return;
        const start = ta.selectionStart;
        ta.value = ta.value.slice(0, start) + text + ta.value.slice(start);
        ta.focus();
        ta.setSelectionRange(start + text.length, start + text.length);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
    }
    </script>
    """
    st.markdown(toolbar_html, unsafe_allow_html=True)

    # Editor textarea
    new_content = st.text_area(
        "Editor",
        value=st.session_state.content,
        height=600,
        label_visibility="collapsed",
        key="editor_area"
    )

    # Atualiza conteúdo se mudou
    if new_content != st.session_state.content:
        st.session_state.content = new_content
        st.session_state.save_status = ""
        st.rerun()

    # Statusbar
    words = len(st.session_state.content.strip().split()) if st.session_state.content.strip() else 0
    chars = len(st.session_state.content)
    st.markdown(f"""
    <div class="gj-statusbar">
        <span>{words} palavras</span>
        <span>{chars} chars</span>
        <span style="margin-left:auto">{st.session_state.save_status}</span>
    </div>
    """, unsafe_allow_html=True)


with col_preview:
    # Preview bar com seletor de template
    preview_bar = f"""
    <div class="gj-preview-bar">
        <span class="gj-preview-label">Template:</span>
        <div style="display:flex;gap:5px;flex:1;justify-content:center">
            <button class="gj-pill {'active' if st.session_state.template == 'bizus' else ''}" 
                    onclick="window.parent.postMessage({{type:'template', value:'bizus'}}, '*')">Bizus</button>
            <button class="gj-pill {'active' if st.session_state.template == 'spoilers' else ''}" 
                    onclick="window.parent.postMessage({{type:'template', value:'spoilers'}}, '*')">Spoilers</button>
        </div>
        <button class="gj-tbr-btn" onclick="window.parent.postMessage({{type:'load_guide'}}, '*')" style="flex-shrink:0">📋 Guia</button>
    </div>
    """
    st.markdown(preview_bar, unsafe_allow_html=True)

    # Render preview
    html_content = parse_markdown(st.session_state.content)

    if st.session_state.template == 'bizus':
        html_content = process_boxes_bizus(html_content)
        html_content = process_h2_subtitles(html_content)
        preview_class = "gj-preview-bizus"
    else:
        html_content = process_spoilers(html_content)
        preview_class = "gj-preview-spoilers"

    st.markdown(f'<div class="{preview_class}">{html_content}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  SIDEBAR — GERENCIADOR DE DOCUMENTOS
# ══════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📁 Meus Documentos")

    # Novo documento
    if st.button("➕ Novo Documento", use_container_width=True):
        st.session_state.doc_id = f"doc_{int(time.time())}"
        st.session_state.content = ""
        st.session_state.filename = "novo-documento"
        st.session_state.template = "bizus"
        st.session_state.save_status = ""
        st.rerun()

    st.divider()

    # Lista de documentos salvos
    docs = list_documents()
    if docs:
        for doc in docs[:10]:  # Mostra os 10 mais recentes
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📄 {doc['name']}", key=f"doc_{doc['id']}", use_container_width=True):
                    data = load_document(doc['id'])
                    if data:
                        st.session_state.doc_id = doc['id']
                        st.session_state.content = data.get('content', '')
                        st.session_state.filename = data.get('filename', 'sem-nome')
                        st.session_state.template = data.get('template', 'bizus')
                        st.session_state.save_status = f"Carregado: {doc['updated'][:16]}"
                        st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{doc['id']}"):
                    path = get_doc_path(doc['id'])
                    if os.path.exists(path):
                        os.remove(path)
                    st.rerun()
    else:
        st.caption("Nenhum documento salvo ainda.")

    st.divider()

    # Info
    st.caption(f"💾 Salvamento automático a cada 10s")
    if st.session_state.last_saved:
        st.caption(f"Último salvamento: {st.session_state.last_saved.strftime('%H:%M:%S')}")


# ══════════════════════════════════════════════════════
#  HANDLERS DE MENSAGENS (botões JS → Python)
# ══════════════════════════════════════════════════════

# Usar componentes nativos do Streamlit para os botões que precisam de ação
# já que o postMessage não funciona diretamente no Streamlit

# Botão de download .md
st.markdown("""
<style>
#md-download, #html-download, #template-bizus, #template-spoilers, #load-guide-btn {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Criar botões invisíveis para capturar ações
if st.button("Download MD", key="md_download"):
    md_content = st.session_state.content
    st.download_button(
        label="📥 Clique para baixar",
        data=md_content,
        file_name=f"{st.session_state.filename}.md",
        mime="text/markdown",
        key="md_download_real"
    )

if st.button("Download HTML", key="html_download"):
    html_content = parse_markdown(st.session_state.content)
    if st.session_state.template == 'bizus':
        html_content = process_boxes_bizus(html_content)
        html_content = process_h2_subtitles(html_content)
        css_extra = """
        h1 { color:#4A4A4A; font-size:24pt; font-weight:800; text-align:left; margin:20px 0 10px; text-transform:uppercase; border-bottom:6px solid #C4D600; display:inline-block; padding-bottom:5px; }
        h2 { background:#C4D600; color:white; padding:18px 28px; border-radius:25px; font-size:17pt; font-weight:800; text-align:center; margin:30px 0 25px; text-transform:uppercase; }
        h3 { background:#4A4A4A; color:white; padding:13px 22px; border-radius:18px; font-size:13pt; font-weight:700; margin:22px 0 14px; }
        h4 { color:#4A4A4A; font-size:13pt; font-weight:700; margin:18px 0 8px; border-bottom:2px solid #C4D600; padding-bottom:4px; }
        .auto-box { padding:18px 22px; margin:14px 0; border-radius:14px; }
        .box-vermelho { background:rgba(255,23,68,.07); border-left:5px solid #FF1744; }
        .box-amarelo  { background:rgba(255,214,0,.09); border-left:5px solid #FFD600; }
        .box-azul     { background:rgba(33,150,243,.07); border-left:5px solid #2196F3; }
        .box-verde    { background:rgba(0,200,83,.07); border-left:5px solid #00C853; }
        .box-laranja  { background:rgba(255,152,0,.09); border-left:5px solid #FF9800; }
        .box-roxo     { background:rgba(156,39,176,.07); border-left:5px solid #9C27B0; }
        .subtitulo-italico { display:block; text-align:center; margin-top:-14px !important; margin-bottom:32px !important; font-style:italic; color:#666; font-size:12pt; }
        """
    else:
        html_content = process_spoilers(html_content)
        css_extra = """
        .instrucao-inicial { background:rgba(196,214,0,.12); padding:20px; border-radius:12px; margin-bottom:30px; border-left:6px solid #C4D600; font-weight:600; }
        .questao-box { background:#fafafa; border:1px solid #eee; border-radius:10px; padding:18px 22px; margin-bottom:14px; }
        .questao-box p.bloco-destaque { margin-top:24px; }
        """

    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{st.session_state.filename}</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: #fff; font-family: 'Nunito', sans-serif; color: #212121; line-height: 1.6; }}
.container {{ max-width: 900px; margin: 0 auto; padding: 40px 30px 60px; }}
p {{ margin-bottom: 18px; text-align: justify; }}
ul, ol {{ margin: 12px 0 12px 56px; }}
li {{ margin: 6px 0; }}
table {{ width: auto; min-width: 55%; max-width: 100%; border-collapse: collapse; margin: 26px auto; border: 1px solid #eee; border-radius: 10px; overflow: hidden; }}
th {{ background: #C4D600; color: white; padding: 11px 22px; text-align: center; font-weight: 800; text-transform: uppercase; }}
td {{ padding: 10px 18px; border-bottom: 1px solid #f0f0f0; text-align: center; }}
code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: .9em; }}
pre {{ background: #f4f4f4; padding: 16px; border-radius: 8px; overflow-x: auto; margin: 18px 0; }}
blockquote {{ border-left: 4px solid #C4D600; padding: 10px 18px; margin: 18px 0; color: #555; }}
strong {{ font-weight: 800; }}
hr {{ border: none; border-top: 2px solid #eee; margin: 24px 0; }}
{css_extra}
@media print {{ body {{ padding: 0; }} .container {{ padding: 20px; }} }}
</style>
</head>
<body>
<div class="container">
{html_content}
</div>
</body>
</html>"""

    st.download_button(
        label="📥 Clique para baixar HTML",
        data=full_html,
        file_name=f"{st.session_state.filename}.html",
        mime="text/html",
        key="html_download_real"
    )

# Template switcher
if st.button("Template Bizus", key="template_bizus"):
    st.session_state.template = "bizus"
    st.rerun()

if st.button("Template Spoilers", key="template_spoilers"):
    st.session_state.template = "spoilers"
    st.rerun()

# Load guide
if st.button("Load Guide", key="load_guide_btn"):
    if st.session_state.template == 'spoilers':
        st.session_state.content = GUIDE_SPOILERS
    else:
        st.session_state.content = GUIDE_BIZUS
    st.rerun()

# Atualizar filename
new_filename = st.text_input("Filename", value=st.session_state.filename, key="filename_input", label_visibility="collapsed")
if new_filename != st.session_state.filename:
    st.session_state.filename = new_filename
    st.rerun()
