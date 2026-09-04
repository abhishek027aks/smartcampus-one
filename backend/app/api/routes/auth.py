from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, decode_access_token, verify_password
from app.models import User


router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == form_data.username,
        User.is_active.is_(True),
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "college_id": str(user.college_id) if user.college_id else None,
    }

    access_token = create_access_token(token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "college_id": user.college_id,
        },
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception

    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(
        User.id == int(user_id),
        User.is_active.is_(True),
    ).first()

    if not user:
        raise credentials_exception

    return user


def require_roles(*allowed_roles: str):
    def role_checker(
        current_user: User = Depends(get_current_user),
    ):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return current_user

    return role_checker


def require_college_access(
    college_id: int,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "super_admin":
        if current_user.college_id != college_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access data from another college.",
            )

    return current_user


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
        "college_id": current_user.college_id,
        "is_active": current_user.is_active,
    }


@router.get("/teacher-only")
def teacher_only(
    current_user: User = Depends(require_roles("teacher")),
):
    return {
        "message": "Teacher access granted.",
        "user_id": current_user.id,
        "role": current_user.role,
        "college_id": current_user.college_id,
    }


@router.get("/admin-only")
def admin_only(
    current_user: User = Depends(
        require_roles("college_admin", "super_admin")
    ),
):
    return {
        "message": "Admin access granted.",
        "user_id": current_user.id,
        "role": current_user.role,
        "college_id": current_user.college_id,
    }


@router.get("/college/{college_id}")
def college_access_test(
    college_id: int,
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "super_admin":
        if current_user.college_id != college_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot access data from another college.",
            )

    return {
        "message": "College access granted.",
        "requested_college_id": college_id,
        "user_college_id": current_user.college_id,
        "role": current_user.role,
    }
