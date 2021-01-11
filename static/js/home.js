function adjust() {
    var  flew_h = document.getElementsByClassName("flew_h");
    var height = window.innerHeight-document.getElementById("nav").offsetHeight;
    for (var i=0;i<flew_h.length;i++){
        flew_h[i].style.maxHeight = height.toString()+"px";
    }
}

function report(element){
    if(element.value.trim() != "")
        element.classList.add('has-val');
    else
        element.classList.remove('has-val');
}

function showValidate(){
    var flag = true;
    div = document.getElementsByClassName("wrap-input100");
    for (var i = 0; i < div.length ; i++){
        input = div[i].getElementsByClassName("input100")[0];
        if (input.value.trim() == ""){
            div[i].classList.add('alert-validate');
            flag = false;
        }
    }  
    return flag;
}

function hideValidate(element){
    element.parentNode.classList.remove('alert-validate');
}
