from fastapi import Request, HTTPException

def require_role(allowed_roles:list):
    def role_checker(request: Request):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized: No user data found")
        user_role = user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient role permissions")

    return role_checker

