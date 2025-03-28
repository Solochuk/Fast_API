from fastapi import FastAPI
from db.config import Config


app = FastAPI()
Config.migrate()

from routes import user, advertisement
