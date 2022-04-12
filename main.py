from fastapi import FastAPI
from router import user
#Database
from database import Base,engine,get_db


app = FastAPI()

app.include_router(user.UserApp)

Base.metadata.create_all(bind=engine)