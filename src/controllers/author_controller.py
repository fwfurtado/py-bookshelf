from fastapi import APIRouter
from fastapi_sqlalchemy import db
from pydantic import BaseModel, EmailStr

from src.entities.author import Author

router = APIRouter()


class AuthorForm(BaseModel):
    name: str
    email: EmailStr

    def to_author(self):
        return Author(name=self.name, email=self.email)


class AuthorView(BaseModel):
    id: int
    name: str
    email: EmailStr

    @staticmethod
    def of(author: Author):
        return AuthorView(id=author.id, name=author.name, email=author.email)


@router.post('/authors', response_model=AuthorView)
def create_author(author_form: AuthorForm):
    author = author_form.to_author()

    db.session.add(author)
    db.session.commit()

    return AuthorView.of(author)
