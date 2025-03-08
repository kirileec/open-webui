import datetime
import time
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import text
import uuid
from open_webui.env import (
    WEBUI_SESSION_COOKIE_SAME_SITE,
    WEBUI_SESSION_COOKIE_SECURE,
)
from open_webui.utils.auth import create_token
from open_webui.utils.misc import parse_duration
from open_webui.models.auths import SignupForm, Auths
from open_webui.models.users import Users
from open_webui.constants import ERROR_MESSAGES
from open_webui.env_linx import SSO_SQL
from open_webui.routers.auths import SessionUserResponse, signup
from open_webui.internal.db2 import get_db2

router = APIRouter()


class Signin2Form(BaseModel):
    email: str
    name: str
    pwd: str = ""


@router.post("/signin2", response_model=SessionUserResponse)
async def signin2(request: Request, response: Response, form_data: Signin2Form):
    if SSO_SQL != "":
        sql = SSO_SQL.replace("{email}", f"'{form_data.email}'")
        try:
            with get_db2() as db:
                result = db.execute(text(sql))
                userSrc = result.fetchone()
        except Exception as e:
            raise HTTPException(500, detail=ERROR_MESSAGES.DEFAULT(e))
        if userSrc:
            # 用户存在, 表示验证通过, 此时将用户注册到系统中
            if not Users.get_user_by_email(form_data.email):
                await signup(
                    request,
                    response,
                    SignupForm(
                        email=form_data.email,
                        password=str(uuid.uuid4()),
                        name=form_data.name,
                    ),
                )
            user = Auths.authenticate_user_by_trusted_header(form_data.email)
            if user:
                expires_delta = parse_duration(request.app.state.config.JWT_EXPIRES_IN)
                expires_at = None
                if expires_delta:
                    expires_at = int(time.time()) + int(expires_delta.total_seconds())
                token = create_token(
                    data={"id": user.id},
                    expires_delta=expires_delta,
                )
                datetime_expires_at = (
                    datetime.datetime.fromtimestamp(expires_at, datetime.timezone.utc)
                    if expires_at
                    else None
                )
                # Set the cookie token
                response.set_cookie(
                    key="token",
                    value=token,
                    expires=datetime_expires_at,
                    httponly=True,  # Ensures the cookie is not accessible via JavaScript
                    samesite=WEBUI_SESSION_COOKIE_SAME_SITE,
                    secure=WEBUI_SESSION_COOKIE_SECURE,
                )
                return {
                    "token": token,
                    "token_type": "Bearer",
                    "expires_at": expires_at,
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "profile_image_url": user.profile_image_url,
                }
            else:
                raise HTTPException(400, detail=ERROR_MESSAGES.INVALID_CRED)
        else:
            raise HTTPException(
                400, detail=f"用户 {form_data.name} 不存在或已过期或为免费账号"
            )
    else:
        raise HTTPException(400, detail=f"SSO_SQL is empty")
