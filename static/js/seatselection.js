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
        const uniqueColumns = [...new Set(data.map((seatData) => seatData.seatno))];
    
        uniqueColumns.forEach((column) => {
            const colDiv = document.createElement("div");
            colDiv.className = "row";
    
            uniqueRows.forEach((row) => {
                const seatData = data.find((seat) => seat.rownum === row && seat.seatno === column);
                const seat = document.createElement("div");
                seat.innerHTML = seatData ? seatData.seatdetailid : "";
                seat.className = "seat";
    
                if (seatData && seatData.istaken) {
                    seat.classList.add("taken");
                } else {
                    seat.classList.add("available");
                }
    
                colDiv.appendChild(seat);
            });
    
            layout.appendChild(colDiv);
        });
    },
    toggle: (seat) => seat.classList.toggle("selected"),

    updateSelectedSeatsMessage: (messageElement) => {
        let userid = document.getElementById("userid").value;
        let selected = document.querySelectorAll("#layout .selected");
        let allSeats = document.querySelectorAll("#layout .seat");
    
        console.log(userid)
        let maxSeats = (userid !== "none") ? 1 : 8;
    
        if (selected.length === 0) {
            messageElement.innerHTML = "No seats selected.";
        } else if (selected.length > maxSeats) {
            messageElement.innerHTML = `You can only select up to ${maxSeats} seats.`;
        } else {
            let seats = Array.from(selected).map((s) => s.innerHTML);
            reserve.selectedSeats = Array.from(selected).map((s) => s.innerHTML);
            console.log("Selected Seats ids:", seats);
            messageElement.innerHTML = `Selected Seats: ${seats}`;
    
            // Disable unselected seats if the user has reached the limit
            allSeats.forEach((seat) => {
                if (!seat.classList.contains("selected") && selected.length === maxSeats) {
                    seat.disabled = true;
                } else {
                    seat.disabled = false;
                }
            });
        }
    },
    
    
    save: () => {
        let selected = document.querySelectorAll("#layout .selected");
        let userid = document.getElementById("userid").value;
        //alert (userid);
        if(userid == 'None'){
            userid =0;
        }
        let maxSeats = (userid !== "none") ? 1 : 8;

        if (selected.length > maxSeats)
            alert("You can only select up to ", maxSeats)
        if (selected.length === 0) {
            alert("No seats selected.");
        } 
        else {
            console.log("Selected Seat IDs:", reserve.selectedSeats);
            let seatIds = Array.from(selected).map((s) => {
                return s.getAttribute("data-seatid");
            });            

            const requestData = {
                seatid: reserve.selectedSeats,
                showingdetailid: document.getElementById("showingdetailid").value, 
                userid: userid,
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

                    const url = `http://127.0.0.1:5001/payment/${data[0].bookingid}`;
                    window.location.href = url;

                    //alert(`Seats reserved successfully! Booking ID: ${data[0].bookingid}`);
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
