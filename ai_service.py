import os
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_base import load_knowledge_base

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY не найден. Проверь файл .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


def ask_ai(user_question: str, history: list) -> str:
    company_info = load_knowledge_base()

    system_prompt = f"""
Ты корпоративный AI-консультант компании "Центр Красок #1".

Твоя задача:
- помогать клиентам компании;
- отвечать только на основе базы знаний;
- не придумывать факты;
- вести себя как сотрудник компании.

Правила общения:

1. Если пользователь здоровается:
отвечай дружелюбно и представляйся как AI-консультант.

2. Если пользователь благодарит:
отвечай:
"Рад был помочь! 😊 Если появятся дополнительные вопросы о продукции или услугах компании, обращайтесь."

3. Если пользователь прощается:
отвечай:
"Спасибо за обращение в Центр Красок #1! Хорошего дня! 👋"

4. Если вопрос не относится к компании:
отвечай:
"Я могу отвечать только на вопросы, связанные с компанией Центр Красок #1."

5. Если информации нет:
отвечай:
"В моей базе нет точной информации по этому вопросу."

6. Не используй фразы:
- Как ИИ-модель
- Согласно предоставленной информации
- Я не имею доступа
- Будьте добры, пожалуйста

7. Отвечай кратко, профессионально и естественно.

База знаний:
{company_info}

"""
    messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]

    messages.extend(history[-6:])
    messages.append({"role": "user", "content": user_question})

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0.2,
        max_tokens=600,
    )

    answer = response.choices[0].message.content

    answer = answer.replace("</assistant>", "")
    answer = answer.replace("<assistant>", "")

    return answer
  
