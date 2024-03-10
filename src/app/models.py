from sqlmodel import Field, Relationship, SQLModel

# class HeroTeamLink(SQLModel, table=True):
#     team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
#     hero_id: int | None = Field(default=None, foreign_key="hero.id", primary_key=True)

#     is_training: bool = False

#     team: "Team" = Relationship(back_populates="hero_links")
#     hero: "Hero" = Relationship(back_populates="team_links")


# class Team(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     name: str = Field(index=True)
#     headquarters: str

#     hero_links: list[HeroTeamLink] = Relationship(back_populates="team")


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    # team_links: list[HeroTeamLink] = Relationship(back_populates="hero")
