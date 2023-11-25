function paymentconfirmation(userdetails, payment, moviedetails){
        var card_number;
        var cvv;
        var exp;
        var rewardpoints = 0;
        var checkBox = document.getElementById("rewardpoints");
        if (checkBox != null && checkBox.checked == true){
            rewardpoints = userdetails.rewardpoints;
        }
        if (document.getElementById('card_number') != null) {
            card_number = document.getElementById('card_number').value;
        }
        else{
            card_number = ""
        }
        if (document.getElementById('cvv') != null) {
            cvv = document.getElementById('cvv').value;
        }
        else{
            cvv = ""
        }

        if (document.getElementById('expiry_date') != null) {
            exp = document.getElementById('expiry_date').value;
        }
        else{
            exp = ""
        }
        let email = document.getElementById('email').value;
        
        // Make a POST request to your Flask route
        fetch('/bookingconfirmation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                card_number: card_number, 
                cvv: cvv,
                exp: exp,
                email: email,
                rewardpointsused: rewardpoints,
                userdetails: userdetails,
                moviedetails: moviedetails,
                payment: payment
            })
        })
        .then(response =>{ 
            if(response.status ==200){
                response.json()
            }
            else{
                return "error";
            }
        })
        .then(data => {
            if(data =="error"){
                window.location.href = '/bookingerror';
            }
            else{
                window.location.href = '/bookingconfirmation';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function addnewcard(){
    document.getElementById('addnewcard').style.display = "none";
    document.getElementById('existingcard').style.display = "none";
    document.getElementById('newcard').style.display = "block";
    document.getElementById('newexp').style.display = "block";
    document.getElementById('newerr').style.display = "block";
    document.getElementById('newcvv').style.display = "block";
    document.getElementById('newsubmit').style.display = "block";

}

function showrewardline(total, points){
    var checkBox = document.getElementById("rewardpoints");
    if (checkBox.checked == true){
        document.getElementById('rewardpoint').style.display = "table-row";
        document.getElementById('total').innerHTML = '$' + (total-points).toFixed(2);
      } else {
        document.getElementById('rewardpoint').style.display = "none";
        document.getElementById('total').innerHTML = '$' + total;
      }
    
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
    var card_number;
    var cvv;
    var exp;
    if (document.getElementById('card_number') != null) {
        card_number = document.getElementById('card_number').value;
    }
    else{
        card_number = ""
    }
    if (document.getElementById('cvv') != null) {
        cvv = document.getElementById('cvv').value;
    }
    else{
        cvv = ""
    }

    if (document.getElementById('expiry_date') != null) {
        exp = document.getElementById('expiry_date').value;
    }
    else{
        exp = ""
    }var email = document.getElementById('email').value;

    if(!card_number || !cvv || !exp || !email){
        document.getElementById('purchasebtn').disabled = true;
        document.getElementById('purchasebtn').style.backgroundColor = 'grey';
    }
    else{
        document.getElementById('purchasebtn').disabled = false;
        document.getElementById('purchasebtn').style.backgroundColor = 'red';
    }
    document.getElementById('purchasebtn').disabled = false;
    document.getElementById('purchasebtn').style.backgroundColor = 'red';
    
}