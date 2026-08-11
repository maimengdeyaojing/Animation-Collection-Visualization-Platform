from fastapi import APIRouter
from fastapi import HTTPException

from sqlalchemy import func

from datetime import datetime
from app.database import SessionLocal
from app.models.anime import AnimeCollection

import requests

router = APIRouter()

CLIENT_ID = "bgm63556a30fef6e8765"
CLIENT_SECRET = "37f9dbd5fe3a785951de4313ee8c163c"

REDIRECT_URI = (
    "http://localhost:5173/oauth/callback"
)

# 用授权码换 access_token
@router.post("/token")
def get_token(code: str):

    url = (
        "https://bgm.tv/oauth/access_token"
    )

    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(
        "https://bgm.tv/oauth/access_token",
        data=payload,
        headers={
            "User-Agent": "AnimeProject/1.0"
        }
    )


    print("状态码:", response.status_code)
    print("返回内容:", response.text)

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=response.text
        )

    return response.json()

# 获取当前登录的 Bangumi 用户信息
@router.get("/me")
def get_me(token: str):

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "AnimeProject/1.0"
    }

    response = requests.get(
        "https://api.bgm.tv/v0/me",
        headers=headers
    )

    print(response.text)

    return response.json()


# 获取某个用户的动画收藏列表
@router.get("/collections/{username}")
def get_collections(
    username: str,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "AnimeProject/1.0"
    }

    all_data = []

    offset = 0

    while True:

        response = requests.get(
            f"https://api.bgm.tv/v0/users/{username}/collections",
            headers=headers,
            params={
                "subject_type": 2,
                "limit": 30,
                "offset": offset
            }
        )

        result = response.json()

        data = result["data"]

        all_data.extend(data)

        if len(data) < 30:
            break

        offset += 30

    return all_data

# 把 Bangumi 收藏同步到你自己的数据库
@router.post("/sync")
def sync_bangumi(
    username: str,
    token: str
):

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "AnimeProject/1.0"
    }

    all_data = []

    offset = 0

    while True:

        response = requests.get(
            f"https://api.bgm.tv/v0/users/{username}/collections",
            headers=headers,
            params={
                "subject_type": 2,
                "limit": 30,
                "offset": offset
            }
        )

        result = response.json()

        data = result["data"]

        all_data.extend(data)

        if len(data) < 30:
            break

        offset += 30

    db = SessionLocal()

    try:

        # 清空旧数据
        db.query(AnimeCollection).delete()

        db.commit()

        for item in all_data:

            subject = item["subject"]

            title = (
                subject.get("name_cn")
                or subject.get("name")
            )

            date_str = subject.get("date")

            anime_date = None
            year = None
            month = None

            if date_str:

                try:

                    anime_date = datetime.strptime(
                        date_str,
                        "%Y-%m-%d"
                    ).date()

                    year = anime_date.year
                    month = anime_date.month

                except:

                    pass

            image_url = (
                subject.get("images", {})
                .get("large")
            )

            anime = AnimeCollection(
                title=title,
                date=anime_date,
                year=year,
                month=month,
                image_url=image_url,
                status=item["type"]
            )

            db.add(anime)

        db.commit()

        return {
            "message": "同步成功",
            "count": len(all_data)
        }

    finally:

        db.close()
# 从你自己的数据库里统计“想看 / 看过 / 在看”数量
@router.get("/stats")
def get_stats():

    db = SessionLocal()

    try:

        wish = (
            db.query(AnimeCollection)
            .filter(
                AnimeCollection.status == 1
            )
            .count()
        )

        completed = (
            db.query(AnimeCollection)
            .filter(
                AnimeCollection.status == 2
            )
            .count()
        )

        doing = (
            db.query(AnimeCollection)
            .filter(
                AnimeCollection.status == 3
            )
            .count()
        )

        return {
            "wish": wish,
            "completed": completed,
            "doing": doing
        }

    finally:

        db.close()