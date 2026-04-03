from fastapi import APIRouter, Depends, Request, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.db import get_db
from sqlalchemy.orm import Session
from services.admin import AdminServices


AdminRouter = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="templates")


@AdminRouter.get("/room-type", response_class=HTMLResponse)
async def new_room_type_view(request: Request, session:Session = Depends(get_db)):
    room_types = await AdminServices.get_all_room_types(session=session)
    return templates.TemplateResponse("new_room_type.html", {"request": request, "room_types": room_types})


@AdminRouter.post("/room-type")
async def new_room_type(session: Session = Depends(get_db), room_type_name:str = Body(embed=True), description:str = Body(embed=True), price:float = Body(embed=True), capacity:int = Body(embed=True)):
    return await AdminServices.new_room_type(session=session, room_type_name=room_type_name, description=description, price=price, capacity=capacity)


@AdminRouter.get("/dashboard", response_class=HTMLResponse)
@AdminRouter.post("/dashboard", response_class=HTMLResponse)
async def dashboard(request:Request, onLoadMessage:str|None = None):
    return templates.TemplateResponse("dashboard.html", {"request": request, "onLoadMessage": onLoadMessage})