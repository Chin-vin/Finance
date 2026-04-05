from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth_routes, user_routes, record_routes, dashboard_routes
from slowapi import Limiter
from slowapi.util import get_remote_address
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(record_routes.router)
app.include_router(dashboard_routes.router)