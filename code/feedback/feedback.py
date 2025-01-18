from fastapi import APIRouter, Query, HTTPException, status
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
    # systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 매일의 일정을 시간별로 추천하세요. 
    #                         사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다."""
    userMessageRaw =  """
                    당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 매일의 일정을 시간별로 추천하세요. 
                    사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다.
                            
                    [입력 예시]
                        - 생년월일 : 20020202
                        - 전공 : 소프트웨어
                        - 희망직종 : 웹 개발자
                        - 취업 목표 기간: 0.25
                        - 단기 계획 제목 : 웹 개발자 취업 계획
                        - 기간 : 20250118-20250120
                        - 필수적인 일정 : 20250124에 모의 코딩테스트가 있음.
                        - 기타 요청 : 첫 번째 주에는 책으로 공부할 것임.

                    [출력 예시]
                        {{
                          tasks: [
                                    {{
                                        title: “HTML+CSS+JS 책 읽기”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 10,
                                            minute : 00
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 13,
                                            minute : 30
                                        }}
                                    }},
                                    {{
                                        title: “인프런 강좌 시청”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 14,
                                            minute : 00
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 17,
                                            minute : 00
                                        }}
                                    }},
                                    {{
                                        title: “배운 내용 복습”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 17,
                                            minute : 30
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 18
                                            hour : 21,
                                            minute : 00
                                        }}
                                    }},
                                    {{
                                        title: “어제 학습한 내용 실습”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 19
                                            hour : 10,
                                            minute : 00
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 19
                                            hour : 15,
                                            minute : 00
                                        }}
                                    }},
                                    {{
                                        title: “실습한 내용 바탕으로 게시판 프로젝트 제작”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 19
                                            hour : 16,
                                            minute : 00
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 19
                                            hour : 21,
                                            minute : 00
                                        }}
                                    }},
                                    {{
                                        title: “어제 만들던 게시판 프로젝트 완성”,
                                        startDate: {{
                                            year: 2025
                                            month : 1
                                            day : 20
                                            hour : 10,
                                            minute : 00
                                        }},
                                        endDate: {{
                                            year: 2025
                                            month : 1
                                            day : 19
                                            hour : 21,
                                            minute : 00
                                        }}
                                    }},
                                ]

                        }}

                    모든 추천 일정은 실현 가능하도록 생략 및 중략 없이 모든 날짜마다 구체적으로 작성하세요.
                    [출력 예시]의 형식을 벗어나는 모든 출력은 금지합니다.
                    하루 일정은 시작 시작 10시 끝나는 시간 21시를 준수해 주세요.
                    또한 매일매일 같은 일정을 설정하는 것을 금지합니다.
                    title 항목은 한국어로 작성해 주세요.
                    json 형식으로 반환해 주세요.
                    
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
                    
                    

    gpt_raw = gpt_communication(systemmessage=None, usermessage=userMessageRaw)
    gpt_content = gpt_raw.model_dump()["choices"][0]["message"]["content"]
    
    # # ` ```json ` 및 ` ``` ` 제거
    # cleaned_content = gpt_content.replace("```json", "").replace("```", "").strip()
    print(gpt_content)
# 문자열을 JSON으로 변환
    json_data = json.loads(gpt_content)
    print("\n\n\n", json_data)
    
        
    return json_data


@router.get("/evaluateSchedule", summary="입력된 일정 평가")
async def feedback(tasks: List[str] = Query(..., description="실제 이행 목록"), isChecked: List[bool] = Query(..., description="실제 이행 여부")):
    
    """
    실제 사용자가 이행한 일정을 평가하는 엔드포인트입니다.
    - 형식
    - /evaluateSchedule?tasks=xxx?tasks=yyy?tasks=zzz?isChecked=True?isChecked=False?isChecked=True
        - task : ex) 기초 PHP 문법 공부, 실습한 내용 바탕으로 게시판 프로젝트 제작 등
        - isChecked : True / False
        
    """
    if len(tasks) != len(isChecked):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task와 isChecked의 길이가 다름."
        )
    gpt_insert_info = dict()
    for i in range(len(tasks)):
        gpt_insert_info[tasks[i]] = isChecked[i]
    
    print(gpt_insert_info)
    # systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 매일의 일정을 시간별로 추천하세요. 
    #                         사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다."""
    userMessageRaw =  """
                    당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 당신이 추천했던 일정의 이행 결과를 평가하세요. 
                    사용자는 당신이 추천했던 일정과 이행여부를 순서대로 입력할 것입니다.
                            
                    [입력 예시]
                        -{{'인프런 강좌 시청':True, '어제 공부했던 내용 실습':True, '오늘 공부한 내용 복습':False, '프로젝트 계획서 작성':False}}

                    [출력 예시]
                    
                    {{'tasks':'📊 당신의 학습 이행률을 평가했습니다.

                    🎯 이행 점수: 50점 (2/4 완료)

                    ✅ 완료한 일정 (성공)
                    - 인프런 강좌 시청
                    - 어제 공부했던 내용 실습

                    ❌ 미이행 일정 (개선 필요)
                    - 오늘 공부한 내용 복습 → 하루 10분이라도 복습해 보세요!
                    - 프로젝트 계획서 작성 → 간단한 개요라도 먼저 정리해보면 좋습니다.

                    💡 오늘의 피드백
                    오늘 목표의 절반을 달성했어요! 하지만 복습과 프로젝트 진행은 꾸준함이 중요합니다.  
                    내일은 조금 더 집중해서 목표를 70% 이상 달성하는 것을 목표로 해보세요!  
                    작은 습관이 큰 성장을 만듭니다. 화이팅! 🚀'}}
                    


                    --------------------------------------------------------
                    [출력 예시]의 형식을 벗어나는 모든 출력은 금지합니다.
                    json형식으로 답변해 주세요.
                    
                    
                    [입력]
                    - {dictionary}
                    """.format(dictionary = gpt_insert_info)
                    
                    

    gpt_raw = gpt_communication(systemmessage=None, usermessage=userMessageRaw)
    gpt_content = gpt_raw.model_dump()["choices"][0]["message"]["content"]

    print("\n\n\n", gpt_content)
    
            
    return json.loads(gpt_content)


@router.get("/manageTeam", summary="비슷한 일정끼리 묶기")
async def feedback(schedule: str):
    
    """
    일정을 입력받으면 시스템 개발자 취업 준비, 임베디드 개발자 취업 준비, 인공지능 개발자 취업 준비, 
    웹 개발자 취업 준비, 디자이너 취업 준비, 웹 스터디, 인공지능 스터디, 임베디드 스터디, 프로젝트 준비, 
    디자인 스터디 중 가장 가깝다고 판단되는 항목을 반환하는 엔드포인트입니다.
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
    # systemMessageRaw = """  당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 매일의 일정을 시간별로 추천하세요. 
    #                         사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다."""
    userMessageRaw =  """
                    당신은 취업 컨설턴트 AI입니다. 사용자의 정보와 희망 직무에 맞춰 효과적인 매일의 일정을 시간별로 추천하세요. 
                    사용자는 생년월일, 전공, 희망직종, 취업 목표 기간(년 단위), 단기 계획 제목, 목표 달성 기간, 필수적인 일정, 기타 요청을 순서대로 입력합니다.
                            
                    [입력 예시]
                        - 생년월일 : 20020202
                        - 전공 : 소프트웨어
                        - 희망직종 : 웹 개발자
                        - 취업 목표 기간: 0.25
                        - 단기 계획 제목 : 웹 개발자 취업 계획
                        - 기간 : 20250118-20250120
                        - 필수적인 일정 : 20250124에 모의 코딩테스트가 있음.
                        - 기타 요청 : 첫 번째 주에는 책으로 공부할 것임.

                    [출력 예시]


                    모든 추천 일정은 실현 가능하도록 생략 및 중략 없이 모든 날짜마다 구체적으로 작성하세요.
                    [출력 예시]의 형식을 벗어나는 모든 출력은 금지합니다.
                    하루 일정은 시작 시작 10시 끝나는 시간 21시를 준수해 주세요.
                    또한 매일매일 같은 일정을 설정하는 것을 금지합니다.
                    title 항목은 한국어로 작성해 주세요.
                    
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
                    
                    

    gpt_raw = gpt_communication(systemmessage=None, usermessage=userMessageRaw)
    gpt_content = gpt_raw.model_dump()["choices"][0]["message"]["content"]

    print("\n\n\n", gpt_content)
    
            
    return {gpt_content}

