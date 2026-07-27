from fastapi import Depends, HTTPException

from app.core.dependencies.auth import get_current_user


def require_roles(*roles):

    def role_checker(current_user=Depends(get_current_user)):

        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return current_user

    return role_checker