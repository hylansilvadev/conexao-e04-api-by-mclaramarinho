from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
import uvicorn
from router.event_routes import router as event_router
from router.faq_routes import router as faq_router
from router.class_routes import router as class_router
from router.contact_routes import router as contact_router
from router.admin_routes import router as admin_router

config = dotenv_values(".env")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "MongoDB - Root"}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print(f"Connected to {app.database}")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Mongo db client closed")


app.include_router(event_router, tags=["events"], prefix="/api/events")
app.include_router(faq_router, tags=["faq", 'frequently asked questions'], prefix="/api/faq")
app.include_router(class_router, tags=["class"], prefix="/api/class")
app.include_router(contact_router, tags=['contact'], prefix="/api/contact")
app.include_router(admin_router, tags=['admin'], prefix="/api/admin")

if __name__ == "__main__":
    uvicorn.run(app, port=8080)