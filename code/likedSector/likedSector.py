from fastapi import APIRouter, HTTPException, status
# from ai.code.database import database
from pydantic import BaseModel
import pandas as pd
from gpt_communication.gpt_communication import *

router = APIRouter(
    tags=["likedSector"],
    responses={404: {"description" : "Not Found"}},
)


# class liked_sector(BaseModel):
#     sector: str


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
        
@router.post("", summary="관심 회사 정보")
async def likedSector():
    """
    관심종목으로 설정한 회사를 담은 엔드포인트입니다.
   
    - **sector**: 종목 이름

    """
    skb_sample_data = [
                        {'2024-09-01': 60000},{'2024-09-02': 59023},{'2024-09-03': 59714},{'2024-09-04': 60358},{'2024-09-05': 60218},{'2024-09-06': 60340},{'2024-09-07': 60537},
                        {'2024-09-08': 60880},{'2024-09-09': 59407},{'2024-09-10': 59364},{'2024-09-11': 60616},{'2024-09-12': 59322},{'2024-09-13': 60488},{'2024-09-14': 61890},
                        {'2024-09-15': 61476},
                        {'2024-09-16': 61737},
                        {'2024-09-17': 61843},
                        {'2024-09-18': 61185},
                        {'2024-09-19': 61326},
                        {'2024-09-20': 62785},
                        {'2024-09-21': 63540},
                        {'2024-09-22': 64050},
                        {'2024-09-23': 63913},
                        {'2024-09-24': 62676},
                        {'2024-09-25': 63270},
                        {'2024-09-26': 64446},
                        {'2024-09-27': 64550},
                        {'2024-09-28': 64410},
                        {'2024-09-29': 63502},
                        {'2024-09-30': 64599},
                        {'2024-10-01': 64383},
                        {'2024-10-02': 65696},
                        {'2024-10-03': 66986},
                        {'2024-10-04': 66906},
                        {'2024-10-05': 68170},
                        {'2024-10-06': 68269},
                        {'2024-10-07': 67890},
                        {'2024-10-08': 68102},
                        {'2024-10-09': 67717},
                        {'2024-10-10': 66750}
                    ]


    # gpt_insert_info = {"dict" : get_news_feed(), "item" : item, "array": skb_sample_data}
    gpt_insert_info = get_news_feed()
    systemMessage = "당신은 워런 버핏처럼 뛰어난 실력의 투자자입니다. 당신은 늘 합리적인 선택을 하며, 주가의 등락과 그 폭을 정확하게 예측합니다."
    userMessage =  "당신은 이제부터 '최근 며칠간의 기사 목록'에 대한 dict를 python dictionary로 입력받을 것입니다. \
                    기사 목록에 대한 dictionary는 {{기사 제목 : 기사 작성 시간}}의 형태로 구성되어 있으며 기사 목록을 보고 \
                    향후 7일간 가장 많이 주가가 상승할 것 같은 회사의 이름 5개를 적고, 그 폭에 대한 당신의 100자 이상 200자 이하의 추론을 기사의 내용을 이용해서\
                    json 형태로 답변해 주세요. 그렇게 생각한 이유는 최대한 구체적이게 작성해 주세요.\
                    #답변의 형식\
                    - [['회사의 이름(ex. SKTelecom)' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유(100자이상)'],\
                       ['회사의 이름(ex. 대한항공)' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유(100자이상)'],\
                       ['회사의 이름(ex. LG화학)' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유(100자이상)'],\
                       ['회사의 이름(ex. 삼성전자)' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유(100자이상)'],\
                       ['회사의 이름(ex. 두산중공업)' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유(100자이상)'],\
                    #주어진 정보\
                    - {info}".format(info = gpt_insert_info)
    gpt = gpt_communication(systemmessage=systemMessage, usermessage=userMessage)
    return {'response' : gpt}
        