//import { baseURL } from './config.js';

const baseURL = "http://127.0.0.1:5000";

multiplexurl =  `${baseURL}/multiplexlist`;
fetch(multiplexurl)
    .then(response => response.json())
    .then(data => {
        const multiplexDropdown = document.getElementById('multiplexid');

        data.forEach(multiplex => {
            const option = document.createElement('option');
            option.value = multiplex.multiplexid;
            option.textContent = multiplex.multiplexname;
            multiplexDropdown.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching multiplex list:', error));
    let moviesArray = [];
    let showtimesArray = [];
    let pricesArray = [];

    function addMovieField() {
    const dynamicInputs = document.getElementById('dynamicMovies');

    const movieField = document.createElement('div');
    const uniqueId = 'movieid_' + Date.now(); // Generate a unique ID
    movieField.innerHTML = `
    <div class= "row col-sm-12">
        <label for="${uniqueId}">Movie:</label>
        <select name="movieid" id="${uniqueId}" style="width: 20%;"></select>

        <label for="price" >Price:</label>
        <input type="text" name="price" style="width:10%;" id="price_${uniqueId}">

        <label for="showtimes">Showtimes:</label>
        <select name="showtimes" style="width: 18%;" id="showtimes_${uniqueId}">
            <option value="10:00:00">10:00 AM</option>
            <option value="13:00:00">01:00 PM</option>
            <option value="17:00:00">05:00 PM</option>
            <option value="20:00:00">08:00 PM</option>
        </select>                
        <button type="button" onclick="removeMovieField(this)">Remove</button>
    </div>
    `;

    dynamicInputs.appendChild(movieField);

    fetchMoviesAndPopulateDropdown(uniqueId);

}

function fetchMoviesAndPopulateDropdown(uniqueId) {
const moviesurl = `${baseURL}/currentmovies`;
fetch(moviesurl)
    .then(response => response.json())
    .then(data => {
        const movieDropdown = document.getElementById(uniqueId);

        data.forEach(movie => {
            const option = document.createElement('option');
            option.value = movie.movieid;
            option.textContent = movie.moviename;
            movieDropdown.appendChild(option);
        });
        movieDropdown.addEventListener('change', () => updateArray(moviesArray, movieDropdown.value));
    })
    .catch(error => console.error('Error fetching movies:', error));
}
    
function updateArray(array, value) {
    array.push(value);
    console.log(array); 
}
    
function removeMovieField(button) {
    const dynamicInputs = document.getElementById('dynamicMovies');
    dynamicInputs.removeChild(button.parentNode);

    moviesArray.pop();
    showtimesArray.pop();
    pricesArray.pop();
}

function submitForm(event) {
    console.log("submit called ")
    event.preventDefault();

    const form = document.getElementById('theaterForm');
    const formData = new FormData(form);

    let movieList = formData.getAll("movieid")
    let priceList = formData.getAll("price")
    let showtimesList = formData.getAll("showtimes")
    let showingidList = formData.getAll("xshowingid")

    console.log(movieList)
    console.log(priceList)
    console.log(showtimesList)
    console.log(showingidList)
    console.log(form);

    const formObject = {};
    formData.forEach((value, key) => {
        if (formObject[key] === undefined) {
            formObject[key] = value;
        } else {
            formObject[key] = Array.isArray(formObject[key])
                ? [...formObject[key], value]
                : [formObject[key], value];
        }
    });

    const request = {
        
        multiplexid: formObject.multiplexid,
        noofseats: formObject.noofseats,
        theaternumber: formObject.theaternumber,
        noofrows: formObject.noofrows,
        noofcolumns: formObject.noofcolumns,
        movieid: movieList,
        price: priceList,
        showtimes: showtimesList,
        showingid: showingidList,
    };

    const addTheaterUrl = `${baseURL}/addTheater`;
    fetch(addTheaterUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Theater added/updated successfully:', data);
    })
    .catch(error => console.error('Error adding/updating theater:', error));
}