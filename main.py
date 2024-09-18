from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from routes.avatar_routes import router
from models.avatar import Base
from utils.utils import engine, get_db
from sqlalchemy.orm import Session
from models.avatar import Avatar

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
    avatar = Avatar(height=height, weight=weight, gender=gender, bmi=(weight / (height / 100) ** 2))  # bmi 계산을 나중에 추가 가능
    db.add(avatar)
    db.commit()  # 데이터베이스에 커밋하여 저장
    db.refresh(avatar)  # 새로 저장된 객체 반환
    return {"height": height, "weight": weight, "gender": gender, "comment": comment}