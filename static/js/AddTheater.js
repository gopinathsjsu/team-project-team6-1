document.addEventListener('DOMContentLoaded', function () {
    loadMultiplexList();
    // loadTheaterDropdown();
});

function loadMultiplexList() {
    
    url = "http://127.0.0.1:5000/multiplexlist";

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

    var url = "http://127.0.0.1:5000/getalltheaters";
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
                <form id="formTheaterId_${theater.theaterid}" class="theater-form"> 
                    <div>
                        <label for="theaterid">theaterid:</label>
                        <input type="text" name="theaterid" style="width:10%;" value=${theater.theaterid} readonly>
                    </div>
                    <div>
                        <label for="price">showingid:</label>
                        <input type="text" name="showingid" style="width:10%;" value=${theater.showingid} readonly>
                    </div>                    
                    <div>
                        <label for="price">multiplexid:</label>
                        <input type="text" name="multiplexid" style="width:10%;" value=${theater.multiplexid} readonly>
                    </div>
                    <div>
                        <label for="price">theaternumber:</label>
                        <input type="text" name="theaternumber" style="width:10%;" value=${theater.theaternumber} readonly>
                    </div>
                    <div>
                        <label for="price">noofseats:</label>
                        <input type="text" name="noofseats" style="width:10%;" value=${theater.noofseats} readonly>
                    </div>
                    <div>
                        <label for="price">noofrows:</label>
                        <input type="text" name="noofrows" style="width:10%;" value=${theater.noofrows} readonly>
                    </div>
                    <div>
                        <label for="price">noofcolumns:</label>
                        <input type="text" name="noofcolumns" style="width:10%;" value=${theater.noofcolumns} readonly>
                    </div>
                    <div>
                        <label for="price">mmovienames:</label>
                        <input type="text" name="movienames" style="width:10%;" value=${theater.mmovienames}>
                    </div>
                    <div>
                        <label for="price">mmovienames:</label>
                        <input type="text" name="movieid" style="width:10%;" value=${theater.mmovieid}>
                    </div>
                    <div>
                        <label for="price">noofcolumns:</label>
                        <input type="text" name="price" style="width:10%;" value=${theater.prices}>
                    </div>
                    <div>
                        <label for="price">noofcolumns:</label>
                        <input type="text" name="mshowtimes" style="width:10%;" value=${theater.mshowtimes}>
                    </div>
                    <button type="button" onclick="movieInTheater('formTheaterId_${theater.theaterid}')">update</button>
                    <button type="button" >Delete</button>
                </form>
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
        "showtimes": showtimes
    };
    
    updateTheaterAPI(updateData);
}

function updateTheaterAPI(updateData) {

    var updateUrl = "http://127.0.0.1:5000/addTheater";

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
            // theaterContainerDiv.innerHTML = `

//             <form id = "formTheaterId_${theater.theaterid}"> 
//                  <label for="theaterid" >theaterid:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.theaterid} readonly>
//                 <label for="price" >showingid:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.showingid} readonly>
//                 <label for="price" >mmovienames:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.mmovienames} readonly>
//                 <label for="price" >multiplexid:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.multiplexid} readonly>
//                 <label for="price" >theaternumber:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.theaternumber} readonly>
//                 <label for="price" >noofcolumns:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.noofcolumns} readonly>
//                 <label for="theaterid" >theaterid:</label>
//                 <input type="text" name="price" style="width:10%;" value=${theater.theaterid} readonly>

//                 <button type="button" onclick="movieInTheater(formTheaterId_${theater.theaterid})">update</button>
//             <form>
//                 <!-- Add more information as needed -->
//             `;
//         });
//     })
//     .catch(error => {
//         console.error('Error fetching theater list:', error);
//     });
// }

// function movieInTheater(formId) {
//     var form = document.getElementById("${formId}");
//     const formData = new FormData(form);
//     console.log(formData);

// }
// function loadTheaterDropdown(multiplexId)
// {
//     url = "http://127.0.0.1:5000/getalltheaters";
    
//     const requestData = {
//         multiplexid: multiplexId,
//     };

//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(requestData),
//     })

//     .then(response => response.json())
//     .then(data => {
//         console.log(data);

//         var theaterDropdown = document.getElementById('theaterid');

//         theaterDropdown.innerHTML = '';

//         console.log("theater dropdown", theaterDropdown)
//         data.forEach(theater => {
//         var option = document.createElement('option');
//         option.value = theater.theaterid;
//         option.textContent = theater.theaternumber;
//         theaterDropdown.appendChild(option);
//     });

//     theaterDropdown.addEventListener('change', function () {
//         console.log('Dropdown value changed');
//         var selectedTheaterId = theaterDropdown.value;
//         console.log('Selected Theater ID:', selectedTheaterId);
//         });
//     })
//     .catch(error => {
//         console.error('Error fetching Theater list:', error);
//     });   
// }

// function loadTheaters(multiplexId) {
    
//     var theaterContainer = document.getElementById('theaterContainer');
//     theaterContainer.innerHTML = '';

//     console.log("load theatrers multiplexid",multiplexId)

//     url = "http://127.0.0.1:5000/getalltheaters";
    
//     fetch(url, {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ multiplexid: multiplexId }),
//     })
//         .then(response => response.json())
//         .then(data => {

//             var theaterContainer = document.getElementById('theaterContainer');
//             theaterContainer.innerHTML = '';

//             data.forEach(theater => {
//                 var theaterBox = document.createElement('div');
//                 theaterBox.classList.add('theater-box');

//                 theaterBox.innerHTML = `
//                 <h2 id="theaternumber" >Theater ${theater.theaternumber}</h2>
//                 <div class="editable-field" data-field="showtimes">
//                     <div class="editable-container">                                               
//                         <div contenteditable="false" id="theaterid">
//                             <label for="theaterid">Theater Id :</label> 
//                             ${theater.theaterid}
//                         </div>                        
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="showingid">
//                     <div class="editable-container">                        
//                         <div contenteditable="false" id="showingid">
//                             <label for="showingid">Showing Id :</label>
//                             ${theater.showingid}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="noofseats">                    
//                     <div class="editable-container">                        
//                         <div name="noofseats" id="noofseats">
//                             <label for="noofseats">Seating Capacity :</label>
//                             ${theater.noofseats}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="noofrows">                    
//                     <div class="editable-container">                        
//                         <div name="noofrows" id="noofrows">
//                             <label for="noofrows">number of rows :</label>
//                             ${theater.noofrows}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="seatingCapacity">                    
//                     <div class="editable-container">                        
//                         <div name="noofcolumns" id="noofcolumns">
//                             <label for="noofcolumns">no of columns :</label>
//                             ${theater.noofcolumns}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="mmovieid">                    
//                     <div class="editable-container">                        
//                         <div name="mmovieid" id="mmovieid">
//                             <label for="mmovieid">movieid :</label>
//                             ${theater.mmovieid}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="mmovienames">                    
//                     <div class="editable-container">                        
//                         <div name="mmovienames" id="mmovienames">
//                             <label for="mmovienames">movienames :</label>
//                             ${theater.mmovienames}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="prices">                    
//                     <div class="editable-container">                        
//                         <div name="seatingCapacity" id="prices">
//                             <label for="prices">Prices:</label>
//                             ${theater.prices}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="editable-field" data-field="mshowtimes">                    
//                     <div class="editable-container">                        
//                         <div name="mshowtimes" id="mshowtimes">
//                             <label for="mshowtimes">Showtimes :</label>
//                             ${theater.mshowtimes}
//                         </div>
//                     </div>
//                 </div>
//                 <div class="button-container">
//                     <button class="save-btn" id="save-btn" onclick="openEditDialog(${theater.theaternumber},${theater.theaterid},${theater.showingid},${theater.noofseats},${theater.noofrows},${theater.noofcolumns},
//                         ${theater.mmovieid}, '${theater.mmovienames}','${theater.prices}','${theater.mshowtimes}')">Edit</button>
//                     <button class="delete-btn" id="delete-btn" onclcik="deleteTheater(${theater.theaterid})">Delete</button>
//                 </div>
//                 `;

//                 theaterContainer.appendChild(theaterBox);
//             });
//         })
//         .catch(error => {
//             console.error('Error fetching theaters:', error);
//         });
// }


function deleteTheater(theaterId) {
    var url = "http://127.0.0.1:5000/removeTheater";

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

    url = "http://127.0.0.1:5000/addTheater";

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

    fetch("http://127.0.0.1:5000/currentmovies", {
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