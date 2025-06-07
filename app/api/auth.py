from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.jwt import verify_access_token
from pydantic import BaseModel
from app.core.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/admin-login")

def get_current_admin_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    print("Token payload:", payload)
    if not payload or payload.get("role") != "mall_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin token")
    return payload

# Pydantic schema for login
class UserLogin(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(user: UserLogin):
    # Placeholder authentication logic
    if user.email == "admin@example.com" and user.password == "admin123":
        return {"access_token": "dummy_token", "token_type": "bearer"}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")




@router.post("/admin-login")
def admin_login():
    # This should be replaced with real authentication in production
    access_token = create_access_token({"sub": "admin", "role": "mall_admin"})
    return {"access_token": access_token, "token_type": "bearer"}


# from fastapi.security import OAuth2PasswordRequestForm

# @router.post("/admin-login")
# def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
#     # Dummy authentication logic (replace with DB check in real case)
    
#     print("Username:", form_data.username)
#     print("Password:", form_data.password)

#     if form_data.username == "admin" and form_data.password == "admin123":
#         access_token = create_access_token({"sub": form_data.username, "role": "mall_admin"})
#         print(access_token)
#         return {"access_token": access_token, "token_type": "bearer"}

#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Invalid credentials",
#     )
