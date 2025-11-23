from typing import Generator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session
from app.database import get_session
from app.settings import settings
from app.models import User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        token_data = payload.get("sub")
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data) # Assuming sub is user ID. Or email.
    # If sub is email, we need to query by email.
    # Let's assume sub is email for now as it's common.
    if not user:
         # Try finding by email if ID failed (or just query by email directly)
         statement = User.email == token_data
         # ... wait, session.get takes primary key.
         # Let's query by email.
         from sqlmodel import select
         user = session.exec(select(User).where(User.email == token_data)).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]

def get_current_admin(current_user: CurrentUser) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user

AdminUser = Annotated[User, Depends(get_current_admin)]
