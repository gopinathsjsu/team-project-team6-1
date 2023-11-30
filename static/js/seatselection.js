var reserve = {
    selectedSeats: [],

    init: () => {
        let layout = document.getElementById("layout");
        let selectedSeatsMessage = document.getElementById("selected-seats-message");

        // let requestData = {
        //     theaterid: 26,
        //     showdetailid: 1,
        // };

        let requestData = {
            theaterid: document.getElementById("theaterid").value,
            showdetailid: document.getElementById("showingdetailid").value,            
        };        

        console.log(document.getElementById("theaterid").value)
        console.log(document.getElementById("showingdetailid").value)
        const url = "http://127.0.0.1:5000/getseatmatrix";
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log("after API call")
            reserve.generateSeats(layout, data);

            layout.querySelectorAll(".seat.available").forEach((seat) => {
                seat.onclick = () => {
                    reserve.toggle(seat);
                    reserve.updateSelectedSeatsMessage(selectedSeatsMessage);
                };
            });
        })
        .catch((error) => console.error("Error:", error));
    },

    generateSeats: (layout, data) => {
        layout.innerHTML = "";
    
        const uniqueRows = [...new Set(data.map((seatData) => seatData.rownum))];
        const uniqueColumns = [...new Set(data.map((seatData) => seatData.noofcolumns))];
    
        uniqueRows.forEach((row) => {
            const rowDiv = document.createElement("div");
            rowDiv.className = "row";
    
            uniqueColumns.forEach((column) => {
                const seatData = data.find((seat) => seat.rownum === row && seat.noofcolumns === column);
                const seat = document.createElement("div");
                seat.innerHTML = seatData ? seatData.seatid : "";
                seat.className = "seat";
    
                if (seatData && seatData.istaken) {
                    seat.classList.add("taken");
                } else {
                    seat.classList.add("available");
                }
    
                rowDiv.appendChild(seat);
            });
    
            layout.appendChild(rowDiv);
        });
    },
    toggle: (seat) => seat.classList.toggle("selected"),

    updateSelectedSeatsMessage: (messageElement) => {

        let selected = document.querySelectorAll("#layout .selected");
    
        if (selected.length === 0) {
            messageElement.innerHTML = "No seats selected.";
        } else {
            let seats = Array.from(selected).map((s) => s.innerHTML);
            reserve.selectedSeats = Array.from(selected).map((s) => s.innerHTML);
            console.log("Selected Seats ids:", seats);
            messageElement.innerHTML = `Selected Seats: ${seats}`;
        }
    },   
    
    save: () => {
        let selected = document.querySelectorAll("#layout .selected");

        if (selected.length === 0) {
            alert("No seats selected.");
        } else {
            console.log("Selected Seat IDs:", reserve.selectedSeats);
            let seatIds = Array.from(selected).map((s) => {
                return s.getAttribute("data-seatid");
            });

            const userid = 1;

            const requestData = {
                seatid: reserve.selectedSeats,
                showingdetailid: document.getElementById("showingdetailid").value, 
                userid: 1,
            };
            const url = "http://127.0.0.1:5000/createbooking";
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData),
            })
            .then(response => response.json())
            .then(data => {
                console.log("API Response:", data);

                if (data && data.length > 0 && data[0].bookingid) {
                    alert(`Seats reserved successfully! Booking ID: ${data[0].bookingid}`);
                } else {
                    alert("Failed to reserve seats.");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("An error occurred while reserving seats.");
            });
        }
    },
};

window.addEventListener("DOMContentLoaded", reserve.init);
