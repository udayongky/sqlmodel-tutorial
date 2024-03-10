from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: int | None = None


class HeroRead(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None = None
