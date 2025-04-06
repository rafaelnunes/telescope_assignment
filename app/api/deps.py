from typing import Annotated

from db.session import get_session
from fastapi import Depends
from sqlalchemy.orm import Session


# Type alias for easier injection in FastAPI endpoints
DBSession = Annotated[Session, Depends(get_session)]
