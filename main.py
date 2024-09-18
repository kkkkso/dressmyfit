from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.avatar_routes import router
from models.avatar import Base
from utils.utils import engine, get_db
from sqlalchemy.orm import Session
from models.avatar import Avatar
from schemas.avatar_schemas import AvatarCreate

app = FastAPI()
app.include_router(router)
app.mount("/static", StaticFiles(directory="static"), name="static")
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
    db: Session = Depends(get_db)  # DB 세션 종속성 추가
):
    # Avatar 데이터베이스 모델에 데이터 저장
    avatar = Avatar(height=height, weight=weight, gender=gender, bmi=(weight / (height / 100) ** 2)) 
    db.add(avatar)
    db.commit()  # 데이터베이스에 커밋하여 저장
    db.refresh(avatar)  # 새로 저장된 객체 반환
    return {"height": height, "weight": weight, "gender": gender, "comment": comment}

@router.post("/create-avatar/")
def create_new_avatar(avatar: AvatarCreate, db: Session = Depends(get_db)):
    if not avatar.height or not avatar.weight or not avatar.gender:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    return create_avatar(db, avatar)

@app.get("/avatar/{avatar_id}")
async def get_avatar(avatar_id: int, db: Session = Depends(get_db)):
    avatar = db.query(Avatar).filter(Avatar.id == avatar_id).first()  # id로 아바타 검색
    if not avatar:
        raise HTTPException(status_code=404, detail="Avatar not found")
    return avatar

from sqlalchemy import text

@app.get("/reset-avatars")
async def reset_avatars(db: Session = Depends(get_db)):
    # 테이블의 모든 데이터 삭제 (테이블 자체는 남아있는 것)
    db.execute(text("DELETE FROM avatar_data"))
    # Oracle에서 시퀀스를 1로 리셋
    db.execute(text("ALTER SEQUENCE avatar_id_seq RESTART START WITH 1"))
    db.commit()
    return {"message": "Avatars table reset and ID sequence restarted."}
