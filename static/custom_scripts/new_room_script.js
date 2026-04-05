document.getElementById("add-new-room-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById("submit-btn-add-room");

    const room_number = document.getElementById("room_number").value;
    const room_type_id = document.getElementById("room_type_id").value;

    try {
        parseInt(room_number);
    } catch(err) {
        Swal.fire({
            "icon": "error",
            "text": "Please Enter a valid number in the field(s) for Room Number"
        });
        return;
    }

    submitBtn.innerText = "...Loading...";
    submitBtn.disabled = true;
    try {
        const response = await fetch("/admin/room", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": JSON.stringify({room_number, room_type_id})
        });

        if (response.ok)
            window.location.href="/admin/dashboard?onLoadMessage=New%20Room%20%20Added%20Successfully";
        else if ((response.status >= 400) && (response.status <= 599)) {
            const error = await response.json()
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
    submitBtn.innerText = "Add Room";
});