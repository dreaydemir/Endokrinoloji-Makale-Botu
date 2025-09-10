from typing import List
from openai import OpenAI
from .config import OPENAI_API_KEY, SUMMARY_LANGUAGE

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_TR = (
    "Bir akademik makale özetini Türkçe olarak 3 kısa ve basit madde halinde özetle. "
    "Önemli bulgulara, çalışmanın türüne ve klinik/pratik çıkarımlara odaklan. "
    "Varsa örneklem, yöntem ve kısıtları kısaca belirt."
)
SYSTEM_EN = (
    "Summarize the academic article in English as 3 short bullets. "
    "Focus on key findings, study type, and clinical/practical implications. "
    "Briefly note sample, methods, and limitations if present."
)

def summarize_article(title: str, abstract_html: str) -> str:
    system = SYSTEM_TR if SUMMARY_LANGUAGE.lower().startswith("tr") else SYSTEM_EN
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Title: {title}\nAbstract: {abstract_html}"},
    ]
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=220,
    )
    return resp.choices[0].message.content.strip()
