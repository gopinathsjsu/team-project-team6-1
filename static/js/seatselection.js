var reserve = {
    init: () => {
        let layout = document.getElementById("layout");

        let requestData = {
            theaterid: 26,
            showdetailid: 1,
        };

        fetch("/getseatmatrix", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        })
        .then((response) => response.json())
        .then((data) => {
            reserve.generateSeats(layout, data);
            layout.querySelectorAll(".seat.available").forEach((seat) => {
                seat.onclick = () => reserve.toggle(seat);
            });
        })
        .catch((error) => console.error("Error:", error));
    },

   
    generateSeats: (layout, data) => {

    layout.innerHTML = "";

    for (let i = 1; i <= data.length; i++) {
        let seatData = data[i - 1];
        let seat = document.createElement("div");
        seat.innerHTML = i;
        seat.className = "seat";
        
        if (seatData.istaken) {
            seat.classList.add("taken");
        } else {
            seat.classList.add("available");
        }

        layout.appendChild(seat);
        }
    },

    toggle: (seat) => seat.classList.toggle("selected"),

    save: () => {

        let selected = document.querySelectorAll("#layout .selected");

        if (selected.length == 0) {
            alert("No seats selected.");
        } 
        else {
            let seats = [];
            for (let s of selected) {
                seats.push(s.innerHTML);
            }

            console.log("Selected Seats:", seats);
        }
    },
};

window.addEventListener("DOMContentLoaded", reserve.init);
