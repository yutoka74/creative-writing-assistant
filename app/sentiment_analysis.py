import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import numpy as np
import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import re
import spacy
import matplotlib.pyplot as plt
from config import EMOTION_COLORS
import os

# Set tokenizer parallelism configuration
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Ensure necessary NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model for syntactic parsing
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import sys
    print("Please install the spaCy model with: python -m spacy download en_core_web_sm")
    sys.exit(1)

class EmotionalToneAnalyzer:
    """
    A class to analyze emotional tone in text at various levels:
    - Sentence level
    - Paragraph level
    - Document level
    """
    
    def __init__(self):
        """Initialize the emotional tone analyzer with required models."""
        # Load pre-trained sentiment analysis model
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )

        # Load emotion detection model
        self.emotion_analyzer = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base", 
            return_all_scores=True
        )

        # Define emotion categories we're tracking
        self.emotion_categories = [
            "joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"
        ]
        
        # NRC Emotion Lexicon simulation (simplified version)
        # In a production environment, you would load the actual NRC lexicon
        self.emotion_lexicon = {
            "happy": ["joy"],
            "sad": ["sadness"],
            "angry": ["anger"],
            "afraid": ["fear"],
            "surprised": ["surprise"],
            "disgusted": ["disgust"],
            "content": ["joy"],
            "miserable": ["sadness"],
            "furious": ["anger"],
            "terrified": ["fear"],
            "astonished": ["surprise"],
            "revolted": ["disgust"],
            # Add more words as needed
        }
        
        # Stop words to filter out
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text):
        """Preprocess text for analysis."""
        # Normalize text: lowercase, remove special chars, etc.
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()

        # Tokenize into sentences
        sentences = sent_tokenize(text)

        # Tokenize into words and remove stopwords (for word-level analysis)
        tokenized_sentences = []
        filtered_sentences = []

        for sentence in sentences:
            words = word_tokenize(sentence)
            tokenized_sentences.append(words)

            # Filter stopwords
            filtered_words = [word for word in words if word.lower() not in self.stop_words]
            filtered_sentences.append(filtered_words)

        # Syntactic parsing using spaCy
        parsed_doc = nlp(text)
        
        return {
            "original_text": text,
            "sentences": sentences,
            "tokenized_sentences": tokenized_sentences,
            "filtered_sentences": filtered_sentences,
            "parsed_doc": parsed_doc
        }
    
    def analyze_sentiment(self, text):
        """Analyze the overall sentiment of the text."""
        results = self.sentiment_analyzer(text)
        
        # Extract positive/negative sentiment scores
        sentiment_scores = results[0]
        sentiment_dict = {item['label']: item['score'] for item in sentiment_scores}
        
        # Determine overall sentiment
        if sentiment_dict.get('POSITIVE', 0) > sentiment_dict.get('NEGATIVE', 0):
            overall_sentiment = "positive"
        else:
            overall_sentiment = "negative"
        
        return {
            "scores": sentiment_dict,
            "overall_sentiment": overall_sentiment
        }
    
    def analyze_emotions(self, text):
        """Analyze the emotions expressed in the text."""
        try:
            # Get emotion scores from the model
            results = self.emotion_analyzer(text)
            
            # Extract emotion scores
            emotion_scores = results[0]
            emotion_dict = {item['label']: item['score'] for item in emotion_scores}
            
            # Find dominant emotion
            dominant_emotion = max(emotion_dict.items(), key=lambda x: x[1])[0]

            return {
                "scores": emotion_dict,
                "dominant_emotion": dominant_emotion
            }
        except Exception as e:
            print(f"Error analyzing emotions: {e}")
            # Fallback to lexicon-based approach if model fails
            return self._analyze_emotions_lexicon_based(text)
    
    def _analyze_emotions_lexicon_based(self, text):
        """Fallback method using lexicon-based approach."""
        emotion_counts = {emotion: 0 for emotion in self.emotion_categories}
        
        # Tokenize and check words against our lexicon
        words = word_tokenize(text.lower())
        for word in words:
            if word in self.emotion_lexicon:
                for emotion in self.emotion_lexicon[word]:
                    if emotion in emotion_counts:
                        emotion_counts[emotion] += 1
        
        # Calculate proportions
        total = sum(emotion_counts.values())
        if total > 0:
            emotion_scores = {emotion: count/total for emotion, count in emotion_counts.items()}
        else:
            emotion_scores = {emotion: 0 for emotion in emotion_counts}
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        if dominant_emotion == 0:
            dominant_emotion = "neutral"
            
        return {
            "scores": emotion_scores,
            "dominant_emotion": dominant_emotion
        }
    
    def analyze_sentence_level(self, sentences):
        """Analyze emotions at the sentence level."""
        sentence_emotions = []
        
        for sentence in sentences:
            if not sentence.strip():
                continue
                
            sentiment = self.analyze_sentiment(sentence)
            emotions = self.analyze_emotions(sentence)
            
            sentence_emotions.append({
                "sentence": sentence,
                "sentiment": sentiment,
                "emotions": emotions
            })
            
        return sentence_emotions
    
    def analyze_paragraph_level(self, paragraphs):
        """Analyze emotions at the paragraph level."""
        paragraph_emotions = []
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
                
            sentiment = self.analyze_sentiment(paragraph)
            emotions = self.analyze_emotions(paragraph)
            
            # Get sentence-level analysis for this paragraph
            sentences = sent_tokenize(paragraph)
            sentence_analysis = self.analyze_sentence_level(sentences)
            
            paragraph_emotions.append({
                "paragraph": paragraph,
                "sentiment": sentiment,
                "emotions": emotions,
                "sentence_analysis": sentence_analysis
            })
            
        return paragraph_emotions
    
    def analyze_document(self, text):
        """Analyze the entire document for emotional tone."""
        # Preprocess the text
        preprocessed = self.preprocess_text(text)

        # Split into paragraphs
        paragraphs = text.split('\n\n')
        paragraphs = [p for p in paragraphs if p.strip()]

        # Analyze at different levels
        document_sentiment = self.analyze_sentiment(text)
        document_emotions = self.analyze_emotions(text)
        sentence_analysis = self.analyze_sentence_level(preprocessed["sentences"])
        paragraph_analysis = self.analyze_paragraph_level(paragraphs)

        # Track emotional shifts and consistency
        emotional_shifts = self._detect_emotional_shifts(sentence_analysis)
        consistency_check = self._check_emotional_consistency(paragraph_analysis)
        
        return {
            "document_sentiment": document_sentiment,
            "document_emotions": document_emotions,
            "sentence_analysis": sentence_analysis,
            "paragraph_analysis": paragraph_analysis,
            "emotional_shifts": emotional_shifts,
            "consistency_check": consistency_check
        }
    
    def _detect_emotional_shifts(self, sentence_analysis):
        """Detect significant shifts in emotional tone between sentences."""
        shifts = []

        if len(sentence_analysis) < 2:
            return shifts

        for i in range(1, len(sentence_analysis)):
            prev_dominant = sentence_analysis[i-1]["emotions"]["dominant_emotion"]
            curr_dominant = sentence_analysis[i]["emotions"]["dominant_emotion"]

            if prev_dominant != curr_dominant:
                shifts.append({
                    "position": i,
                    "from_sentence": sentence_analysis[i-1]["sentence"],
                    "to_sentence": sentence_analysis[i]["sentence"],
                    "from_emotion": prev_dominant,
                    "to_emotion": curr_dominant
                })
    
        return shifts
    
    def _check_emotional_consistency(self, paragraph_analysis):
        """Check for consistency in emotional tone across paragraphs."""
        if not paragraph_analysis:
            return {"is_consistent": True, "inconsistencies": []}
    
        dominant_emotions = [p["emotions"]["dominant_emotion"] for p in paragraph_analysis]
        main_emotion = max(set(dominant_emotions), key=dominant_emotions.count)

        inconsistencies = []
        for i, paragraph in enumerate(paragraph_analysis):
            if paragraph["emotions"]["dominant_emotion"] != main_emotion:
                inconsistencies.append({
                    "paragraph_index": i,
                    "paragraph": paragraph["paragraph"],
                    "emotion": paragraph["emotions"]["dominant_emotion"],
                    "main_emotion": main_emotion
                })
                
        return {
            "is_consistent": len(inconsistencies) == 0,
            "main_emotion": main_emotion,
            "inconsistencies": inconsistencies
        }
    
    def visualize_emotional_arc(self, analysis_result):
        """Create a visualization of the emotional arc throughout the text."""
        # Extract emotions from sentence analysis
        emotions = [s["emotions"]["dominant_emotion"] for s in analysis_result["sentence_analysis"]]
    
        # Count occurrences of each emotion
        emotion_counts = {}
        for emotion in emotions:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1
    
        # Create color mapping for emotions from config
        emotion_colors = EMOTION_COLORS
    
        # Create the emotional arc plot
        plt.figure(figsize=(12, 6))

        # Plot the emotional arc with y-value to show different emotions
        unique_emotions = list(set(emotions))
        y_positions = {emotion: i - (len(unique_emotions) - 1) / 2 for i, emotion in enumerate(unique_emotions)}
    
    
        # # Plot the emotional arc
        # for i, emotion in enumerate(emotions):
        #     plt.scatter(i, 0, color=emotion_colors.get(emotion, 'black'), s=100)
        for i, emotion in enumerate(emotions):
            plt.scatter(i, y_positions[emotion], 
                        color=emotion_colors.get(emotion, 'black'), 
                        s=100)
        
        # Add labels and title
        plt.xlabel('Sentence Position')
        # plt.yticks([])  # Remove y-axis
        plt.ylabel('Emotion')
        plt.title('Emotional Arc Throughout the Text')

        # Set y-ticks to show emotions
        plt.yticks(list(y_positions.values()), list(y_positions.keys()))
        plt.axhline(y=0, color='k', linestyle='--')  # Add a horizontal line at y=0
        
        # Add a legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                          label=emotion, markerfacecolor=color, markersize=10)
                          for emotion, color in emotion_colors.items() 
                          if emotion in emotion_counts]
        plt.legend(handles=legend_elements, loc='upper right')
        
        # Save or display the plot
        plt.tight_layout()
        return plt
    
    def create_emotion_radar_chart(self, analysis_result):
        """Create a radar chart visualization of emotions throughout the text."""
        # Get sentence-level emotions for radar chart
        emotions_data = []
        for sentence in analysis_result["sentence_analysis"]:
            emotion_scores = sentence["emotions"]["scores"]
            emotions_data.append({
                "sentence": sentence["sentence"],
                "emotions": emotion_scores
            })

        # Calculate average emotion scores across all sentences
        all_emotions = {}
        for entry in emotions_data:
            for emotion, score in entry["emotions"].items():
                if emotion in all_emotions:
                    all_emotions[emotion].append(score)
                else:
                    all_emotions[emotion] = [score]

        # Calculate averages
        emotion_averages = {emotion: sum(scores)/len(scores) for emotion, scores in all_emotions.items()}
        
        # Create the radar chart
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)
        
        # Get emotion labels and values
        emotions = list(emotion_averages.keys())
        values = [emotion_averages[e] for e in emotions]
        
        # Number of variables
        N = len(emotions)
        
        # What will be the angle of each axis in the plot (divide the plot / number of variables)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # Close the loop
        
        # Add the values for the chart
        values += values[:1]  # Close the loop
        
        # Draw the chart
        ax.plot(angles, values, linewidth=2, linestyle='solid')
        ax.fill(angles, values, alpha=0.4)
        
        # Fix axis to go in the right order and start at 12 o'clock
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Draw axis lines for each angle and label
        plt.xticks(angles[:-1], emotions)
        
        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks([0.25, 0.5, 0.75], ["0.25", "0.5", "0.75"], color="grey", size=8)
        plt.ylim(0, 1)
        
        # Add title
        plt.title("Emotional Distribution", size=14, color='black', y=1.1)
        
        # Return the plot
        return plt

# Example usage function
def analyze_text_emotions(text):
    """Analyze the emotional content of the given text."""
    analyzer = EmotionalToneAnalyzer()
    analysis = analyzer.analyze_document(text)
    
    # Print overall analysis
    print("Document Analysis:")
    print(f"Overall Sentiment: {analysis['document_sentiment']['overall_sentiment']}")
    print(f"Dominant Emotion: {analysis['document_emotions']['dominant_emotion']}")
    
    # Check for consistency
    if not analysis['consistency_check']['is_consistent']:
        print("\nEmotional Inconsistencies Detected:")
        for inconsistency in analysis['consistency_check']['inconsistencies']:
            print(f"- Paragraph {inconsistency['paragraph_index'] + 1} has emotion '{inconsistency['emotion']}' while the main emotion is '{inconsistency['main_emotion']}'")
    
    # Report emotional shifts
    if analysis['emotional_shifts']:
        print("\nEmotional Shifts Detected:")
        for shift in analysis['emotional_shifts']:
            print(f"- Shift from '{shift['from_emotion']}' to '{shift['to_emotion']}' between sentences:")
            print(f"  \"{shift['from_sentence']}\"")
            print(f"  \"{shift['to_sentence']}\"")
    
    # Create visualization
    plot = analyzer.visualize_emotional_arc(analysis)
    plot.show()
    
    return analysis

# If run as a script, provide a simple example
if __name__ == "__main__":
    sample_text = """
    The morning dawned bright and beautiful. Birds sang in the trees and a gentle breeze carried the scent of flowers through the open window.
    
    But as the day wore on, dark clouds gathered on the horizon. The wind picked up, scattering leaves across the yard. The birds fell silent.
    
    By evening, a storm raged outside. Lightning flashed and thunder crashed, shaking the windows. The power went out, leaving the house in darkness.
    
    When morning came again, the storm had passed. Sunlight glinted off raindrops clinging to leaves. A rainbow arched across the sky, promising better days ahead.
    """
    
    analysis_result = analyze_text_emotions(sample_text)
