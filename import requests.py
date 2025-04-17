import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"
model = "openai/gpt-4o-mini"

messages = [
    {
        "role": "system",
        "content": "Відповідай лише у форматі JSON. Приклад: [{\"country\": ..., \"capital\": ..., \"language\": ..., \"currency\": ...}, ...]"
    },
    {
        "role": "user",
        "content": "Наведи 5 різних країн. Для кожної вкажи: country, capital, language (офіційна мова), currency (грошова одиниця)."
    }
]

payload = {
    "model": model,
    "messages": messages,
    "temperature": 0.7,
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=payload)

if response.ok:
    try:
        data = json.loads(response.json()["choices"][0]["message"]["content"])
        with open("countries.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("Збережено у файл countries.json")
    except json.JSONDecodeError:
        print("Не вдалося розпізнати JSON:\n", response.text)
else:
    print("Помилка:", response.status_code, response.text)
