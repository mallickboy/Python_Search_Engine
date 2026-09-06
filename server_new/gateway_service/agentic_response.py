import re
from google import genai
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL
)

CLIENT = None

def _get_or_create_client():
    """Checks for an existing client or recreates it if it's missing."""
    global CLIENT
    if CLIENT is None:
        # print("Initializing (or re-initializing) Gemini Client...")
        CLIENT = genai.Client(api_key=GEMINI_API_KEY)
    return CLIENT

async def get_gemini_response(prompt):
    global CLIENT
    try:
        # 1. Get the current client (recreates if CLIENT is None)
        client = _get_or_create_client()
        
        # 2. Attempt the request
        response = client.models.generate_content(
            model=GEMINI_MODEL, 
            contents=prompt
        )
        return response.text
    except Exception as e:
        # print(f"Request failed: {e}")
        CLIENT = None 
        return f"An error occurred: {e}"

def clean_and_normalize(text):
    """Standardizes text to ensure high-quality context."""
    if not text: return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

async def rerank_and_answer_with_gemini(query, search_responses, top_k=10):
    try:
        top_results = search_responses[:top_k]
        
        # Extract and clean descriptions
        context_list = [f"- {clean_and_normalize(item.get('desc', ''))}" for item in top_results]
        context_text = "\n".join(context_list)
        
        if not context_text:
            return "No valid search descriptions available to answer."

        prompt = f"""
        Answer the user query strictly using only the provided context descriptions. 
        Do not add outside information.

        Constraint: Keep your answer concise, between 200 and 400 characters.

        User Query: {query}

        Context Descriptions:
        {context_text}
        """

        return await get_gemini_response(prompt)
    
    except Exception as e:
        print(f"Reranking error: {e}")
        return None