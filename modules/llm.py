import os
from openai import OpenAI
import streamlit as st
import requests

def get_client(api_key, base_url):
    if not api_key:
        return None
    return OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

def fetch_openrouter_models():
    """Fetches the list of available models from OpenRouter."""
    try:
        response = requests.get("https://openrouter.ai/api/v1/models")
        if response.status_code == 200:
            data = response.json()
            # Sort models by ID for easier searching
            models = sorted([model["id"] for model in data["data"]])
            return models
        else:
            return ["meta-llama/llama-3-8b-instruct:free"] # Fallback
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ["meta-llama/llama-3-8b-instruct:free"] # Fallback

def validate_api_key(api_key, provider="OpenRouter"):
    """Validates the API key by making a test request."""
    if not api_key:
        return False
    
    try:
        if provider == "OpenRouter":
            response = requests.get(
                "https://openrouter.ai/api/v1/auth/key",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            return response.status_code == 200
        elif provider == "Groq":
            # Groq doesn't have a dedicated auth endpoint, try listing models
            client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=api_key)
            client.models.list()
            return True
    except Exception:
        return False
    return False

def stream_chat(messages, model, api_key, base_url="https://openrouter.ai/api/v1", extra_headers=None, temperature=0.7, max_tokens=1024):
    client = get_client(api_key, base_url)
    if not client:
        yield "Error: API Key is missing."
        return

    try:
        # Prepare params
        params = {
            "model": model,
            "messages": messages,
            "stream": True,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        # Add extra headers if provided (e.g. for transforms)
        if extra_headers:
             params["extra_headers"] = extra_headers

        stream = client.chat.completions.create(**params)
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {str(e)}"

def build_system_prompt(tone="Professional", domain="General Assistant", custom_instructions=""):
    base_prompt = f"You are a helpful AI assistant. Your tone should be {tone}. You are an expert in {domain}."
    if custom_instructions:
        base_prompt += f"\n\nAdditional Instructions: {custom_instructions}"
    return base_prompt
