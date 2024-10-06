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
        news_feed_list = df[['Title', 'Time']].to_dict(orient='records')

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
async def likedSector(item: liked_sector):
    """
    관심종목으로 설정한 회사를 담은 엔드포인트입니다.
   
    - **sector**: 종목 이름

    """
    systemMessage = "당신은 워런 버핏처럼 뛰어난 실력의 투자자입니다. 당신은 늘 합리적인 선택을 하며, 주가의 등락과 그 폭을 정확하게 예측합니다."
    userMessage = " 당신은 이제부터 '최근 며칠간의 기사 목록'에 대한 dict와 '예측을 원하는 회사들의 이름'을 담은 list들, \
                    그리고 '해당 회사들의 최근 주가'를 담은 2-dimentional array를 {dict, list, 2-dimensional array}의 형태로 입력받을 것입니다. \
                    기사 목록에 대한 dict는 {기사 제목 : 기사 작성 시간}의 형태로 구성되어 있으며 기사 목록과 같은 시간의 주가 데이터를 \
                    시간 순서대로 분석해서 이 회사들의 향후 주가에 대한 당신의 추론을 \
                    {['예측을 원하는 회사들의 이름 1' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유'], \
                    ['예측을 원하는 회사들의 이름 2', '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유'] ...\
                    , ['예측을 원하는 회사들의 이름 n' , '향후 7일간 변화할 가격의 %', '그렇게 생각한 이유]}의 list를 담은 json 형태로 답변해 주세요. "
    gpt = gpt_communication(systemmessage=systemMessage, usermessage=userMessage)
    return {'response' : gpt}
        