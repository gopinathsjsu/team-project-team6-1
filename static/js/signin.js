document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("signInForm");
    form.addEventListener("submit", function(event) {
        event.preventDefault(); 

        var username = document.getElementById("username").value;
        var password = document.getElementById("password").value;
        console.log("clicked")

        invokeService(username, password);    
    });
});

function invokeService(username, password) {
    const data = {
        username: username, 
        password: password
    };

    fetch('/signin', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return alert("Incorrect Username or password")
        }
        return alert("Signed in Succesfully !!"); 
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        // Handle errors
        console.error('Fetch error:', error);
    });
    
}    