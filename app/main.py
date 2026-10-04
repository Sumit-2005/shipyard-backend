from fastapi import FastAPI
from .routers import user, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["https://sumit-social.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome, to my API!"}