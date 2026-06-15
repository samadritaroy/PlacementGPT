"""
LLM Service — Groq API (replaces local Ollama)
Llama3 at 300+ tokens/second. Free. No GPU needed.
DROPS IN to replace your existing ask_llama() calls.
"""

import os
import logging
from typing import List, Optional, Generator
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# ── Groq Client ──────────────────────────────────────────────────────────────
_client = None

def get_groq_client() -> Groq:
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set in .env file!")
        _client = Groq(api_key=api_key)
    return _client


# ── Model Options (all free on Groq) ─────────────────────────────────────────
MODELS = {
    "fast":    "llama-3.1-8b-instant",      # ~1s response, good quality
    "smart":   "llama-3.3-70b-versatile",   # ~3s response, best quality  
    "code":    "llama-3.1-8b-instant",      # for DSA/coding questions
    "mixtral": "mixtral-8x7b-32768",        # alternative, great for reasoning
}

DEFAULT_MODEL = MODELS["fast"]


# ══════════════════════════════════════════════
# MAIN FUNCTION — Drop-in replacement for ask_llama()
# ══════════════════════════════════════════════
def ask_llm(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = None,
    temperature: float = 0.3,
    max_tokens: int = 1000
) -> str:
    """
    Send a prompt to Groq and return the response.
    This REPLACES your existing ask_llama() function.
    
    If you had:  answer = ask_llama(prompt)
    Replace with: answer = ask_llm(prompt)
    """
    client = get_groq_client()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    try:
        response = client.chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        if "api_key" in str(e).lower():
            return "Error: Invalid GROQ_API_KEY. Check your .env file."
        return f"Error generating response: {str(e)}"


# ══════════════════════════════════════════════
# MULTI-TURN — For interview chat with history
# ══════════════════════════════════════════════
def ask_llm_with_history(
    messages: List[dict],
    model: str = None,
    temperature: float = 0.5,
    max_tokens: int = 1000
) -> str:
    """
    Multi-turn chat. Pass full conversation history.
    messages = [{"role": "system"/"user"/"assistant", "content": "..."}]
    """
    client = get_groq_client()
    
    try:
        response = client.chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Groq multi-turn error: {e}")
        return f"Error: {str(e)}"


# ══════════════════════════════════════════════
# STREAMING — Makes responses feel instant
# ══════════════════════════════════════════════
def ask_llm_stream(
    prompt: str,
    system_prompt: Optional[str] = None,
    model: str = None,
    temperature: float = 0.3,
    max_tokens: int = 1500
) -> Generator[str, None, None]:
    """
    Streaming version — yields tokens one by one.
    Use with FastAPI StreamingResponse.
    Tokens appear immediately even for long responses.
    """
    client = get_groq_client()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    try:
        stream = client.chat.completions.create(
            model=model or DEFAULT_MODEL,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=True,    # ← This is the key
        )
        for chunk in stream:
            token = chunk.choices[0].delta.content
            if token:
                yield token
    
    except Exception as e:
        yield f"\nError: {str(e)}"


# ── Backward compat alias (if your other services call ask_llama) ─────────────
ask_llama = ask_llm