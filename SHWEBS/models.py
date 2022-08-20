from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa


Base = declarative_base()


class Shwebs(Base):
    __tablename__ = "users"

    # id = sa.Column(sa.Integer, primary_key=True)
    # firstname = sa.Column(sa.String, unique=False)
    # lastname = sa.Column(sa.String, unique=False)
