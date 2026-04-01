from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.utils import APIResponse, MessageResponse

router = APIRouter(prefix="/public", tags=["Public"])


@router.get("/ping", response_model=APIResponse[MessageResponse])
def ping() -> APIResponse[MessageResponse]:
    """Endpoint de test."""
    return APIResponse(
        status=True,
        data=MessageResponse(message="pong"),
        message="Ping successful",
        timestamp=datetime.now(timezone.utc),
    )
