from flask import Flask, render_template, request, jsonify
import os
from utils.email_processor import process_email_content
from utils.ai_classifier import classify_email, generate_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    try:
        # Obter conteúdo do email
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            content = process_email_content(file)
        else:
            content = request.form['email_text']
        
        if not content.strip():
            return jsonify({'error': 'Nenhum conteúdo fornecido'}), 400
        
        # Classificar email
        classification = classify_email(content)
        
        # Gerar resposta
        response = generate_response(content, classification)
        
        return jsonify({
            'classification': classification,
            'response': response,
            'content_preview': content[:200] + '...' if len(content) > 200 else content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)