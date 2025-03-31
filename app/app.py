from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import sys
import json

# Import from your modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sentiment_analysis import EmotionalToneAnalyzer
from suggestion_generator import generate_improved_sentence_with_gpt, get_emotion_general_suggestions

app = Flask(__name__)

# Initialize the analyzer
analyzer = EmotionalToneAnalyzer()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze the text submitted by the user."""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        # Perform the analysis
        analysis = analyzer.analyze_document(text)
        
        # Create emotional arc visualization
        plt_obj = analyzer.visualize_emotional_arc(analysis)
        
        # Convert plot to base64 image
        img = BytesIO()
        plt_obj.savefig(img, format='png', bbox_inches='tight')
        plt_obj.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        # Create radar chart visualization
        radar_plt = analyzer.create_emotion_radar_chart(analysis)
        
        # Convert radar plot to base64 image
        radar_img = BytesIO()
        radar_plt.savefig(radar_img, format='png', bbox_inches='tight')
        radar_plt.close()
        radar_img.seek(0)
        radar_plot_url = base64.b64encode(radar_img.getvalue()).decode('utf8')
        
        # Prepare response
        response = {
            'document_sentiment': analysis['document_sentiment'],
            'document_emotions': analysis['document_emotions'],
            'emotional_shifts': analysis['emotional_shifts'],
            'consistency_check': analysis['consistency_check'],
            'plot_url': plot_url,
            'radar_plot_url': radar_plot_url
        }
    
        return jsonify(response)
    except Exception as e:
        print("Error during /analyze:", e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    """Generate suggestions for improving emotional tone with specific text replacement examples."""
    data = request.json
    text = data.get('text', '')
    target_emotion = data.get('target_emotion', '')

    if not text or not target_emotion:
        return jsonify({'error': 'Text and target emotion are required'})

    # Analyze the current text
    current_analysis = analyzer.analyze_document(text)

    # Get sentence analysis to find weak sentences to improve
    sentences = current_analysis['sentence_analysis']

    # Find sentences that don't match the target emotion
    sentences_to_improve = []
    for sent_data in sentences:
        if sent_data['emotions']['dominant_emotion'] != target_emotion:
            sentences_to_improve.append({
                'sentence': sent_data['sentence'],
                'current_emotion': sent_data['emotions']['dominant_emotion']
            })

    # If no sentences to improve or too many, select a few representative ones
    if not sentences_to_improve:
        # Just pick the first 2 sentences if we have no specific targets
        if len(sentences) > 2:
            sentences_to_improve = [{'sentence': s['sentence'], 'current_emotion': s['emotions']['dominant_emotion']} 
                                for s in sentences[:2]]
        else:
            sentences_to_improve = [{'sentence': s['sentence'], 'current_emotion': s['emotions']['dominant_emotion']} 
                                for s in sentences]
    elif len(sentences_to_improve) > 3:
        # Limit to 3 sentences if too many to improve
        sentences_to_improve = sentences_to_improve[:3]

    # Generate specific suggestions for each sentence
    specific_suggestions = []
    
    for sentence_data in sentences_to_improve:
        original = sentence_data['sentence']
        # Use the imported function to generate improved sentences
        improved = generate_improved_sentence_with_gpt(original, target_emotion)
        
        specific_suggestions.append({
            'original': original,
            'improved': improved,
            'emotion': {
                'current': sentence_data['current_emotion'],
                'target': target_emotion
            }
        })
    
    # Get general suggestions based on target emotion
    general_suggestions = get_emotion_general_suggestions(target_emotion)
    
    return jsonify({
        'current_dominant_emotion': current_analysis['document_emotions']['dominant_emotion'],
        'target_emotion': target_emotion,
        'specific_suggestions': specific_suggestions,
        'general_suggestions': general_suggestions
    })

if __name__ == '__main__':
    # Make sure necessary directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)
