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