import openai
from dotenv import load_dotenv
import os


def gpt_communication(systemmessage, usermessage):
    # OpenAI API 키 설정

    # load .env
    load_dotenv()

    gpt_key = os.environ.get('API_KEY')
    openai.api_key = gpt_key

    # GPT-4 모델에 요청 보내기
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": systemmessage},
            {"role": "user", "content": usermessage},
        ]
    )

    # 응답 출력
    print(response)
    return response
