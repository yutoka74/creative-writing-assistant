"""
Module for generating sentence improvement suggestions for creative writing.
Uses GPT-3 when available or falls back to pattern-based approach.
"""

import re
import openai
import os
from dotenv import load_dotenv
from config import (
    OPENAI_MODEL, 
    OPENAI_MAX_TOKENS, 
    OPENAI_TEMPERATURE, 
    OPENAI_TOP_P,
    OPENAI_FREQUENCY_PENALTY,
    OPENAI_PRESENCE_PENALTY,
    EMOTION_WORD_REPLACEMENTS,
    EMOTION_SENTENCE_ENDINGS,
    EMOTION_GENERAL_SUGGESTIONS
)

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_improved_sentence_with_gpt(original, target_emotion, strength="moderate"):
    """
    Use GPT-3 to improve a sentence to better express a specific emotion

    Parameters:
    -----------
    original : str
        The original sentence to improve
    target_emotion : str
        The target emotion (joy, sadness, anger, fear, surprise, disgust)
    strength : str
        The intensity of the emotion (subtle, moderate, strong)

    Returns:
    --------
    str
        The improved sentence
    """
    # Check if API key is available
    if not openai.api_key:
        # Fallback to pattern-based replacement if no API key
        print("OpenAI API key not found. Using fallback sentence improvement method.")
        return generate_improved_sentence_fallback(original, target_emotion)

    prompt = f"""
    Rewrite the following sentence to better express {target_emotion} at a {strength} level of intensity.
    The rewritten sentence should maintain the core meaning but enhance the emotional impact.

    Original sentence: "{original}"

    Rewritten sentence to express {target_emotion}:
    """

    try:
        response = openai.Completion.create(
            model=OPENAI_MODEL,
            prompt=prompt,
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=OPENAI_TEMPERATURE,
            top_p=OPENAI_TOP_P,
            frequency_penalty=OPENAI_FREQUENCY_PENALTY,
            presence_penalty=OPENAI_PRESENCE_PENALTY
        )
        
        improved_text = response.choices[0].text.strip()

        # Clean up the response to remove any leading/trailing quotes
        if improved_text.startswith('"') and improved_text.endswith('"'):
            improved_text = improved_text[1:-1]
        elif improved_text.startswith('"'):
            improved_text = improved_text[1:]
        elif improved_text.endswith('"'):
            improved_text = improved_text[:-1]

        return improved_text
    
    except Exception as e:
        print(f"Error in GPT API call: {e}")
        # Fallback to pattern-based method if API call fails
        return generate_improved_sentence_fallback(original, target_emotion)

def generate_improved_sentence_fallback(original, target_emotion):
    """
    Fallback method for sentence improvement when GPT-3 is unavailable
    Uses a pattern-based approach to enhance emotional expression

    Parameters:
    -----------
    original : str
        The original sentence to improve
    target_emotion : str
        The target emotion

    Returns:
    --------
    str
        The improved sentence using pattern-based replacements
    """
    # Get the appropriate replacements for the target emotion
    if target_emotion in EMOTION_WORD_REPLACEMENTS:
        improvements = EMOTION_WORD_REPLACEMENTS[target_emotion]
    else:
        improvements = EMOTION_WORD_REPLACEMENTS['default']

    # Apply the replacements
    improved = original
    for word, replacement in improvements.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        improved = pattern.sub(replacement, improved)

    # If the sentence didn't change much, add some emotion-specific modifications
    if improved == original or len(set(improved.split()) - set(original.split())) < 2:
        ending = EMOTION_SENTENCE_ENDINGS.get(target_emotion, EMOTION_SENTENCE_ENDINGS['default'])
        improved = improved.rstrip('.') + ending

    return improved

def get_emotion_general_suggestions(target_emotion):
    """
    Generate general suggestions for enhancing a specific emotion in text
    
    Parameters:
    -----------
    target_emotion : str
        The target emotion
        
    Returns:
    --------
    list
        List of suggestion strings
    """
    if target_emotion in EMOTION_GENERAL_SUGGESTIONS:
        return EMOTION_GENERAL_SUGGESTIONS[target_emotion]
    else:
        return EMOTION_GENERAL_SUGGESTIONS['default']
