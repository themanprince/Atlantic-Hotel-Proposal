from fastapi import APIRouter, Form, Request, Depends, Body
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.admin import AdminServices
from sqlalchemy.orm import Session
from db.db import get_db
from datetime import date


BookingRouter = APIRouter(prefix="/book")
templates = Jinja2Templates(directory="templates")


@BookingRouter.post("/book")
async def create_booking(session:Session = Depends(get_db), phone_number = Body(embed=True), email = Body(embed=True), arrival = Body(embed=True), full_name = Body(embed=True), address = Body(embed=True), room_type_id = Body(embed=True)):
    return await AdminServices.create_booking(
        session = session,
        guest_info=dict(
            phone_number = phone_number,
            email = email, 
            full_name = full_name,
            address = address
        ),
        other_info = dict(
            arrival = arrival,
            room_type_id = room_type_id
        )
    )


@BookingRouter.post("/payment")
async def booking_payment(session: Session = Depends(get_db), booking_id = Body(embed=True), amount = Body(embed=True), payment_method = Body(embed=True)):
    return await AdminServices.booking_payment(session = session, booking_id = booking_id, amount = amount, payment_method = payment_method)


@BookingRouter.post("/", response_class=HTMLResponse)
async def get_booking_view(request: Request, session:Session = Depends(get_db), arrival_date=Form(), phone_number=Form(), email=Form()):
    room_types = await AdminServices.get_all_room_types(session=session)
    return templates.TemplateResponse("booking_form.html", {"request": request, "arrival_date": arrival_date, "phone_number": phone_number, "email": email, "room_types": room_types, "today": str(date.today())})
