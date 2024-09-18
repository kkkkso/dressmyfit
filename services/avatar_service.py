from sqlalchemy.orm import Session
from models.avatar import Avatar

def calculate_bmi(height: float, weight: float) -> float:
    return weight / (height / 100) ** 2

def create_avatar(db: Session, avatar_data):
    bmi = calculate_bmi(avatar_data.height, avatar_data.weight)
    new_avatar = Avatar(
        height=avatar_data.height,
        weight=avatar_data.weight,
        gender=avatar_data.gender,
        bmi=bmi
    )
    db.add(new_avatar)
    db.commit()
    db.refresh(new_avatar)
    return new_avatar
