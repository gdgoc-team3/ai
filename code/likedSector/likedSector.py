from fastapi import APIRouter, HTTPException, status, Header
from ai.code.database import database
from typing import Optional
from pydantic import BaseModel

router = APIRouter(
    tags=["profile"],
    responses={404: {"description" : "Not Found"}},
)


class liked_sector(BaseModel):
    sector: str


@router.post("", summary="관심 회사 정보")
async def likedSector(item: liked_sector):
    """
    관심종목으로 설정한 회사를 담은 엔드포인트입니다.
   
    - **company**: 글 ID

    """
    print("데이터 조회 시작")
    
    try:
        query = "SELECT * FROM bookmark WHERE user_id = %s AND post_id = %s AND post_type = %s"
        params = (userId, item.postID, item.postType)
        # 쿼리 실행
        result = await database.execute_query(query, params)

        if len(result) == 0:
            query = "INSERT INTO bookmark (user_id, post_id, post_type) VALUES (%s, %s, %s)"
            params = (userId, item.postID, item.postType)
            await database.execute_query(query, params)
            return {"message": "Bookmarked successfully"}
        else:
            query = "DELETE FROM `bookmark` WHERE user_id = %s AND post_id = %s AND post_type = %s"
            params = (userId, item.postID, item.postType)
            await database.execute_query(query, params)
            return {"message": "Bookmarked contents removed successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="예상치 못한 오류가 발생했습니다."
        )