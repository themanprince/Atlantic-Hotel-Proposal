document.getElementById("add-room-type-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById("submit-btn-add-room-type");

    const room_type_name = document.getElementById("room_type_name").value;
    const description = document.getElementById("description").value;
    let price = document.getElementById("price").value;
    let capacity = document.getElementById("capacity").value;

    try {
        price = parseFloat(price);
        capacity = parseFloat(capacity);
    } catch(err) {
        Swal.fire({
            "icon": "error",
            "text": "Please Enter a valid number in the field(s) for Price/Capacity"
        });
        return;
    }

    submitBtn.disabled = true;
    submitBtn.innerText = "...Loading...";

    try {
        const response = await fetch("/admin/room-type", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify({room_type_name, description, price, capacity})
        });

        if (response.ok){
            window.location.href="/admin/dashboard?onLoadMessage=Room%20Type%20Created%20Successfully";
        } else if ((response.status >= 400) && (response.status <= 599)) {
            error = await response.json()
            Swal.fire({
                "icon": "error",
                "text": error.detail
            });
        }
    } catch(error) {
        Swal.fire({
            "icon": "error",
            "text": "Request Failed: " + error
        });
    }

    submitBtn.disabled = false;
    submitBtn.innerText = "Add Room Type";
});