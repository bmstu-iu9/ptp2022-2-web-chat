from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(20), unique=True)
    hashed_password = sa.Column(sa.String(64), unique=False)
    firstname = sa.Column(sa.String(20), unique=False)
    lastname = sa.Column(sa.String(20), unique=False)
    active = sa.Column(sa.Boolean, default=False)
