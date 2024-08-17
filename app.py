from openai import OpenAI
import dotenv
import os
import csv
import random


dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
conversation_archive = []
MAX_ITER = 3


situations_list = []
with open('situation_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        situations_list.append(row[0])
    file.close()


items_list = []
with open('items_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        items_list.append(row[0])
    file.close()


current_situation = situations_list[random.randint(0, len(situations_list))]
selectable_items = random.sample(items_list, k=4)


def openai_conn(prompt):
    client = OpenAI()
    OpenAI.api_key = OPENAI_API_KEY

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 텍스트 게임 진행자 입니다."},
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )

    res = completion.choices[0].message.content
    return res


def select_1_from_4(selection):
    if selection in [1, 2, 3, 4]:
        return selection
    else:
        return False    # 재입력 요구
    


payload = f"{current_situation} 상황으로 텍스트 게임을 진행하겠습니다. 플레이어는 살아남기 힘든 상황에 놓여있으며, 체력 100으로 시작합니다. 위기 상황이 찾아오면 {selectable_items}를 제시해 주십시오. 그리고 해당 물건에 대한 1줄 이내의 간략한 설명을 해주십시오. 플레이어는 반드시 1,2,3,4로만 입력해야 합니다. 플레이어가 선택하면 해당 물건을 골랐을 때 주인공의 체력 변화를 알려주십시오. 이때 체력 변화는 최대치 100을 넘을 수 없으며 +-90까지 소수점 한자리 단위로 일어날 수 있습니다. 체력 0이 되면 사망으로 게임오버되고, 최종목표를 달성하면 승리하게 됩니다. 바로 구체적인 상황을 생성해주십시오."
result_1 = openai_conn(payload)

conversation_archive.append(payload)
conversation_archive.append(result_1)

print(result_1)


i = 0
while i < MAX_ITER:
    user_input = input("위기 상황이 찾아왔습니다. 선택할 물건의 번호를 입력해 주십시오: ")
    user_input = select_1_from_4(int(user_input))
    payload_2 = f"{user_input}, 이어지는 상황의 선택지로 {selectable_items} 를 제시해주십시오."

    conversation_archive.append(payload_2)
    result_2 = openai_conn(''.join(i for i in conversation_archive))
    conversation_archive.append(result_2)
    print(result_2)
    i += 1