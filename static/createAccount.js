function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changeIcon(){
    var input = document.getElementById("password");
    var icon = document.getElementById("icon");
    if (icon.className == "far fa-eye-slash"){
        icon.className = "far fa-eye";
        input.type = "text";
    }
    else{
        icon.className = "far fa-eye-slash";
        input.type = "password";
    }
}

function validatePassword(url){
    password = document.getElementById("password");
    if (password.value  == ""){
        alertbox.innerHTML = "";
        alertbox.style.display = "none";
        password.style.borderColor = '#ebebeb';
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200){
            alertbox = document.getElementById("alert");
            if (this.responseText == "true"){
                alertbox.innerHTML = "";
                alertbox.style.display = "none";
                password.style.borderColor = '#ebebeb';
            }
            else{
                alertbox.innerHTML = this.responseText;
                alertbox.style.display = "block";
                password.style.borderColor = "red";
            }
        }
    };
    xhttp.open("post", url);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.setRequestHeader('Cache-Control','no-cache');
    xhttp.send(password.value);
}

function checkPassword(object0, object1){
    if (object0.value == '' || object1.value == '')
        return;
    if (object0.value == object1.value){
        object0.style.borderColor = "green";
        object1.style.borderColor = "green";
    }
    else{
        object0.style.borderColor = "red";
        object1.style.borderColor = "red";
    }
}

function addSpaces(){
    var input =document.getElementById("phone");
    input.value = input.value.replace(" ", "").replace(/(\d{3})\D?(\d{3})\D?(\d{1})/,"$1 $2 $3");
    input.value = input.value.replace(" ", "").replace(/(\d{3})\D?(\d{1})/,"$1 $2");
}

function showValidate(){
    var flag = true;
    input = document.getElementsByClassName("form-input");
    for (var i = 0; i < input.length ; i++){
        if (input[i].value.trim() == ""){
            input[i].style.borderColor = "red";
            flag = false;
        }
    }
    if (document.getElementById("password").style.borderColor == "red")
        flag = false;
    return flag;
}

function removeAlert(object){
    if (object.style.borderColor == 'red')
        object.style.borderColor = '#ebebeb';
}