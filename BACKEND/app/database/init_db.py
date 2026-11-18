from app.database.database import Base, engine

# Import every model here
from app.models.user import User
from app.models.profile import Profile


def init_db():
    Base.metadata.create_all(bind=engine)