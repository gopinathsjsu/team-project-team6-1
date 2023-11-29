document.addEventListener('DOMContentLoaded', function () {
    loadMultiplexList();
});

function loadMultiplexList() {
    fetch('/multiplexlist')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var multiplexDropdown = document.getElementById('multiplex');
            data.forEach(multiplex => {
                var option = document.createElement('option');
                option.value = multiplex.multiplexid;
                option.textContent = multiplex.multiplexname;
                multiplexDropdown.appendChild(option);
            });

            multiplexDropdown.addEventListener('change', function () {
                console.log('Dropdown value changed');
                var selectedMultiplexId = multiplexDropdown.value;
                console.log('Selected Multiplex ID:', selectedMultiplexId);
                loadTheaters(selectedMultiplexId);
            });

            loadTheaters(multiplexDropdown.value);
        })
        .catch(error => {
            console.error('Error fetching multiplex list:', error);
        });
}

function loadTheaters(multiplexId) {
    fetch('/getalltheaters', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ multiplexid: multiplexId }),
    })
        .then(response => response.json())
        .then(data => {
            var theaterContainer = document.getElementById('theaterContainer');
            theaterContainer.innerHTML = '';

            data.forEach(theater => {
                var theaterBox = document.createElement('div');
                theaterBox.classList.add('theater-box');

                theaterBox.innerHTML = `
                <h2>Theater ${theater.theaternumber}</h2>
                <div class="editable-field" data-field="showtimes">
                    <div class="editable-container">                                               
                        <div contenteditable="false" id="showtimes">
                            <label for="showtimes">Showtimes :</label> 
                            ${theater.mshowtimes}
                        </div>                        
                    </div>
                </div>
                <div class="editable-field" data-field="movies">
                    <div class="editable-container">                        
                        <div contenteditable="false" id="movies">
                            <label for="movies">Movies Playing :</label>
                            ${theater.mmovienames}
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="seatingCapacity">                    
                    <div class="editable-container">                        
                        <div name="seatingCapacity" id="seatingCapacity">
                            <label for="seatingCapacity">Seating Capacity :</label>
                            ${theater.noofseats}
                        </div>
                    </div>
                </div>
                <button class="save-btn" id="save-btn" onclick="openEditDialog(${multiplexId},${theater.theaterid},'${theater.mshowtimes}','${theater.mmovienames}',${theater.noofseats})">Edit</button>
                `;

                theaterContainer.appendChild(theaterBox);
            });
        })
        .catch(error => {
            console.error('Error fetching theaters:', error);
        });
}

function openEditDialog(multiplexId, theaterId, mshowtimes, mmovienames, noofseats) {
    var dialog = document.getElementById("edit-theater-dialog");
    document.getElementById("theaterId").value = theaterId;
    document.getElementById("multiplexId").value = multiplexId;
    document.getElementById("mshowtimes").value = mshowtimes;
    document.getElementById("mmovienames").value = mmovienames;
    document.getElementById("noofseats").value = noofseats;
    dialog.showModal();
}

function saveChanges(theaterId) {
    var theaterId =  document.getElementById('theaterId').value;
    var showtimes = document.getElementById('showtimes').value;
    var movies = document.getElementById('movies').value;
    var seatingCapacity = document.getElementById('seatingCapacity').value;
    var multiplexId = document.getElementById('multiplexId').value;

    fetch('/addTheater', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            multiplexid: multiplexId,
            theaterId: theaterId,
            showtimes: showtimes,
            movies: movies,
            noofseats: seatingCapacity
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Theater updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating theater:', error);
    });
}

function addTheater() {
    var theaterContainer = document.getElementById('theaterContainer');
    var newTheaterBox = document.createElement('div');
    newTheaterBox.className = 'theater-box';
    newTheaterBox.innerHTML = `
        <h2>New Theater</h2>
        <div class="editable-field" data-field="showtimes">
            <label for="showtimes">Showtimes:</label>
            <div class="editable-container">
                <input type="text" class="showtimes-input" value="[Add showtimes]" id="showtimes" readonly>
                <span class="pen-icon" onclick="toggleEditable('showtimes')">✎</span>
            </div>
        </div>
        <div class="editable-field" data-field="movies">
            <label for="movies">Movies Playing:</label>
            <div class="editable-container">
                <input type="text" class="movies-input" value="[Add movies]" id="movies" readonly>
                <span class="pen-icon" onclick="toggleEditable('movies')">✎</span>
            </div>
        </div>
        <div class="editable-field" data-field="seatingCapacity">
            <label for="seatingCapacity">Seating Capacity:</label>
            <div class="editable-container">
                <input type="text" class="seatingCapacity-input" value="[Add capacity]" id="seatingCapacity" readonly>
                <span class="pen-icon" onclick="toggleEditable('seatingCapacity')">✎</span>
            </div>
        </div>
        <button class="update-btn">Update</button>
    `;
    theaterContainer.appendChild(newTheaterBox);
}

async function addTheater() {
    const showtimes = document.getElementById("showtimes").value;
    const movies = document.getElementById("movies").value;
    const seatingCapacity = document.getElementById("seatingCapacity").value;

    const requestData = {
        multiplexid: 14, 
        noofseats: seatingCapacity,
        theaternumber: 4, 
        noofrows: 4,  
        noofcolumns: 5,  
        movieid: movies,
        price: "12.00, 12.00, 12.25, 12.25",  
        showtimes: showtimes
    };
    const response = await fetch('/addTheater', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    });

    if (response.ok) {
        const result = await response.json();
        console.log('Theater added successfully. Theater ID:', result[0].theaterid);
    } else {
        console.error('Failed to add theater. Status:', response.status);
    }
    document.getElementById("add-theater-dialog").close();
}

function openDialog() {
    var dialog = document.getElementById("add-theater-dialog");
    dialog.showModal();
}