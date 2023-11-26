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
                    <label for="showtimes">Showtimes:</label>
                    <div class="editable-container">
                        <div contenteditable="false" id="showtimes">${theater.mshowtimes}</div>
                        <span class="pen-icon" onclick="toggleEditable('showtimes')">✎</span>
                    </div>
                </div>
                <div class="editable-field" data-field="movies">
                    <label for="movies">Movies Playing:</label>
                    <div class="editable-container">
                        <div contenteditable="false" id="movies">${theater.mmovienames}</div>
                        <span class="pen-icon" onclick="toggleEditable('movies')">✎</span>
                    </div>
                </div>
                <div class="editable-field" data-field="seatingCapacity">
                    <label for="seatingCapacity">Seating Capacity:</label>
                    <div class="editable-container">
                        <div contenteditable="false" id="seatingCapacity">${theater.noofseats}</div>
                        <span class="pen-icon" onclick="toggleEditable('seatingCapacity')">✎</span>
                    </div>
                </div>
                <button class="update-btn" id="update-btn" onclick="navigateToUpdatePage()">Update</button>
                <button class="save-btn" id="save-btn" onclick="saveChanges(${theater.theaterid})">Save Changes</button>
                
                `;

                theaterContainer.appendChild(theaterBox);
            });
        })
        .catch(error => {
            console.error('Error fetching theaters:', error);
        });
}

function toggleEditable(fieldName) {
    var field = document.querySelector(`[data-field="${fieldName}"] div`);
    var penIcon = document.querySelector(`[data-field="${fieldName}"] .pen-icon`);

    if (field.contentEditable === "false") {
        field.contentEditable = "true";
        penIcon.textContent = "✓";
    } else {
        field.contentEditable = "false";
        penIcon.textContent = "✎";
    }
}
function saveChanges(theaterId) {
    var showtimes = document.getElementById('showtimes').value;
    var movies = document.getElementById('movies').value;
    var seatingCapacity = document.getElementById('seatingCapacity').value;

    fetch('/updateTheater', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            theaterId: theaterId,
            showtimes: showtimes,
            movies: movies,
            seatingCapacity: seatingCapacity
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
        <p>Showtimes: [Add showtimes]</p>
        <p>Movies Playing: [Add movies]</p>
        <p>Seating Capacity: [Add capacity]</p>
        <button class="update-btn">Update</button>
    `;
    theaterContainer.appendChild(newTheaterBox);
}
function navigateToUpdatePage() {
    window.location.href = 'templates/sample.html';
}