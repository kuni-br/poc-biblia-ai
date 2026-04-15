# csv_to_html.py
# Gera HTML formatado que pode ser convertido para PDF via navegador ou wkhtmltopdf

import pandas as pd
import re

def markdown_to_html(text):
    """Converte Markdown básico para HTML"""
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'^[\*\-]\s+(.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.+?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    text = re.sub(r'\n\n', r'</p><p>', text)
    text = f'<p>{text}</p>'
    return text

def generate_html(input_csv, output_html):
    df = pd.read_csv(input_csv)
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Validação de Respostas - Agentes de IA</title>
    <style>
        @page {{ size: A4; margin: 2cm; }}
        body {{ 
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            color: #333;
            max-width: 21cm;
            margin: 0 auto;
            padding: 2cm;
        }}
        .header {{ 
            border-bottom: 3px solid #2c5282; 
            padding-bottom: 1cm; 
            margin-bottom: 1.5cm;
        }}
        .header h1 {{ margin: 0; color: #2c5282; }}
        .header p {{ margin: 0.5cm 0 0; color: #666; font-style: italic; }}
        .question-block {{ 
            margin-bottom: 2cm; 
            page-break-inside: avoid;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5cm;
            background: #fafafa;
        }}
        .question-number {{ 
            color: #c53030; 
            font-weight: bold; 
            font-size: 1.1em;
            margin-bottom: 0.5cm;
        }}
        .question {{ 
            background: #ebf8ff; 
            border-left: 4px solid #3182ce; 
            padding: 1cm; 
            margin: 0.5cm 0;
            border-radius: 0 4px 4px 0;
        }}
        .question strong {{ color: #2c5282; }}
        .answer {{ margin: 1cm 0; }}
        .answer-label {{ font-weight: bold; color: #276749; margin-bottom: 0.5cm; }}
        .references {{ 
            font-size: 0.9em; 
            color: #2f855a; 
            margin-top: 1cm; 
            padding-top: 0.5cm;
            border-top: 1px dashed #a0aec0;
        }}
        .separator {{ 
            text-align: center; 
            color: #a0aec0; 
            margin: 1cm 0;
            font-size: 0.9em;
        }}
        .footer {{ 
            margin-top: 2cm; 
            padding-top: 1cm; 
            border-top: 1px solid #e2e8f0;
            font-size: 0.9em;
            color: #718096;
            font-style: italic;
        }}
        ul {{ padding-left: 1.5cm; }}
        li {{ margin: 0.3cm 0; }}
        @media print {{
            .question-block {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Validação de Respostas - Agentes de IA</h1>
        <p>Perguntas Filosófico-Existenciais com Fundamentação Bíblica</p>
        <p><strong>Total de questões:</strong> {len(df)} | <strong>Finalidade:</strong> Avaliação por especialista</p>
    </div>
'''
    
    for idx, row in df.iterrows():
        pergunta = row['pergunta']
        conteudo = row['conteudo']
        
        # Extrair referências bíblicas se existirem
        refs_match = re.search(r'\*\*Referências? Bíblicas?:\*\*\s*(.+?)(?:\n\n|$)', conteudo, re.DOTALL)
        if refs_match:
            references = refs_match.group(1).strip()
            conteudo_limpo = re.sub(r'\*\*Referências? Bíblicas?:\*\*\s*.+?(?:\n\n|$)', '', conteudo, flags=re.DOTALL).strip()
        else:
            references = None
            conteudo_limpo = conteudo
        
        html += f'''
    <div class="question-block">
        <div class="question-number">QUESTÃO {idx + 1}</div>
        
        <div class="question">
            <strong>Pergunta:</strong> {pergunta}
        </div>
        
        <div class="answer">
            <div class="answer-label">Resposta da IA:</div>
            {markdown_to_html(conteudo_limpo)}
        </div>
'''
        if references:
            html += f'''
        <div class="references">
            <strong>Referências:</strong> {references}
        </div>
'''
        html += '''
        <div class="separator">────────────────────────────────────────</div>
    </div>
'''
    
    html += '''
    <div class="footer">
        Documento gerado para validação por especialista. 
        As respostas foram produzidas por agentes de IA com fundamentação bíblica.
    </div>
</body>
</html>'''
    
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✓ HTML gerado: {output_html}")
    print(f"✓ Para converter para PDF: abra no navegador e use 'Imprimir → Salvar como PDF'")
    print(f"✓ Ou use: wkhtmltopdf {output_html} saida.pdf")

if __name__ == "__main__":
    generate_html('data/csv/poc_biblia_ai.csv', 'data/html/validacao_respostas.html')