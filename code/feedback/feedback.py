from fastapi import APIRouter, Query
# from ai.code.database import database
from pydantic import BaseModel
from typing import List
from gpt_communication.gpt_communication import *

router = APIRouter(
    tags=["feedback"],
    responses={404: {"description" : "Not Found"}},
)


@router.get("/readInfo", summary="사용자 정보 입력")
async def feedback(info: List[str] = Query(..., description="사용자 정보 목록", max_length=4)):
    
    """
    사용자 정보를 입럭받는 엔드포인트입니다.
    - 형식
        - /readInfo?info=생년월일?info=전공?info=희망직종?info=취업기간
        - 생년월일 : yyyymmdd
        - 전공 : ex)소프트웨어, 기계공학
        - 희망직종 : ex)웹 개발자, 임베디드 개발자, 디자이너
        - 취업기간 : 3개월 : 0.25, 6개월 : 0.5, 1년 : 1, 2년6개월 : 2.5, 3년이상 : 3
        
    """
    print(info)
    gpt_insert_info = {"생년월일" : info[0], "전공" : info[1],"희망직종" : info[2],"취업기간" : info[3]}
    systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 취업 목표와 희망 직무에 맞춰 효과적인 일정을 추천하세요. 
                            사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위)을 순서대로 입력합니다."""
    userMessageRaw =  """
                    [입력 예시]
                    - 생년월일 : 20020202
                    - 전공 : 소프트웨어
                    - 희망직종 : 웹 개발자
                    - 취업 목표 기간: 0.25

                    [출력 예시]
                    1주 차: HTML/CSS 기본 학습 (추천 강의: OOO, 실습: OOO)
                    2주 차: JavaScript 기본 문법 익히기 (OOP, 비동기 처리)
                    3주 차: 프로젝트 1개 만들어 보기 (TODO 리스트 웹 앱)
                    ...
                    10주 차: 면접 준비 (기술 면접, 코딩 테스트 연습)
                    12주 차: 기업 지원 및 최종 점검

                    모든 추천 일정은 실현 가능하도록 구체적으로 작성하세요.
                    
                    [입력]
                    - 생년월일 : {birthday}
                    - 전공 : {major}
                    - 희망직종 : {hope}
                    - 취업 목표 기간: {period}
                    """.format(birthday = gpt_insert_info["생년월일"], major = gpt_insert_info["전공"], hope = gpt_insert_info["희망직종"], period = gpt_insert_info["취업기간"])
                    
                    

    gpt_raw = gpt_communication(systemmessage=systemMessageRaw, usermessage=userMessageRaw)

    return gpt_raw





# @router.get("/readSchedule", summary="사용자 정보 입력")
# async def feedback(schedule: List[str] = Query(..., description="사용자 정의 일정", max_length=4)):
    
#     """
#     사용자 정보를 입럭받는 엔드포인트입니다.
#     - 형식
#         - /readInfo?info=생년월일?info=전공?info=희망직종?info=취업기간
#         - 생년월일 : yyyymmdd
#         - 전공 : ex)소프트웨어, 기계공학
#         - 희망직종 : ex)웹 개발자, 임베디드 개발자, 디자이너
#         - 취업기간 : 3개월 : 0.25, 6개월 : 0.5, 1년 : 1, 2년6개월 : 2.5, 3년이상 : 3
        
#     """
#     print(info)
#     gpt_insert_info = {"생년월일" : info[0], "전공" : info[1],"희망직종" : info[2],"취업기간" : info[3]}
#     systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 취업 목표와 희망 직무에 맞춰 효과적인 일정을 추천하세요. 
#                             사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위)을 순서대로 입력합니다."""
#     userMessageRaw =  """
#                     [입력 예시]
#                     - 생년월일 : 20020202
#                     - 전공 : 소프트웨어
#                     - 희망직종 : 웹 개발자
#                     - 취업 목표 기간: 0.25

#                     [출력 예시]
#                     1주 차: HTML/CSS 기본 학습 (추천 강의: OOO, 실습: OOO)
#                     2주 차: JavaScript 기본 문법 익히기 (OOP, 비동기 처리)
#                     3주 차: 프로젝트 1개 만들어 보기 (TODO 리스트 웹 앱)
#                     ...
#                     10주 차: 면접 준비 (기술 면접, 코딩 테스트 연습)
#                     12주 차: 기업 지원 및 최종 점검

#                     모든 추천 일정은 실현 가능하도록 구체적으로 작성하세요.
                    
#                     [입력]
#                     - 생년월일 : {birthday}
#                     - 전공 : {major}
#                     - 희망직종 : {hope}
#                     - 취업 목표 기간: {period}
#                     """.format(birthday = gpt_insert_info["생년월일"], major = gpt_insert_info["전공"], hope = gpt_insert_info["희망직종"], period = gpt_insert_info["취업기간"])
                    
                    

#     gpt_raw = gpt_communication(systemmessage=systemMessageRaw, usermessage=userMessageRaw)

#     return gpt_raw

