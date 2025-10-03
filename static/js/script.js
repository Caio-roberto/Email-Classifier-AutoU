document.addEventListener('DOMContentLoaded', function() {
    console.log('Classificador de Emails carregado!');
});

document.getElementById('emailForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const error = document.getElementById('error');
    
    // Reset states
    error.style.display = 'none';
    results.style.display = 'none';
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
    loading.style.display = 'block';
    
    try {
        const formData = new FormData();
        
        // Verifica se é upload de arquivo ou texto
        const fileInput = document.getElementById('emailFile');
        const textInput = document.getElementById('emailText');
        
        if (fileInput.files.length > 0 && fileInput.files[0].name !== '') {
            const file = fileInput.files[0];
            
            // Validação do tipo de arquivo
            if (!file.name.toLowerCase().endsWith('.txt') && !file.name.toLowerCase().endsWith('.pdf')) {
                throw new Error('Por favor, selecione um arquivo .txt ou .pdf');
            }
            
            // Validação do tamanho do arquivo (max 5MB)
            if (file.size > 5 * 1024 * 1024) {
                throw new Error('O arquivo é muito grande. Tamanho máximo: 5MB');
            }
            
            formData.append('file', file);
        } else if (textInput.value.trim() !== '') {
            if (textInput.value.trim().length < 10) {
                throw new Error('O texto do email é muito curto. Mínimo 10 caracteres.');
            }
            formData.append('email_text', textInput.value);
        } else {
            throw new Error('Por favor, insira o conteúdo do email ou faça upload de um arquivo.');
        }
        
        const response = await fetch('/classify', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro ao processar o email');
        }
        
        // Exibir resultados
        displayResults(data);
        
    } catch (err) {
        showError(err.message);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Analisar Email';
        loading.style.display = 'none';
    }
});

function displayResults(data) {
    const results = document.getElementById('results');
    const classificationBadge = document.getElementById('classificationBadge');
    const contentPreview = document.getElementById('contentPreview');
    const suggestedResponse = document.getElementById('suggestedResponse');
    
    // Atualizar classificação
    classificationBadge.textContent = data.classification;
    classificationBadge.className = `badge fs-6 ${
        data.classification === 'Produtivo' ? 'bg-success' : 'bg-secondary'
    }`;
    
    // Atualizar prévia do conteúdo
    contentPreview.textContent = data.content_preview || 'Nenhum conteúdo para exibir';
    
    // Atualizar resposta sugerida
    suggestedResponse.textContent = data.response;
    
    // Mostrar resultados com animação
    results.style.display = 'block';
    results.classList.add('fade-in');
    
    // Scroll suave para resultados
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    const error = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    error.style.display = 'block';
    error.classList.add('fade-in');
    
    // Scroll para erro
    error.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function copyResponse() {
    const responseText = document.getElementById('suggestedResponse').textContent;
    
    navigator.clipboard.writeText(responseText).then(() => {
        // Feedback visual
        const btn = event.target;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check me-1"></i>Copiado!';
        btn.classList.remove('btn-outline-primary');
        btn.classList.add('btn-success');
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-primary');
        }, 2000);
    }).catch(err => {
        console.error('Erro ao copiar: ', err);
        alert('Erro ao copiar texto. Tente selecionar e copiar manualmente.');
    });
}

// Limpar formulário ao mudar de aba
document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
    tab.addEventListener('shown.bs.tab', () => {
        document.getElementById('error').style.display = 'none';
    });
});

// Exemplo de email para teste rápido
document.addEventListener('DOMContentLoaded', function() {
    // Adiciona exemplo de email no textarea para facilitar teste
    const textarea = document.getElementById('emailText');
    if (textarea && textarea.value === '') {
        textarea.placeholder = 'Exemplo: "Prezados, estou com problema no sistema de pagamentos. Quando tento processar um pagamento, recebo erro. Podem ajudar?"\n\nCole seu email aqui...';
    }
});