from fastapi import APIRouter, Query
# from ai.code.database import database
from typing import List
from gpt_communication.gpt_communication import *
import json


router = APIRouter(
    tags=["feedback"],
    responses={404: {"description" : "Not Found"}},
)



@router.get("/readInfo", summary="사용자 정보 입력")
async def feedback(info: List[str] = Query(..., description="사용자 정보 목록", max_length=8)):
    
    """
    사용자 일정 정보를 입럭받는 엔드포인트입니다.
    - 형식
    - /readInfo?info=생년월일?info=전공?info=희망직종?info=취업기간?info=일정제목?info=기간?info=필수일정?info=비고
        - 생년월일 : yyyymmdd
        - 전공 : ex)소프트웨어, 기계공학
        - 희망직종 : ex)웹 개발자, 임베디드 개발자, 디자이너
        - 취업기간 : n년m개월 : nmm ex) 1년2개월: 102, 0년 6개월: 006
        - 일정제목: ex) 웹 개발자 취업 계획
        - 기간 : yyyymmdd-yyyymmdd ex)20250118-20250201
        - 필수일정 : ex) 모의 코딩테스트 1월 31일
        - 비고 : ex) 첫 번째 주에는 책으로 공부할 것임.
        
    """
    gpt_insert_info = {"생년월일": info[0], "전공": info[1], "희망직종": info[2], "취업기간(년)": info[3][0],"취업기간(월)": info[3][1:], "일정제목": info[4], "기간": info[5], "필수일정": info[6], "비고": info[7]}
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
                        - 기간 : 20250118-20250125
                        - 필수적인 일정 : 20250124에 모의 코딩테스트가 있음.
                        - 기타 요청 : 첫 번째 주에는 책으로 공부할 것임.

                    [출력 예시]
                        {{
                        "20250118": "HTML 기본 학습 (추천 도서: OOO, 실습: OOO)",
                        "20250119": "CSS 기본 학습 (추천 도서: OOO, 실습: OOO)",
                        "20250120": "JavaScript 기본 문법 익히기 (OOP, 비동기 처리)",
                        "20250121": "FastAPI를 이용하여 백엔드 기초 익히기(추천 도서: OOO, 실습: OOO)",
                        "20250122": "MySQL로 DB 공부하기(추천 도서: OOO, 실습: OOO)",
                        "20250123": "웹 프로젝트 제작해 보기(추천 도서: OOO, 실습: OOO)",
                        "20250124": "모의 코딩 테스트 및 최종 점검",
                        "20250125": "기업 지원 및 최종 점검"
                        }}

                    모든 추천 일정은 실현 가능하도록 생략 및 중략 없이 모든 날짜마다 구체적으로 작성하세요.
                    [출력 예시]의 형식을 벗어나는 모든 출력은 금지합니다.
                    [입력]
                    - 생년월일 : {birthday}
                    - 전공 : {major}
                    - 희망직종 : {hope}
                    - 취업 목표 기간: {employperiodyear}년 {employperiodmonth}개월
                    - 단기 계획 제목 : {title}
                    - 기간 : {planperiod}
                    - 필수적인 일정 : {necessary}
                    - 기타 요청 : {extra}
                    """.format(birthday = gpt_insert_info["생년월일"], major = gpt_insert_info["전공"], hope = gpt_insert_info["희망직종"], employperiodyear = gpt_insert_info["취업기간(년)"], employperiodmonth = gpt_insert_info["취업기간(월)"], title = gpt_insert_info["일정제목"], planperiod = gpt_insert_info["기간"], necessary = gpt_insert_info["필수일정"], extra = gpt_insert_info["비고"])
                    
                    

    gpt_raw = gpt_communication(systemmessage=systemMessageRaw, usermessage=userMessageRaw)
    gpt_content = gpt_raw.model_dump()["choices"][0]["message"]["content"]
    response = dict()
    print("\n\n\n", gpt_content)
    gpt_content_list = json.loads(gpt_content)
    print(gpt_content_list)
    for key, val in gpt_content_list.items():
        response[key]=val
    
    print(response)
            
    return {"response": response}

