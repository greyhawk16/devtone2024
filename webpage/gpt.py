from openai import OpenAI
from pydantic import BaseModel
import dotenv
import os
import csv
import random
from .app_class import Problem, Check, Session

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
conversation_archive = []

situations_list = []
with open('./webpage/situation_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        situations_list.append(row[0])
    file.close()

items_list = []
with open('./webpage/items_data.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        items_list.append(row[0])
    file.close()

def openai_conn(prompt):
    client = OpenAI()
    class game_information(BaseModel):
        player_life: int
        situation_discription: str
        option1_description: str
        option2_description: str
        option3_description: str
        option4_description: str

    OpenAI.api_key = OPENAI_API_KEY

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "당신은 텍스트 게임 진행자 입니다."},
            {"role": "user", "content": prompt,"temperature": 0.9}
        ],response_format=game_information,
    )

    information = completion.choices[0].message.parsed

    return information

def start_game(problem: Problem) -> Problem:
    pic_num = random.randint(0, len(situations_list)-1)
    current_situation = situations_list[pic_num]
    selectable_items = random.sample(items_list, k=4)
    payload = f"{current_situation} 상황으로 텍스트 게임을 진행하겠습니다. 플레이어는 살아남기 힘든 상황에 놓여있으며, 체력 {Session.player_life}으로 시작합니다. 이번 위기 상황에는 {selectable_items}를 부가적인 설명 없이 제시해 주십시오. 플레이어는 반드시 1,2,3,4로만 입력해야 합니다. 플레이어가 선택하면 해당 물건을 골랐을 때 주인공의 체력 변화를 알려주십시오. 이때 체력은 최대치 100을 넘을 수 없으며 변화량은 +-90까지 소수점 한자리 단위로 일어날 수 있습니다. 체력 0이 되면 사망으로 게임오버되고, 최종목표를 달성하면 승리하게 됩니다. 바로 구체적인 상황을 생성해주십시오."
    game_info = openai_conn(payload)
    problem.problem_number += 1
    problem.life = game_info.player_life
    problem.description = game_info.situation_discription
    problem.option[0] = selectable_items[0]
    problem.option[1] = selectable_items[1]
    problem.option[2] = selectable_items[2]
    problem.option[3] = selectable_items[3]
    conversation_archive.append(payload)
    conversation_archive.append(game_info.situation_discription)
    return problem

def get_input(check: Check) -> Check:
    payload = f"{check.select_number}, 각 선택지에 따른 생존 확률과, 플레이어의 선택에 따른 결과를 말해 주십시오."
    conversation_archive.append(payload)
    game_info = openai_conn(''.join(i for i in conversation_archive))
    conversation_archive.append(game_info.situation_discription)
    check.option[0] = game_info.option1_description
    check.option[1] = game_info.option2_description
    check.option[2] = game_info.option3_description
    check.option[3] = game_info.option4_description
    return check

def next_level(problem: Problem) -> Problem:
    problem.problem_number += 1
    selectable_items = random.sample(items_list, k=4)
    payload = f"이어지는 상황에 기존의 선택지 대신에 다음 4개의 {selectable_items}들을 제시해주십시오."
    conversation_archive.append(payload)
    game_info = openai_conn(''.join(i for i in conversation_archive))

    problem.life = game_info.player_life
    problem.description = game_info.situation_discription
    problem.option[0] = selectable_items[0]
    problem.option[1] = selectable_items[1]
    problem.option[2] = selectable_items[2]
    problem.option[3] = selectable_items[3]
    #result = openai_conn(''.join(i for i in conversation_archive)).situation_discription
    #conversation_archive.append(result)
    conversation_archive.append(game_info.situation_discription)
    return problem