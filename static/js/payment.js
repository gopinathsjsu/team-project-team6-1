function paymentconfirmation(){
        let card_number = document.getElementById('card_number').value;
        let cvv = document.getElementById('cvv').value;

        // Make a POST request to your Flask route
        fetch('/process_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                card_number: card_number+1234567812345678, 
                cvv: cvv+458,
                userdetails: userdetails
            })
        })
        .then(response => response.text())
        .then(data => {
            console.log(data); // Process the response from Flask
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



function cardFormSubmit() {
    var exp = document.getElementById('expiry_date').value;
    
    if(!isValidDate(exp)){
        document.getElementById('error').style.display = "block";
        document.getElementById('purchasebtn').disabled = true;
        document.getElementById('purchasebtn').style.backgroundColor = 'grey';
        document.getElementById('expiry_date').value = "";
    }
    else{
        document.getElementById('error').style.display = "none";
        var card_number = document.getElementById('card_number').value;
        var cvv = document.getElementById('cvv').value;
        if(card_number && cvv){
            alert("Card details saved successfully!");
        }
        enablePaymentbtn();
    }

}

function isValidDate(dateString) {
    const date = new Date();
    let month = date.getMonth() + 1;
    var year= `${date.getFullYear()}`.substring(2);
    var mon = dateString.substring(0, 2);
    
    var yr = dateString.substring(3);
    if(yr< year){
        return false;
    }
    if(yr == year && mon < month){
        return false;
    }
    if(mon>12){
        return false;
    }
    return true;
}

function enablePaymentbtn(){
    var card_number = document.getElementById('card_number').value;
    var cvv = document.getElementById('cvv').value;
    var exp = document.getElementById('expiry_date').value;
    var email = document.getElementById('email').value;

    if(!card_number || !cvv || !exp || !email){
        document.getElementById('purchasebtn').disabled = true;
        document.getElementById('purchasebtn').style.backgroundColor = 'grey';
    }
    else{
        document.getElementById('purchasebtn').disabled = false;
        document.getElementById('purchasebtn').style.backgroundColor = 'red';
    }
}