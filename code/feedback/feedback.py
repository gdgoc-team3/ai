from fastapi import APIRouter, Query, Depends
# from ai.code.database import database
from pydantic import BaseModel
from typing import List
from gpt_communication.gpt_communication import *

router = APIRouter(
    tags=["feedback"],
    responses={404: {"description" : "Not Found"}},
)

class SharedData:
    def __init__(self):
        self.data = {}

    def set_value(self, key: str, value: str):
        self.data[key] = value

    def get_value(self, key: str):
        return self.data.get(key, "No Value")
    
    
shared_data = SharedData()  # 전역 객체


def get_shared_data():
    return shared_data

@router.post("/readInfo", summary="사용자 기본 정보 입력")
async def feedback(info: List[str] = Query(..., description="사용자 정보 목록", max_length=4), shared: SharedData = Depends(get_shared_data)):
    
    """
    사용자 기본 정보를 입럭받는 엔드포인트입니다.
    - 형식
        - /readInfo?info=생년월일?info=전공?info=희망직종?info=취업기간
        - 생년월일 : yyyymmdd
        - 전공 : ex)소프트웨어, 기계공학
        - 희망직종 : ex)웹 개발자, 임베디드 개발자, 디자이너
        - 취업기간 : 3개월 : 0.25, 6개월 : 0.5, 1년 : 1, 2년6개월 : 2.5, 3년이상 : 3
        
    """
    print(info)
    shared.set_value("생년월일", info[0])
    shared.set_value("전공", info[1])
    shared.set_value("희망직종", info[2])
    shared.set_value("취업기간", info[3])
    
    return {"message", f"{info} value saved"}





@router.get("/readSchedule", summary="사용자 일정 입력")
async def feedback(schedule: List[str] = Query(..., description="사용자 정의 일정", max_length=4), shared: SharedData = Depends(get_shared_data)):
    
    """
    사용자 일정 정보를 입럭받는 엔드포인트입니다.
    - 형식
        - /readSchedule?schedule=일정제목?schedule=기간?schedule=필수일정?schedule=비고
        - 일정제목: ex) 웹 개발자 취업 계획
        - 기간 : yyyymmdd-yyyymmdd ex)20250118-20250201
        - 필수일정 : ex) 모의 코딩테스트 1월 31일
        - 비고 : ex) 첫 번째 주에는 책으로 공부할 것임.
        
    """
    gpt_insert_info = {"생년월일": shared.get_value("생년월일"), "전공": shared.get_value("전공"), "희망직종": shared.get_value("희망직종"), "취업기간": shared.get_value("취업기간"), "일정제목": schedule[0], "기간": schedule[1], "필수일정": schedule[2], "비고": schedule[3]}
    print(gpt_insert_info)
    systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 일정을 추천하세요. 
                            사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다."""
    userMessageRaw =  """
                    [입력 예시]
                        - 생년월일 : 20020202
                        - 전공 : 소프트웨어
                        - 희망직종 : 웹 개발자
                        - 취업 목표 기간: 0.25
                        - 단기 계획 제목 : 웹 개발자 취업 계획
                        - 기간 : 20250118-20250201
                        - 필수적인 일정 : 20250131에 모의 코딩테스트가 있음.
                        - 기타 요청 : 첫 번째 주에는 책으로 공부할 것임.

                    [출력 예시]
                        [
                        20250118: HTML 기본 학습 (추천 도서: OOO, 실습: OOO),
                        20250119: CSS 기본 학습 (추천 도서: OOO, 실습: OOO),
                        20250120: JavaScript 기본 문법 익히기 (OOP, 비동기 처리),
                        ...
                        20250131: 모의 코딩 테스트 및 최종 점검,
                        20250201: 기업 지원 및 최종 점검
                        ]

                    모든 추천 일정은 실현 가능하도록 구체적으로 작성하세요.
                    [출력 예시]의 형식을 벗어나는 모든 출력은 금지합니다.
                    [입력]
                    - 생년월일 : {birthday}
                    - 전공 : {major}
                    - 희망직종 : {hope}
                    - 취업 목표 기간: {employperiod}
                    - 단기 계획 제목 : {title}
                    - 기간 : {planperiod}
                    - 필수적인 일정 : {necessary}
                    - 기타 요청 : {extra}
                    """.format(birthday = gpt_insert_info["생년월일"], major = gpt_insert_info["전공"], hope = gpt_insert_info["희망직종"], employperiod = gpt_insert_info["취업기간"], title = gpt_insert_info["일정제목"], planperiod = gpt_insert_info["기간"], necessary = gpt_insert_info["필수일정"], extra = gpt_insert_info["비고"])
                    
                    

    gpt_raw = gpt_communication(systemmessage=systemMessageRaw, usermessage=userMessageRaw)

    return gpt_raw

