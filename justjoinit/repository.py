from database import get_session
from models import Content
from typing import List, Optional


def create_content(text: str) -> Content:
    db = get_session()
    content = Content(content=text)
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def get_all() -> Optional[List[Content]]:
    db = get_session()
    content = db.query(Content).all()
    return content


