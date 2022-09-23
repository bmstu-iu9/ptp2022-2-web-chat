from database import Base, engine
from models import User

"""Creating database"""

Base.metadata.create_all(engine)