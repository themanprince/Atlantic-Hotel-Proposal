document.getElementById("book-room-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById("submit-btn-book-room");

    const phone_number = document.getElementById("phone_number").value;
    const email = document.getElementById("email").value;
    const arrival = document.getElementById("arrival").value;
    const full_name = document.getElementById("full_name").value;
    const address = document.getElementById("address").value;
    const room_type_id = (new FormData(e.target)).get("room_type_id");

    if(!room_type_id) {
        Swal.fire({
            "icon": "error",
            "text": "Please select a room to book"
        });

        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerText = "...Loading...";
    try {
        const response = await fetch("/book/book", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify({phone_number, email, arrival, full_name, address, room_type_id})
        });

        if (response.ok) {
            const json = await response.json();
            
            if("error" in json) {
                Swal.fire({
                    "icon": "error",
                    "text": json["error"]
                });

                return;
            }
            
            const {booking_id, price} = json;
            
            Swal.fire({
                "icon": "success",
                "text": "Reservation Made",
                "confirmButtonText": "Proceed To Payment",
                "showCancelButton": true
            }).then(res => {
                payWithPaystack(email, price, booking_id, function callback_success(response) {
                    try {
                        fetch("/book/payment", {
                            "method": "POST",
                            "headers": {"Content-Type": "application/json"},
                            "body": JSON.stringify({"booking_id":booking_id, "amount": price, "payment_method": "paystack"})
                        }).then(save_payment_response => {
                            if(save_payment_response.ok) {
                                Swal.fire({
                                    "icon": "success",
                                    "text": "Payment Successful"
                                }).then(res => {
                                    window.location.href="/";
                                }).catch(error => {
                                    Swal.fire({
                                        "icon": "error",
                                        "text": "" + error
                                    });
                                });
                            } else {
                                response.json().then(json => Swal.fire(JSON.stringify(json)));
                            } 
                        });
                    } catch(err) {
                        Swal.fire({
                            "icon": "error",
                            "text": "Payment Request Failed: " + error
                        });
                    }
                });                
            });
        } else if ((response.status >= 400) && (response.status <= 599)) {
            error = await response.json()
            Swal.fire({
                "icon": "error",
                "text": error.detail
            });
        } else {
            Swal.fire("Site Admin Please check out response status of room booking request")
        }       

    } catch(error) {
        Swal.fire({
            "icon": "error",
            "text": "Request Failed: " + error
        });
    }
    submitBtn.disabled = false;
    submitBtn.innerText = "Check Room Availability";
});


