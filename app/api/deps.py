from typing import Annotated

from db.session import get_session
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession


# Type alias for easier injection in FastAPI endpoints
DBSession = Annotated[AsyncSession, Depends(get_session)]
