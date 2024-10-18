from fastapi import APIRouter, HTTPException, status
# from ai.code.database import database
from pydantic import BaseModel
import pandas as pd
from gpt_communication.gpt_communication import *

router = APIRouter(
    tags=["likedSector"],
    responses={404: {"description" : "Not Found"}},
)


class liked_sector(BaseModel):
    sector: str


def get_news_feed():
    try:
        # CSV 파일 읽기
        csv_file_path = "C:/Users/kth_0/OneDrive/바탕 화면/프로젝트/퀀트/news_feed.csv"  # 실제 csv 파일 경로로 수정
        df = pd.read_csv(csv_file_path)

        # title과 time 열을 딕셔너리로 변환하여 리스트 생성
        news_feed_list = df[['Title', 'Time']].to_dict(orient='records')[-50:]

        return news_feed_list

    except FileNotFoundError:
        raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="CSV 파일을 찾을 수 없습니다."
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"파일을 처리하는 동안 오류가 발생했습니다: {str(e)}"
        )

@router.get("", summary="관심 회사 목록")
async def sectorList():
    """
    관심종목으로 설정한 회사들의 목록을 반환하는 엔드포인트입니다.

    """
    industry_classification = [
        {
            "분류": "기술/정보 기술",
            "세부 항목": ["소프트웨어", "전자제품", "반도체"]
        },
        {
            "분류": "통신 서비스",
            "세부 항목": ["소셜 미디어", "검색 엔진 및 포털", "통신"]
        },
        {
            "분류": "금융",
            "세부 항목": ["은행", "투자", "보험"]
        },
        {
            "분류": "헬스케어",
            "세부 항목": ["제약", "의료 기기", "바이오테크"]
        },
        {
            "분류": "산업재",
            "세부 항목": ["항공/방위", "건설", "운송"]
        },
        {
            "분류": "소비재",
            "세부 항목": ["자동차", "소매", "레저/오락"]
        },
        {
            "분류": "필수 소비재",
            "세부 항목": ["식음료", "가정용품", "유통"]
        },
        {
            "분류": "에너지",
            "세부 항목": ["석유/가스", "신재생에너지"]
        },
        {
            "분류": "소재",
            "세부 항목": ["화학", "철강/금속", "건축 자재"]
        },
        {
            "분류": "유틸리티",
            "세부 항목": ["전력/가스", "물 공급"]
        },
        {
            "분류": "부동산",
            "세부 항목": ["부동산 투자 신탁(REITs)", "개발/건설"]
        },
        {
            "분류": "금속 및 광업",
            "세부 항목": ["광업", "귀금속"]
        }
    ]
    return industry_classification



@router.get("/gpt", summary="관심 회사 정보(GPT)")
async def likedSector(sector = str):
    
    """
    관심종목으로 설정한 회사를 담은 엔드포인트입니다.

    """
    
    gpt_insert_info = {"dict" : get_news_feed(), "item" : sector}
    # gpt_insert_info = get_news_feed()
    systemMessageRaw = "당신은 워런 버핏처럼 뛰어난 실력의 투자자입니다. 당신은 늘 합리적인 선택을 하며, 주가의 등락과 그 폭을 정확하게 예측합니다."
    userMessageRaw =  "당신은 이제부터 '최근 며칠간의 기사 목록'에 대한 dict를 python dictionary로 입력받을 것입니다. \
                    #최근 며칠간의 기사 목록\
                    - {info}\
                    기사 목록에 대한 dictionary는 {{기사 제목 : 기사 작성 시간}}의 형태로 구성되어 있으며 기사 목록을 보고 \
                    '관심종목'의 전망에 대한 당신의 추론과 향후 7일간 가장 주가가 많이 상승할 것 같은 회사 이름 3개를 적고, \
                    그 폭에 대한 당신의 추론을 기사의 내용을 이용해서 json 형태로 답변해 주세요. 그렇게 생각한 이유는 최대한 구체적이게 작성해 주세요.\
                    #예시답변('관심종목' == 게임)\
                    - [['게임', '기사 목록을 살펴본 결과, 최근에 게임 시장의 성장세가 높아지고 있는 가운데, 게임 기업들의 신규 서비스 출시와 성과 향상에 대한 기사가 많아졌습니다. 이러한 분위기 속에서 게임 기업들의 주가가 상승할 것으로 예상됩니다. 따라서, 향후 7일간 가장 주가가 많이 상승할 것으로 예상되는 기업 3곳은 '넥슨', '넷마블', '네오위즈'로 예상됩니다.']\
                        ['넥슨', '넥슨은 국내 게임 시장에서 지속적으로 선전하고 있으며, 신규 서비스 출시로 인해 수익성이 개선되고 있는 추세다. 게임 시장 성장을 고려할 때, 주가가 7% 이상 증가할 것으로 예상된다.'],\
                        ['네오위즈', '네오위즈는 콘텐츠 다양성과 글로벌 시장 진출을 통해 안정적인 성과를 거두고 있다. 주가가 약 8% 상승할 것으로 전망된다.'],\
                        ['넷마블게임즈', '넷마블게임즈는 모바일 게임 시장에서 강세를 보여왔고, 최근 출시한 신작으로 기대감이 높아 주가 상승이 예상된다. 게임 시장의 성장세를 고려하면 7일 내 주가가 10% 이상 상승할 것으로 예상한다.']]\
                    #당신의 추론('관심종목' == {sectors})\
                    ".format(info = gpt_insert_info["dict"], sectors = gpt_insert_info["item"])
    gpt_raw = gpt_communication(systemmessage=systemMessageRaw, usermessage=userMessageRaw)
    systemMessage = "당신은 훌륭한 문장 인코딩 전문가입니다. 당신은 이제부터 주어진 문장을 정해진 형식에 맞는 json데이터로 변환해야 합니다."
    userMessage =  "- 주어진 문장 : {gptAnswer}\
                    - 정해진 형식 : {{기업이름1 : '선택이유1', 기업이름2 : '선택이유2', 기업이름3 : '선택이유3'}}\
                    정해진 형식에 맞게 주어진 문장에서 관심종목과, 선택한 기업과 이유 3개를 추려내어 json데이터로 변환하세요.\
                    기업이름1~3에는 기업의 이름이, 선택이유1~3에는 선택한 이유가 각각 들어가야 합니다.\
                    정해진 형식 이외에 다른 데이터를 출력하는 것은 금지됩니다. 정해진 형식과 맞지 않는 필요 없는 데이터는 어떠한 경우에도 출력하지 마세요.\
                    단, 이유는 최대한 구체적으로 출력해야 합니다.\
                    json데이터 외에는 아무것도 출력하지 마세요.".format(gptAnswer = gpt_raw)
    gpt = gpt_communication(systemmessage=systemMessage, usermessage=userMessage)
    return {'response' : gpt}

# #예시답변2\
#                     - [['소프트웨어', '기사 목록을 살펴본 결과, 최근 IT 기업들의 기술 혁신과 새로운 제품 출시에 관한 기사가 많이 나왔습니다. 이러한 IT 기업들의 활발한 활동으로 주가가 상승할 것으로 전망됩니다. 또한, 인공지능 및 클라우드 컴퓨팅 분야에 대한 수요가 계속해서 증가하고 있어서 향후 7일간 가장 주가가 많이 상승할 것으로 예상되는 기업 3곳은 '구글', '아마존', '마이크로소프트'로 예상됩니다.']\
#                         ['구글' , '5%', '구글은 최근 인공지능 기술 개발 및 클라우드 컴퓨팅 분야에서 주목을 받고 있으며, 신제품 출시에 대한 긍정적인 반응이 예상됩니다. IT 기업의 성장세를 고려할 때, 주가가 5% 이상 증가할 것으로 전망됩니다.'],\
#                         ['아마존 , '8%', '아마존은 전 세계적으로 온라인 쇼핑 및 클라우드 서비스 시장에서 선두를 달리고 있으며, 최근 신규 사업 분야에 진출하여 성과를 낼 것으로 예상됩니다. 따라서, 향후 7일 내 아마존의 주가가 약 8% 상승할 것으로 예상됩니다.'],\
#                         ['마이크로소프트' , '5%', '최근 마이크로소프트의 클라우드 사업 부문이 성장세를 보이고 있습니다. 글로벌 기업들의 클라우드 이전과 디지털 전환을 통해 수익성이 향상되고 있는 경향이 강조되는 것으로 보아 주가가 5% 이상 증가할 것으로 전망됩니다.'],\
                    
        