from fastapi import APIRouter

from app.schemas.public import InfoResponse, PingResponse, SecurityInfoResponse

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/ping", response_model=PingResponse)
def ping() -> PingResponse:
    """Endpoint de test."""
    return {"message": "pong"}


@router.get("/info", response_model=InfoResponse)
def public_info() -> InfoResponse:
    """Endpoint public pour montrer la différence avec les routes protégées."""
    return {
        "message": "Ceci est un endpoint public.",
        "hint": "Pour accéder aux routes privées, connectez-vous et envoyez un token Bearer.",
    }


@router.get("/security-info", response_model=SecurityInfoResponse)
def security_info() -> SecurityInfoResponse:
    """Fournit un résumé simple de ce que montre la démo."""
    return {
        "authentication": "JWT Bearer",
        "password_storage": "PBKDF2-HMAC-SHA256",
        "roles": ["admin", "user", "guest"],
        "public_endpoints": [
            "/public/ping",
            "/public/info",
            "/public/security-info",
            "/auth/login",
            "/auth/register",
        ],
        "authenticated_endpoints": [
            "/private/me",
            "/private/secret",
            "/auth/refresh",
            "/auth/logout",
        ],
        "role_protected_endpoints": {
            "admin_or_user": ["/private/users"],
            "admin_only": ["/private/admin/users", "/private/admin/users/{user_id}"],
        },
    }
