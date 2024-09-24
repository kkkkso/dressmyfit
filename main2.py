from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from models.avatar import Base, Avatar
from sqlalchemy.orm import Session
from utils.utils import engine, get_db
from schemas.avatar_schemas import AvatarCreate
from fastapi.responses import JSONResponse

app = FastAPI()

# 정적 파일 경로 추가
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/avatar-images", StaticFiles(directory="C:/Users/syk/dressmyfit/avatarImg"), name="avatar-images")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create-avatar", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("create_avatar.html", {"request": request})

# 데이터베이스 초기화
Base.metadata.create_all(bind=engine)

# POST 요청 처리 및 DB 저장
@app.post("/create-avatar")
async def create_avatar(
    height: float = Form(...),
    weight: float = Form(...),
    gender: str = Form(...),
    comment: str = Form(None),
    db: Session = Depends(get_db)
):
    bmi = weight / (height / 100) ** 2
    if bmi < 18.5:
        avatar_img_url = "/avatar-images/m_lvl0.png" if gender == 'man' else "/avatar-images/w_lvl0.png"
    elif 18.5 <= bmi < 25:
        avatar_img_url = "/avatar-images/m_lvl1.png" if gender == 'man' else "/avatar-images/w_lvl1.png"
    elif 25 <= bmi < 30:
        avatar_img_url = "/avatar-images/m_lvl2.png" if gender == 'man' else "/avatar-images/w_lvl2.png"
    else:
        avatar_img_url = "/avatar-images/m_lvl3.png" if gender == 'man' else "/avatar-images/w_lvl3.png"

    avatar = Avatar(height=height, weight=weight, gender=gender, comment=comment, bmi=bmi) 
    db.add(avatar)
    db.commit()
    db.refresh(avatar)
    return JSONResponse(content={"id": avatar.id, "avatar_img_url": avatar_img_url})

@app.get("/avatar/{avatar_id}")
async def get_avatar(avatar_id: int, db: Session = Depends(get_db)):
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar

from sqlalchemy import text

@app.get("/reset-avatars")
async def reset_avatars(db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM avatar_data"))
    db.execute(text("ALTER SEQUENCE avatar_id_seq RESTART START WITH 1"))
    db.commit()
    return {"message": "Avatars table reset and ID sequence restarted."}
