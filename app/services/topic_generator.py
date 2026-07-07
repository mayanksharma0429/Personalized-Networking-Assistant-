# app/services/topic_generator.py

from transformers import pipeline, set_seed, GenerationConfig
from app.config import MODEL_NAMES

# Reproducibility ke liye random seed fix karna
set_seed(42)

# Module level par GPT-2 pipeline load karna
generator = pipeline("text-generation", model=MODEL_NAMES["topic_generation"])

def generate_topics(themes: list, interests: list) -> list:
    # Themes aur interests ko text mein badalna
    themes_str = ", ".join(themes) if themes else "various topics"
    interests_str = ", ".join(interests) if interests else "learning new things"
    
    # Few-shot prompting: Showing the AI exactly what a conversation starter looks like
    theme = themes[0] if themes else "technology"
    prompt = (
        f"Event: Artificial Intelligence\n"
        f"Starter: How is your company using AI today?\n\n"
        f"Event: Cloud Computing\n"
        f"Starter: What cloud platforms are you currently migrating to?\n\n"
        f"Event: {theme}\n"
        f"Starter:"
    )
    
    # Create a GenerationConfig object to avoid deprecation warnings
    gen_config = GenerationConfig(
        max_new_tokens=50,
        num_return_sequences=3,
        pad_token_id=50256,
        repetition_penalty=1.5,
        no_repeat_ngram_size=2,
        temperature=0.7,
        do_sample=True
    )
    
    # GPT-2 se text generate karna (3 different ideas)
    output = generator(
        prompt, 
        generation_config=gen_config,
        truncation=True,
        clean_up_tokenization_spaces=False
    )
    
    clean_suggestions = []
    for seq in output:
        generated_text = seq["generated_text"]
        new_text = generated_text[len(prompt):].strip()
        
        # We cut it off at the first newline to grab just the single starter sentence
        first_starter = new_text.split('\n')[0].strip()
        
        if first_starter and first_starter not in clean_suggestions:
            clean_suggestions.append(first_starter)
            
    # Fallback questions in case GPT-2 fails to generate 3 unique ones
    fallbacks = [
        f"What brings you to this {theme} event?",
        f"How long have you been interested in {interests[0] if interests else 'this field'}?",
        "Have you attended any similar events recently?"
    ]
    
    while len(clean_suggestions) < 3:
        clean_suggestions.append(fallbacks[len(clean_suggestions)])
        
    return clean_suggestions[:3]
