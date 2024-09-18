from pydantic import BaseModel, Field

class AvatarCreate(BaseModel):
    height: float = Field(..., gt=0, description="Height must be greater than 0")
    weight: float = Field(..., gt=0, description="Weight must be greater than 0")
    gender: str = Field(..., description="Gender is required")
