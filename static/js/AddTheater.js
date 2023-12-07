// import { baseURL } from 'config.js';

const baseURL = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', function () {
    loadMultiplexList();
    // loadTheaterDropdown();
});

function loadMultiplexList() {
    
    url = `${baseURL}/multiplexlist`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })

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
        loadTheaterDropdown(selectedMultiplexId);
        });        
    })
    .catch(error => {
        console.error('Error fetching multiplex list:', error);
    });
}

function loadTheaterDropdown(selectedMultiplexId) {
    if(selectedMultiplexId == null) {
        var multiplexDropdown = document.getElementById('multiplex');
        selectedMultiplexId = multiplexDropdown.value;
    }
    // var theaterDropdown = document.getElementById('theater');
    var theaterContainer = document.getElementById('theaterContainer');

    // Clear existing options and containers
    // theaterDropdown.innerHTML = '';
    theaterContainer.innerHTML = '';

    var url =  `${baseURL}/getalltheaters`;
    var requestData = {
        "multiplexid": selectedMultiplexId
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);

        data.forEach(theater => {
            // Create a container for each theater
            var theaterContainerDiv = document.createElement('div');
            theaterContainerDiv.id = 'theaterContainer_' + theater.theaterid; // Unique ID for each container
            theaterContainerDiv.className =""
            theaterContainer.appendChild(theaterContainerDiv);

            // Create an option for each theater in the dropdown
            // var option = document.createElement('option');
            // option.value = theater.theaterid;
            // option.textContent = 'Theater ' + theater.theaternumber;
            // theaterDropdown.appendChild(option);

            // Populate the theater container with relevant information
            theaterContainerDiv.innerHTML = `
            <div class="theater-form-container">
                <form id="formTheaterId_${theater.theaterid}" class="theater-form"> 
                        <div>
                            <label for="theaterid">theaterid:</label>
                            <input type="text" name="theaterid" value=${theater.theaterid} readonly>
                        </div>
                        <div>
                            <label for="price">showingid:</label>
                            <input type="text" name="showingid"  value=${theater.showingid} readonly>
                        </div>
                        <div>
                            <label for="price">multiplexid:</label>
                            <input type="text" name="multiplexid"  value=${theater.multiplexid} readonly>
                        </div>
                        <div>
                            <label for="price">theaternumber:</label>
                            <input type="text" name="theaternumber" value=${theater.theaternumber} readonly>
                        </div>
                        <div>
                            <label for="price">noofseats:</label>
                            <input type="text" name="noofseats" value=${theater.noofseats} readonly>
                        </div>
                        <div>
                            <label for="price">noofrows:</label>
                            <input type="text" name="noofrows" value=${theater.noofrows} readonly>
                        </div>
                        <div>
                            <label for="price">noofcolumns:</label>
                            <input type="text" name="noofcolumns" value=${theater.noofcolumns} readonly>
                        </div>
                        <div>
                            <label for="price">mmovienames:</label>
                            <input type="text" name="movienames" value="${theater.mmovienames}">
                        </div>
                        <div>
                            <label for="price">mmovienames:</label>
                            <input type="text" name="movieid" value="${theater.mmovieid}">
                        </div>
                        <div>
                            <label for="price">noofcolumns:</label>
                            <input type="text" name="price" value="${theater.prices}">
                        </div>
                        <div>
                            <label for="price">noofcolumns:</label>
                            <input type="text" name="mshowtimes" value="${theater.mshowtimes}">
                        </div>
                        <div hidden>
                            <label for="price">noofcolumns:</label>
                            <input type="text" name="xshowingid" value="${theater.showingid}">
                        </div>
                        <div class="button-conatiner">
                    <button class="save-button" type="button" onclick="movieInTheater('formTheaterId_${theater.theaterid}')">update</button>
                    <button class="save-button" type="button" >Delete</button>
                    </div>
                </form>
                </div>
            `;
        });
    })
    .catch(error => {
        console.error('Error fetching theater list:', error);
    });
}

function movieInTheater(formId) {

    var form = document.getElementById(formId);
    console.log(form);
    var formData = new FormData(form);

    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`);
    });

    var theaterId = formData.get('theaterid');
    var showingId = formData.get('showingid');
    var multiplexId = formData.get('multiplexid');
    var noOfSeats = formData.get('noofseats');
    var theaterNumber = formData.get('theaternumber');
    var noOfRows = formData.get('noofrows');
    var noOfColumns = formData.get('noofcolumns');
    var movieId = formData.get('movieid');
    var price = formData.get('price');
    var showtimes = formData.get('mshowtimes');
    var showingidList = formData.get("xshowingid")

    var updateData = {
        "theaterid": theaterId,
        "showingid": showingId,
        "multiplexid": multiplexId,
        "noofseats": noOfSeats,
        "theaternumber": theaterNumber,
        "noofrows": noOfRows,
        "noofcolumns": noOfColumns,
        "movieid": movieId,
        "price": price,
        "showtimes": showtimes, 
        "showingid": showingidList
    };
    
    updateTheaterAPI(updateData);
}

function updateTheaterAPI(updateData) {

    var updateUrl = `${baseURL}/addTheater`;

    fetch(updateUrl, {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Theater updated successfully:', data);
    })
    .catch(error => {
        console.error('Error updating theater:', error);
    });
}

function deleteTheater(theaterId) {
    var url =  `${baseURL}/removeTheater`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            theaterid: theaterId
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Theater deleted successfully:', data);
    })
    .catch(error => {
        console.error('Error deleting theater:', error);
    });
}

function openEditDialog(theaternumber,theaterid,showingid,noofseats, noofrows, noofcolumns
    ,mmovieid,mmovienames,prices,mshowtimes) {
    var dialog = document.getElementById("edit-theater-dialog");
    document.getElementById("theaternumber").value = theaternumber;
    document.getElementById("theaterid").value = theaterid;
    document.getElementById("showingid").value = showingid;
    document.getElementById("mmovienames").value = mmovienames;
    document.getElementById("noofseats").value = noofseats;
    document.getElementById("noofrows").value = noofrows;
    document.getElementById("noofcolumns").value = noofcolumns;
    document.getElementById("mmovieid").value = mmovieid;
    document.getElementById("mmovienames").value = mmovienames;
    document.getElementById("prices").value = prices;
    document.getElementById("mshowtimes").value = mshowtimes;
    dialog.showModal();
}

function saveChanges(theaterId) {

    var theaterId =  document.getElementById('theaterId').value;
    var showtimes = document.getElementById('showtimes').value;
    var movies = document.getElementById('movies').value;
    var seatingCapacity = document.getElementById('seatingCapacity').value;
    var multiplexId = document.getElementById('multiplexId').value;

    url =  `${baseURL}/addTheater`;

    fetch(url, {
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

function openDialog() {
    var dialog = document.getElementById("add-theater-dialog");
    dialog.showModal();
    updateMovieDropdown();
}

function closeAddTheater() {
    var dialog = document.getElementById("add-theater-dialog");
    dialog.close();
}

function closeEditTheater()
{
    var dialog = document.getElementById("edit-theater-dialog");
    dialog.close();
}

function updateMovieDropdown() {
    var dropdown = document.getElementById("movienames");

    fetch(`${baseURL}/currentmovies`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        dropdown.innerHTML = '';

        var defaultOption = document.createElement('option');
        defaultOption.text = 'Select a movie';
        dropdown.add(defaultOption);

        data.forEach(movie => {
            var option = document.createElement('option');
            option.value = movie.movieid;
            option.text = movie.moviename;
            dropdown.add(option);
        });
    })
    .catch(error => {
        console.error('Error fetching current movies:', error);
    });
}