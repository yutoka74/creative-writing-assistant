"""
Configuration file for the Creative Writing Assistant application.
Contains settings for emotional analysis and suggestion generation.
"""

# OpenAI API settings
OPENAI_MODEL = "gpt-3.5-turbo-instruct"
OPENAI_MAX_TOKENS = 150
OPENAI_TEMPERATURE = 0.7
OPENAI_TOP_P = 1.0
OPENAI_FREQUENCY_PENALTY = 0.0
OPENAI_PRESENCE_PENALTY = 0.0

# Emotion categories
EMOTION_CATEGORIES = [
    "joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"
]

# Emotion-specific word replacements for fallback suggestion generation
EMOTION_WORD_REPLACEMENTS = {
    'joy': {
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
    },
    'sadness': {
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
    },
    'anger': {
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
    },
    'fear': {
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
    },
    'surprise': {
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
    },
    'default': {
        'good': 'fine',
        'bad': 'challenging',
        'happy': 'content',
        'sad': 'thoughtful'
    }
}

# Emotion-specific sentence endings for fallback suggestion generation
EMOTION_SENTENCE_ENDINGS = {
    'joy': ', filling the moment with pure happiness.',
    'sadness': ', leaving a sense of melancholy in the air.',
    'anger': ', fueling a burning frustration.',
    'fear': ', sending a chill down the spine.',
    'surprise': ', completely defying all expectations!',
    'default': '.'
}

# General suggestions for improving emotional expression
EMOTION_GENERAL_SUGGESTIONS = {
    'joy': [
        "Use more positive and uplifting language throughout your text.",
        "Incorporate words that evoke happiness such as 'delighted', 'ecstatic', 'thrilled'.",
        "Describe pleasant sensory experiences like warm sunlight, gentle breezes, or sweet aromas."
    ],
    'sadness': [
        "Use more melancholic and reflective language throughout your text.",
        "Consider words like 'somber', 'wistful', 'longing', 'melancholy'.",
        "Slow down the narrative pace with longer, more flowing sentences."
    ],
    'anger': [
        "Use shorter, more dynamic sentences to convey intensity.",
        "Consider words like 'furious', 'enraged', 'seething', 'burning'.",
        "Use harsh consonant sounds and incorporate metaphors related to fire or storms."
    ],
    'fear': [
        "Build suspense through pacing and ambiguity throughout your text.",
        "Use words like 'dread', 'terrified', 'ominous', 'looming'.",
        "Describe physiological responses to fear (racing heart, shortness of breath)."
    ],
    'surprise': [
        "Use sentence structures that create sudden revelations throughout your text.",
        "Consider words like 'astonished', 'startled', 'unexpected', 'shocked'.",
        "Build up expectations in one direction, then subvert them for dramatic effect."
    ],
    'default': [
        "Consider the emotional tone of your language.",
        "Pay attention to word choice, sentence structure, and pacing.",
        "Ensure consistency in emotional tone throughout your text."
    ]
}

# Visualization settings
EMOTION_COLORS = {
    "joy": "green",
    "sadness": "blue",
    "anger": "red",
    "fear": "purple",
    "surprise": "orange",
    "disgust": "brown",
    "neutral": "gray"
}
