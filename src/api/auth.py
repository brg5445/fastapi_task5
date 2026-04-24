from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.security import verify_password, create_access_token
from src.infrastructure.sqlite.database import get_db
from src.infrastructure.sqlite.models.user_models import UserModel
from src.schemas.token import Token

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.nickname == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный никнейм или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.nickname})
    return {"access_token": access_token, "token_type": "bearer"}