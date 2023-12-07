// import { baseURL } from './config.js';
const baseURL = "http://127.0.0.1:5000";

document.addEventListener("DOMContentLoaded", function () {
    const locationDropdown = document.getElementById('locations');
    const multiplexDropdown = document.getElementById('multiplexs');
    const chosenDateInput = document.getElementById('chosenDate');
    const movieIdInput = document.getElementById('movieid');
    const form = document.querySelector('form');
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const chosenDateParts = chosenDateInput.value.split('-');
    const chosenDate = new Date(chosenDateParts[0], chosenDateParts[1] - 1, chosenDateParts[2]);
    
    if (chosenDate < today) {
        alert('Please select a date equal to or greater than today.');
    }

    const locationUrl = `${baseURL}/getlocationlist`;
    
    fetch(locationUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data) && data.length > 0) {
            data.forEach(location => {
                const option = document.createElement('option');
                option.value = location.locationid;
                option.text = location.city;
                locationDropdown.add(option);
            });
        } else {
            console.error('Error fetching location data:', data);
            alert('Error fetching location data. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error fetching location data:', error);
        alert('Error fetching location data. Please try again.');
    });

    const fetchMultiplexes = (locationid) => {
        const multiplexUrl =  `${baseURL}/multiplexlist`;
        const requestData = {
                locationid: locationid,
            };

        fetch(multiplexUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(requestData),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if (Array.isArray(data) && data.length > 0) {
                multiplexDropdown.innerHTML = ''; 

                data.forEach(multiplex => {
                    const option = document.createElement('option');
                    option.value = multiplex.multiplexid;
                    option.text = multiplex.multiplexname;
                    multiplexDropdown.add(option);
                });
            } else {
                console.error('Error fetching multiplex data:', data);
                alert('Error fetching multiplex data. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error fetching multiplex data:', error);
            alert('Error fetching multiplex data. Please try again.');
        });
    };

    locationDropdown.addEventListener('change', function () {
        const selectedLocationId = locationDropdown.value;
        console.log(selectedLocationId);
        fetchMultiplexes(selectedLocationId);
    });

    function submitForm() {
        const selectedMultiplexId = document.getElementById('multiplexs').value;

        console.log('Selected Multiplex ID:', selectedMultiplexId);
        return true;
    }
});
