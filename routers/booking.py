from fastapi import APIRouter, Form, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.admin import AdminServices
from sqlalchemy.orm import Session
from db.db import get_db
from datetime import date


BookingRouter = APIRouter(prefix="/book")
templates = Jinja2Templates(directory="templates")



@BookingRouter.post("/form", response_class=HTMLResponse)
async def get_booking_view(request: Request, session:Session = Depends(get_db), arrival_date=Form(), phone_number=Form(), email=Form()):
    room_types = await AdminServices.get_all_room_types(session=session)
    return templates.TemplateResponse("booking_form.html", {"request": request, "arrival_date": arrival_date, "phone_number": phone_number, "email": email, "room_types": room_types, "today": str(date.today())})
