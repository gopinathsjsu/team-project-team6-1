// import { baseURL } from 'config.js';
const baseURL = "http://127.0.0.1:5000";

document.addEventListener('DOMContentLoaded', function () {
    loadMovies();
});

function loadMovies() {
    var movieContainer = document.getElementById('movieContainer');
    movieContainer.innerHTML = '';

    var selectedOption = document.getElementById("movies").value;
    
    console.log("selectedmovie", selectedOption)
    if (selectedOption === "upcoming") {

        url = `${baseURL}/upcomingmovies`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        .then(response => response.json())
        .then(data => {
            console.log(data);
            var movieContainer = document.getElementById('movieContainer');
            movieContainer.innerHTML = '';

            data.forEach(movie => {
                var movieBox = document.createElement('div');
                movieBox.classList.add('movie-box');

                movieBox.innerHTML = `
                <h2 >${movie.moviename}</h2>
                <div class="editable-field" data-field="moviename">
                    <div class="editable-container">                                               
                        <div contenteditable="false" id="moviename" name="moviename">
                            <label for="moviename">moviename: ${movie.moviename}</label> 
                        </div>                        
                    </div>
                    <div class="editable-container">                                               
                        <div contenteditable="false" id="movieid">
                            <label for="movieid">movieid: ${movie.movieid}</label> 
                        </div>                        
                    </div>
                </div>
                <div class="editable-field" data-field="runtimeminutes">                    
                    <div class="editable-container">                        
                        <div name="runtimeminutes" id="runtimeminutes">
                            <label for="runtimeminutes">Runtime minutes : ${movie.runtimeminutes} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="releasedate">                    
                    <div class="editable-container">                        
                        <div name="releasedate" id="releasedate" name="releasedate">
                            <label for="releasedate">Release date : ${movie.releasedate} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="endshowingdate">                    
                    <div class="editable-container">                        
                        <div name="endshowingdate" id="endshowingdate" name="endshowingdate">
                            <label for="endshowingdate">End showing date ${movie.endshowingdate} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="poster">                    
                    <div class="editable-container">                        
                        <div name="poster" id="poster" name="poster">
                            <label for="poster">End showing date ${movie.poster} mins</label>
                        </div>
                    </div>
                </div>
                <div class="button-container">
                    <button class="save-btn" id="save-btn" onclick="openEditDialog(${movie.movieid},'${movie.moviename}',${movie.runtimeminutes},'${movie.releasedate}','${movie.endshowingdate}','${movie.poster}')">Edit</button>
                </div>
                `;

                movieContainer.appendChild(movieBox);});
        });
    }
    else if (selectedOption== "current")
    {
        url = `${baseURL}/currentmovies`;

        fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })

        .then(response => response.json())
        .then(data => {
            console.log(data);
            var movieContainer = document.getElementById('movieContainer');
            movieContainer.innerHTML = '';

            data.forEach(movie => {
                var movieBox = document.createElement('div');
                movieBox.classList.add('movie-box');

                movieBox.innerHTML = `
                <h2>${movie.moviename}</h2>
                <div class="editable-field" data-field="movieid">
                    <div class="editable-container">                                               
                        <div contenteditable="false" id="movieid" name="moviename">
                            <label for="movieid">movieid: ${movie.movieid}</label> 
                        </div>                        
                    </div>
                </div>
                <div class="editable-field" data-field="runtimeminutes">                    
                    <div class="editable-container">                        
                        <div name="runtimeminutes" id="runtimeminutes">
                            <label for="runtimeminutes">Runtime minutes : ${movie.runtimeminutes} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="releasedate" name="releasedate">                    
                    <div class="editable-container">                        
                        <div name="releasedate" id="releasedate">
                            <label for="releasedate">Release date : ${movie.releasedate} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="endshowingdate">                    
                    <div class="editable-container">                        
                        <div name="endshowingdate" id="endshowingdate" name="endshowingdate">
                            <label for="endshowingdate">End showing date ${movie.endshowingdate} mins</label>
                        </div>
                    </div>
                </div>
                <div class="editable-field" data-field="poster">                    
                    <div class="editable-container">                        
                        <div name="endshowingdate" id="poster">
                            <label for="poster">End showing date ${movie.poster} mins</label>
                        </div>
                    </div>
                </div>
                <div class="button-container">
                    <button class="save-btn" id="save-btn" onclick="openEditDialog(${movie.movieid},'${movie.moviename}',${movie.runtimeminutes},'${movie.releasedate}','${movie.endshowingdate}','${movie.poster}')">Edit</button>
                </div>
                `;

                movieContainer.appendChild(movieBox);});
        });
    }
}

function openEditDialog(movieid, moviename, runtimeminutes, releasedate, endshowingdate, poster) {
    console.log("inside edit dialog")
    var dialog = document.getElementById("edit-movie-dialog");
    document.getElementById("editmovieid").value = movieid;
    document.getElementById("editmoviename").value = moviename;
    document.getElementById("editruntimeminutes").value = runtimeminutes;
    document.getElementById("editreleasedate").value = releasedate;
    document.getElementById("editendshowingdate").value = endshowingdate;
    document.getElementById("editposter").value = poster;
    dialog.showModal();
}

function closeEditDialog()
{
    var dialog = document.getElementById("edit-movie-dialog");
    dialog.close();
}

function openDialog() {
    var dialog = document.getElementById("add-movie-dialog");
    dialog.showModal();
}

function closeDialog()
{
    var dialog = document.getElementById("add-movie-dialog");
    dialog.close();
}

function addMovie() {

    movieid = document.getElementById("movieid").value;
    moviename = document.getElementById("moviename").value;
    runtimeminutes = document.getElementById("runtimeminutes").value;
    releasedate = document.getElementById("releasedate").value;
    endshowingdate = document.getElementById("endshowingdate").value;
    poster = document.getElementById("poster").value;

    var requestBody = {
        "movieid": movieid,
        "moviename": moviename,
        "runtimeminutes": runtimeminutes,
        "releasedate": releasedate,
        "endshowingdate": endshowingdate,
        "poster" : poster
    };

    fetch(`${baseURL}/addMovie`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

