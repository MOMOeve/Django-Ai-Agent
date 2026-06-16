from django.conf import settings
from langchain_openai import ChatOpenAI

def get_openai_model(model="deepseek-v4-flash"):
    return ChatOpenAI(
        model=model,
        temperature=0,
        max_retries=2,
        api_key=settings.DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com"
    )

