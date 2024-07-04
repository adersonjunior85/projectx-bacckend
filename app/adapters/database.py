from sqlmodel import create_engine

from config import settings

db = settings.database
db_uri = f"{db.driver}://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}"

engine = create_engine(url=db_uri, echo=True)
