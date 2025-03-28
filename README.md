# Creative Writing Assistant with Emotional Feedback

A web application that helps writers enhance their creative work by focusing on emotional expression, tone consistency, and overall narrative engagement. Using natural language processing and sentiment analysis, this tool provides actionable feedback to improve the emotional impact of your writing.

## Features

- **Emotional Tone Analysis**: Analyzes text to identify emotional tones (joy, sadness, anger, fear, etc.)
- **Sentiment Visualization**: Visualizes emotional arcs and sentiment distribution through charts
- **Consistency Checking**: Identifies inconsistencies in emotional tone across your text
- **Improvement Suggestions**: Provides specific suggestions to enhance emotional impact, including sentence rewrites

## Getting Started

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/creative-writing-assistant.git
cd creative-writing-assistant
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Download required NLTK data and spaCy model:
```bash
python -m nltk.downloader punkt stopwords
python -m spacy download en_core_web_sm
```

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open a web browser and navigate to:
```
http://127.0.0.1:5000/
```

## Usage

1. Enter or paste your text in the input area
2. Click "Analyze Emotional Tone" to process the text
3. Review the analysis results:
   - Overall sentiment and dominant emotions
   - Emotional arc visualization
   - Emotion radar chart showing distribution of emotions
   - Consistency checks and emotional shifts
4. Select a target emotion and click "Get Suggestions" to receive improvement recommendations

## Project Structure

- `app.py` - Main Flask application
- `sentiment_analysis.py` - Core sentiment analysis module
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files

## Technologies Used

- **Flask**: Web framework
- **NLTK**: Natural Language Processing tasks
- **spaCy**: Advanced NLP for syntactic parsing
- **Transformers**: Sentiment analysis and emotion detection
- **Matplotlib**: Data visualization
- **Bootstrap**: Frontend styling
- **Chart.js**: Interactive charts

## Future Improvements

- Expan
