# EduVoice FR™ - Traduction (NLLB-200)
# Fichier: backend/app/models/translation.py

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import sentencepiece
import logging
from typing import Optional

# --- Config ---
MODEL_NAME = "facebook/nllb-200-distilled-600M"  # Modèle léger pour la traduction
DEVICE = "cpu"  # ou "cuda" si GPU disponible

# --- Charger le modèle et le tokenizer ---
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.to(DEVICE)
    logging.info(f"Modèle NLLB-200 ({MODEL_NAME}) chargé avec succès.")
except Exception as e:
    logging.error(f"Erreur lors du chargement du modèle NLLB-200: {e}")
    tokenizer = None
    model = None

# --- Dictionnaire des langues (NLLB utilise des codes spécifiques) ---
LANG_CODES = {
    "en": "eng_Latn",  # Anglais
    "fr": "fra_Latn",  # Français
}

# --- Fonctions ---
async def translate_text(text: str, source_lang: str = "en", target_lang: str = "fr") -> str:
    """
    Traduit un texte de l'anglais vers le français.
    
    Args:
        text: Texte à traduire.
        source_lang: Langue source (toujours 'en' pour ce projet).
        target_lang: Langue cible (toujours 'fr' pour ce projet).
    
    Returns:
        str: Texte traduit.
    """
    if tokenizer is None or model is None:
        raise RuntimeError("Modèle NLLB-200 ou tokenizer non chargé.")
    
    # Préparer les tokens pour NLLB
    source_code = LANG_CODES.get(source_lang, "eng_Latn")
    target_code = LANG_CODES.get(target_lang, "fra_Latn")
    
    # Ajouter le préfixe de langue pour NLLB
    text_with_prefix = f"{source_code} {text} {target_code}"
    
    # Tokenizer et génération
    inputs = tokenizer(text_with_prefix, return_tensors="pt", padding=True).to(DEVICE)
    outputs = model.generate(
        **inputs,
        max_length=512,
        num_beams=5,
        early_stopping=True,
    )
    
    # Décoder la sortie
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return translated_text

# --- Test ---
if __name__ == "__main__":
    import asyncio
    
    async def test():
        result = await translate_text("Hello, how are you?", source_lang="en", target_lang="fr")
        print(f"Traduction: {result}")
    
    asyncio.run(test())
