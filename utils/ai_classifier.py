from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

class EmailClassifier:
    def __init__(self):
        print("Inicializando classificador inteligente...")
        
        # API para análise SEMÂNTICA (não apenas sentimento)
        try:
            self.sentiment_analyzer = pipeline(
                "text-classification",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                tokenizer="nlptown/bert-base-multilingual-uncased-sentiment"
            )
            
            # NOVA API: Análise de zero-shot classification para detectar INTENÇÃO
            self.intent_classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            print("APIs de IA carregadas com sucesso!")
            
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            self.sentiment_analyzer = None
            self.intent_classifier = None
        
        # Palavras-chave como backup/refinamento
        self.productive_indicators = [
            'problema', 'erro', 'bug', 'urgente', 'suporte', 'ajuda', 'solicitação',
            'pagamento', 'sistema', 'funciona', 'resolver', 'timeout', 'conexão',
            'atualização', 'status', 'cliente', 'contrato', 'financeiro'
        ]
        
        self.unproductive_indicators = [
            'feliz natal', 'ano novo', 'parabéns', 'festas', 'comemorações',
            'cumprimentos', 'abraços', 'beijos', 'sucesso', 'conquistas'
        ]

    def analyze_with_ai(self, content):
        if not self.sentiment_analyzer or not self.intent_classifier:
            return None
            
        try:
            # ANÁLISE DE INTENÇÃO (Zero-shot classification)
            intent_categories = ["solicitação de ajuda", "reporte de problema", "questão comercial", "cumprimentos", "agradecimentos"]
            
            intent_result = self.intent_classifier(
                content[:512],
                intent_categories,
                multi_label=False
            )
            
            return {
                'intent': intent_result['labels'][0],  # Intenção principal
                'intent_confidence': intent_result['scores'][0], # Confiança na intenção
            }
            
        except Exception as e:
            print(f"Erro na análise IA: {e}")
            return None

    def classify_email(self, content):
        if not content:
            return "Improdutivo"
            
        content_lower = content.lower()
        
        # 1. VERIFICAÇÃO RÁPIDA: Frases obviamente improdutivas
        strong_unproductive = ['feliz natal', 'ano novo', 'parabéns', 'obrigado pela parceria']
        if any(phrase in content_lower for phrase in strong_unproductive):
            return "Improdutivo"
        
        # 2. ANÁLISE COM IA (se disponível)
        ai_analysis = self.analyze_with_ai(content)
        
        if ai_analysis:
            # LÓGICA INTELIGENTE baseada na análise semântica
            intent = ai_analysis['intent']
            intent_conf = ai_analysis['intent_confidence']
            
            # Intenções produtivas com alta confiança
            productive_intents = ["solicitação de ajuda", "reporte de problema", "questão comercial"]
            if intent in productive_intents and intent_conf > 0.7:
                return "Produtivo"
            
            # Intenções improdutivas
            unproductive_intents = ["cumprimentos", "agradecimentos"]
            if intent in unproductive_intents and intent_conf > 0.6:
                return "Improdutivo"
        
        # 3. FALLBACK: Análise por palavras-chave (quando IA não é conclusiva)
        productive_count = sum(1 for word in self.productive_indicators if word in content_lower)
        unproductive_count = sum(1 for word in self.unproductive_indicators if word in content_lower)
        
        if productive_count >= 2 or (productive_count == 1 and unproductive_count == 0):
            return "Produtivo"
        else:
            return "Improdutivo"

    def generate_response(self, content, classification):
        content_lower = content.lower()
        
        # Análise semântica para personalizar resposta
        ai_analysis = self.analyze_with_ai(content) if hasattr(self, 'intent_classifier') else None
        
        if classification == "Produtivo":
            # Detectar o tipo específico de problema usando IA
            if ai_analysis and ai_analysis['intent'] == "reporte de problema":
                urgency = "URGENTE" if any(word in content_lower for word in ['urgente', 'crítico', 'asap']) else "NORMAL"
                return f"Suporte Técnico - {urgency}\nProblema técnico identificado e em análise. Nossa equipe trabalha na solução.\nPrevisão: 2-4 horas | Ticket: #T{abs(hash(content)) % 10000}"
            
            elif ai_analysis and ai_analysis['intent'] == "solicitação de ajuda":
                return f"Suporte ao Cliente\nSolicitação de ajuda recebida. Especialista designado responderá em até 2h.\nProtocolo: #C{abs(hash(content)) % 10000}"
            
            else:
                return f"Solicitação Recebida\nEm processamento. Retornaremos em 24h úteis.\nProtocolo: #{abs(hash(content)) % 10000}"
        
        else:
            # Respostas personalizadas baseadas na análise semântica
            if ai_analysis and ai_analysis['intent'] == "cumprimentos":
                return "Agradecemos os cumprimentos! - Desejamos um excelente final de ano! - Resposta Automática"
            
            elif ai_analysis and ai_analysis['intent'] == "agradecimentos":
                return "Obrigado pelo feedback! - Ficamos felizes em ajudar! - Resposta Automática"
            
            else:
                return "Mensagem Recebida - Agradecemos o contato. Para assuntos urgentes, contate nosso suporte."

# Instância global
classifier = EmailClassifier()

def classify_email(content):
    return classifier.classify_email(content)

def generate_response(content, classification):
    return classifier.generate_response(content, classification)
