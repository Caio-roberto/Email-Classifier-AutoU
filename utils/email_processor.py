import pdfplumber
import re

def process_email_content(file):
    filename = file.filename.lower()
    
    if filename.endswith('.txt'):
        content = file.read().decode('utf-8')
    
    elif filename.endswith('.pdf'):
        content = extract_text_from_pdf(file)
    
    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf")
    
    return clean_email_content(content)

def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise ValueError(f"Erro ao ler PDF: {str(e)}")
    
    return text.strip()

def clean_email_content(content):
    """Limpa e pré-processa o conteúdo do email"""
    if not content:
        return ""
    
    # Remove assinaturas comuns
    patterns = [
        r'Best regards,.*',
        r'Atenciosamente,.*',
        r'Cheers,.*',
        r'Thank you,.*',
        r'Obrigado,.*',
        r'Att,.*',
        r'Abraços,.*'
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
    
    return content.strip()

# Teste simples para verificar se o arquivo funciona
if __name__ == "__main__":
    print("Módulo email_processor carregado com sucesso!")