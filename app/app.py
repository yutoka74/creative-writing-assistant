from flask import Flask, render_template, request, jsonify
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import sys
import json
import re

# Import from your sentiment_analysis.py
# Make sure the EmotionalToneAnalyzer class is properly imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from sentiment_analysis import EmotionalToneAnalyzer

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
        improved = generate_improved_sentence(original, target_emotion)
        
        specific_suggestions.append({
            'original': original,
            'improved': improved,
            'emotion': {
                'current': sentence_data['current_emotion'],
                'target': target_emotion
            }
        })
    
    # Generate general suggestions based on the target emotion
    general_suggestions = []
    
    if target_emotion == 'joy':
        general_suggestions.append("Use more positive and uplifting language throughout your text.")
        general_suggestions.append("Incorporate words that evoke happiness such as 'delighted', 'ecstatic', 'thrilled'.")
        general_suggestions.append("Describe pleasant sensory experiences like warm sunlight, gentle breezes, or sweet aromas.")
    elif target_emotion == 'sadness':
        general_suggestions.append("Use more melancholic and reflective language throughout your text.")
        general_suggestions.append("Consider words like 'somber', 'wistful', 'longing', 'melancholy'.")
        general_suggestions.append("Slow down the narrative pace with longer, more flowing sentences.")
    elif target_emotion == 'anger':
        general_suggestions.append("Use shorter, more dynamic sentences to convey intensity.")
        general_suggestions.append("Consider words like 'furious', 'enraged', 'seething', 'burning'.")
        general_suggestions.append("Use harsh consonant sounds and incorporate metaphors related to fire or storms.")
    elif target_emotion == 'fear':
        general_suggestions.append("Build suspense through pacing and ambiguity throughout your text.")
        general_suggestions.append("Use words like 'dread', 'terrified', 'ominous', 'looming'.")
        general_suggestions.append("Describe physiological responses to fear (racing heart, shortness of breath).")
    elif target_emotion == 'surprise':
        general_suggestions.append("Use sentence structures that create sudden revelations throughout your text.")
        general_suggestions.append("Consider words like 'astonished', 'startled', 'unexpected', 'shocked'.")
        general_suggestions.append("Build up expectations in one direction, then subvert them for dramatic effect.")
    else:
        general_suggestions.append(f"To enhance {target_emotion}, consider the emotional tone of your language.")
        general_suggestions.append("Pay attention to word choice, sentence structure, and pacing.")
        general_suggestions.append("Ensure consistency in emotional tone throughout your text.")
    
    return jsonify({
        'current_dominant_emotion': current_analysis['document_emotions']['dominant_emotion'],
        'target_emotion': target_emotion,
        'specific_suggestions': specific_suggestions,
        'general_suggestions': general_suggestions
    })

def generate_improved_sentence(original, target_emotion):
    """Generate an improved version of a sentence to better match the target emotion."""
    # This function would ideally use a more sophisticated approach like LLM
    # For now, we'll use simple replacements and additions based on the target emotion
    
    if target_emotion == 'joy':
        # For joy, make sentences more upbeat and positive
        improvements = {
            'the morning': 'the glorious morning',
            'beautiful': 'breathtakingly beautiful',
            'good': 'wonderful',
            'nice': 'delightful',
            'happy': 'overjoyed',
            'smiled': 'beamed with happiness',
            'sun': 'golden sun',
            'walked': 'strolled happily',
            'said': 'exclaimed cheerfully',
            'looked': 'gazed with delight',
            'day': 'perfect day',
            'night': 'magical night',
            'dark': 'mysterious',
            'storm': 'refreshing rain',
            'clouds': 'fluffy clouds'
        }
    elif target_emotion == 'sadness':
        # For sadness, add melancholic elements
        improvements = {
            'the morning': 'the lonely morning',
            'beautiful': 'hauntingly beautiful',
            'good': 'bittersweet',
            'happy': 'momentarily content',
            'smiled': 'smiled weakly',
            'sun': 'fading sun',
            'walked': 'trudged wearily',
            'said': 'murmured softly',
            'looked': 'gazed longingly',
            'day': 'long, empty day',
            'night': 'solitary night',
            'clouds': 'gray, heavy clouds',
            'storm': 'relentless storm'
        }
    elif target_emotion == 'anger':
        # For anger, add intensity and sharpness
        improvements = {
            'the morning': 'the harsh morning',
            'beautiful': 'deceptively serene',
            'good': 'barely tolerable',
            'walked': 'stormed',
            'said': 'snapped',
            'looked': 'glared',
            'day': 'frustrating day',
            'night': 'tense night',
            'sun': 'scorching sun',
            'clouds': 'threatening clouds',
            'storm': 'violent storm'
        }
    elif target_emotion == 'fear':
        # For fear, add elements of uncertainty and threat
        improvements = {
            'the morning': 'the eerily silent morning',
            'beautiful': 'unnervingly quiet',
            'good': 'unsettlingly calm',
            'walked': 'crept cautiously',
            'said': 'whispered nervously',
            'looked': 'peered anxiously',
            'day': 'foreboding day',
            'night': 'pitch-black night',
            'sun': 'obscured sun',
            'clouds': 'ominous clouds',
            'storm': 'terrifying storm'
        }
    elif target_emotion == 'surprise':
        # For surprise, add unexpected elements
        improvements = {
            'the morning': 'the suddenly bright morning',
            'beautiful': 'unexpectedly stunning',
            'walked': 'stumbled upon',
            'said': 'blurted out',
            'looked': 'stared in astonishment',
            'day': 'remarkable day',
            'night': 'extraordinary night',
            'sun': 'blinding sun',
            'clouds': 'rapidly forming clouds',
            'storm': 'sudden, explosive storm'
        }
    else:
        # Default case - minimal changes
        improvements = {
            'good': 'fine',
            'bad': 'challenging',
            'happy': 'content',
            'sad': 'thoughtful'
        }
    
    # Apply the replacements
    improved = original
    for word, replacement in improvements.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        improved = pattern.sub(replacement, improved)
    
    # If the sentence didn't change much, add some emotion-specific modifications
    if improved == original or len(improvements) < 2:
        if target_emotion == 'joy':
            improved = improved.rstrip('.') + ', filling the moment with pure happiness.'
        elif target_emotion == 'sadness':
            improved = improved.rstrip('.') + ', leaving a sense of melancholy in the air.'
        elif target_emotion == 'anger':
            improved = improved.rstrip('.') + ', fueling a burning frustration.'
        elif target_emotion == 'fear':
            improved = improved.rstrip('.') + ', sending a chill down the spine.'
        elif target_emotion == 'surprise':
            improved = improved.rstrip('.') + ', completely defying all expectations!'
    
    return improved

if __name__ == '__main__':
    # Make sure necessary directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)
