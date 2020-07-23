function openModal0() {
    var modal = document.getElementById("myModal0");
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = "block";
    span.onclick = function() {
        modal.style.display = "none";
    }
    window.onclick = function(event) {
        if (event.target == modal) 
            modal.style.display = "none";
    }
}

function openModal1(text) {
    var modal = document.getElementById("myModal1");
    document.getElementById("response").innerText = text;
    modal.style.display = "block";
    window.onclick = function(event) {
        if (event.target == modal) 
            modal.style.display = "none";
    }
}

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

function postAJAX(url, callback, params = '') {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
            callback(this.responseText);
    };
    xhttp.open("post", url);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.send(params);
}

function changeDetails(post_url) {
    var formData = new FormData();
    if (document.getElementById("id_username").disabled==false){
        if (document.getElementById("id_username").value == ""){
            openModal1("Input can't be empty.");
            return;
        }
        formData.append("username", document.getElementById("id_username").value);
    }
    if (document.getElementById("id_first_name").disabled==false){
        if (document.getElementById("id_first_name").value == ""){
            openModal1("Input can't be empty.");
            return;
        }
        formData.append("firstname", document.getElementById("id_first_name").value);
    }
    if (document.getElementById("id_last_name").disabled==false){
        if (document.getElementById("id_last_name").value == ""){
            openModal1("Input can't be empty.");
            return;
        }
        formData.append("lastname", document.getElementById("id_last_name").value);
    }
    if (document.getElementById("id_email").disabled==false){
        if (document.getElementById("id_email").value == ""){
            openModal1("Input can't be empty.");
            return;
        }
        formData.append("email", document.getElementById("id_email").value);
    }
    var perform = function(response) {
        openModal1(response);
    };
    postAJAX(post_url, perform, formData);
}

function changePassword(post_url) {
    var oldpass = document.getElementById("old_password");
    var newpass = document.getElementById("new_password");
    var newrepass = document.getElementById("new_re_password");
    if (oldpass.value == "" || newpass.value == "" || newrepass.value == ""){
        openModal1("Input can't be empty.");
        return;
    }
    else if (newrepass.value != newpass.value){
        openModal1("Passwords not matched.");
        return;
    }
    var formData = new FormData();
    formData.append("old_password", oldpass.value);
    formData.append("new_password", newpass.value);
    var perform = function(response) {
        openModal1(response);
        if (response == "Password changed.")
            document.getElementById("myModal").style.display = 'none';
    };
    postAJAX(post_url, perform, formData);
}

function remove(post_url, name){
    var perform = function(response) {
        document.getElementById(name).style.display = "none";
    };
    postAJAX(post_url, perform);
}
function download(post_url, name){
    var perform = function(response) {
        var element = document.createElement("a");
        element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(response));
        element.setAttribute("download", name + ".txt");
        element.style.display = "none";
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };
    postAJAX(post_url, perform);
}
