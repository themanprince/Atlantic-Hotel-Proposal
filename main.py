from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routers.admin import AdminRouter
from routers.booking import BookingRouter

from services.admin import AdminServices
from db.db import get_db
from sqlalchemy.orm import Session



app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def landing(request: Request, session:Session = Depends(get_db)):
	room_types = await AdminServices.get_all_room_types(session=session)
	return templates.TemplateResponse("index.html", {"request": request, "room_types": room_types}) #type: ignore


app.include_router(AdminRouter)
app.include_router(BookingRouter)


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", reload=True)