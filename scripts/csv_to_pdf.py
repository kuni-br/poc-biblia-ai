# csv_to_pdf.py
# Instale as dependências: pip install reportlab pandas

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
import re

def clean_markdown(text):
    """Converte marcações Markdown básicas para formato compatível com ReportLab"""
    # Negrito **texto** -> <b>texto</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Itálico *texto* -> <i>texto</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Listas com * ou - no início da linha
    text = re.sub(r'^[\*\-]\s+(.+)$', r'• \1', text, flags=re.MULTILINE)
    # Números de lista 1. 2. 3.
    text = re.sub(r'^\d+\.\s+(.+)$', r'\1', text, flags=re.MULTILINE)
    # Referências bíblicas em negrito
    text = re.sub(r'(\w+\s+\d+:\d+)', r'<b>\1</b>', text)
    return text

def create_pdf(input_csv, output_pdf):
    # Leitura do CSV
    df = pd.read_csv(input_csv)
    
    # Configuração do documento
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    style_title = ParagraphStyle(
        'QuestionTitle',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        spaceAfter=12,
        textColor=colors.darkblue,
        borderPadding=8,
        borderColor=colors.lightgrey,
        borderWidth=1
        #borderPadding=10
    )
    
    style_answer = ParagraphStyle(
        'AnswerBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        firstLineIndent=0
    )
    
    style_reference = ParagraphStyle(
        'References',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=colors.darkgreen,
        spaceBefore=5,
        spaceAfter=15,
        leftIndent=1*cm
    )
    
    style_separator = ParagraphStyle(
        'Separator',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_LEFT,
        spaceBefore=5,
        spaceAfter=10
    )
    
    elements = []
    
    # Cabeçalho do documento
    header_title = Paragraph(
        '<b>Validação de Respostas - Agentes de IA</b><br/>'
        '<i>Perguntas Filosófico-Existenciais com Fundamentação Bíblica</i>',
        styles['Heading1']
    )
    elements.append(header_title)
    elements.append(Spacer(1, 0.5*cm))
    
    # Metadados do documento
    meta_info = Paragraph(
        f'<b>Total de perguntas:</b> {len(df)} | '
        f'<b>Data de geração:</b> Documento para avaliação especializada',
        style_separator
    )
    elements.append(meta_info)
    elements.append(Spacer(1, 1*cm))
    
    # Processamento de cada linha
    for idx, row in df.iterrows():
        pergunta = str(row['pergunta']).strip()
        conteudo = str(row['conteudo']).strip()
        
        # Número da questão
        question_number = Paragraph(
            f'<b>QUESTÃO {idx + 1}</b>',
            ParagraphStyle('QNumber', parent=styles['Heading3'], textColor=colors.darkred)
        )
        elements.append(question_number)
        elements.append(Spacer(1, 0.3*cm))
        
        # Pergunta formatada
        pergunta_formatada = clean_markdown(f'<b>Pergunta:</b> {pergunta}')
        elements.append(Paragraph(pergunta_formatada, style_title))
        
        # Resposta formatada
        conteudo_formatado = clean_markdown(conteudo)
        elements.append(Paragraph('<b>Resposta da IA:</b>', styles['Heading3']))
        elements.append(Paragraph(conteudo_formatado, style_answer))
        
        # Separador visual entre questões
        elements.append(Paragraph('─' * 50, style_separator))
        elements.append(PageBreak())
    
    # Rodapé informativo
    footer = Paragraph(
        '<i>Documento gerado para validação por especialista. '
        'As respostas foram produzidas por agentes de IA com fundamentação bíblica.</i>',
        style_separator
    )
    elements.append(footer)
    
    # Geração do PDF
    doc.build(elements)
    print(f"✓ PDF gerado com sucesso: {output_pdf}")
    print(f"✓ Total de questões processadas: {len(df)}")

# Execução
if __name__ == "__main__":
    create_pdf('data/csv/poc_biblia_ai.csv', 'data/pdf/validacao_respostas_ia.pdf')