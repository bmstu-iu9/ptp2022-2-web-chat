from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = sa.Column(sa.String(20), primary_key=True)
    hashed_password = sa.Column(sa.String(64), unique=False)
    firstname = sa.Column(sa.String(20), unique=False)
    lastname = sa.Column(sa.String(20), unique=False)
