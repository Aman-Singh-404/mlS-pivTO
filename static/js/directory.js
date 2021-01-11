dataTable = [];

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

function postAJAX(url, params = '', callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200)
            callback(this.responseText);
    };
    xhttp.open("post", url);
    xhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    xhttp.setRequestHeader('Cache-Control','no-cache');
    xhttp.send(params);
}

function existData(data){
    var x = document.getElementsByClassName("folder");
    for(var i = 0;i < x.length;i++)
        if(x[i].id == data)
            return true;
    return false;
}

function deselect(){
    if(document.getElementById("select").innerHTML == "Deselect All")
        document.getElementById("select").innerHTML = "Select All";
    else{
        var x = document.getElementsByClassName("folder");
        for(var i = 0;i < x.length;i++)
            if(x[i].checked == false)
                return;
        document.getElementById("select").innerHTML = "Deselect All";
    }
}

function selectAll(){
    var flag = false;
    if(document.getElementById("select").innerHTML == "Select All"){
        document.getElementById("select").innerHTML = "Deselect All";
        flag = true;
    }
    else{
        document.getElementById("select").innerHTML = "Select All";
        flag = false;
    }
    var x = document.getElementsByTagName("input");
    for(var i = 0;i < x.length;i++)
        if(x[i].classList == "folder")
            x[i].checked = flag;
}

function redo(){
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/redo"+document.getElementsByClassName("dirlist")[0].id;
    mform.submit();
}

function undo(){
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/undo"+document.getElementsByClassName("dirlist")[0].id;
    mform.submit();
}

function move(){
    list="";
    var x=document.getElementsByTagName("input");
    for(var i=0;i<x.length;i++)
        if(x[i].classList=="folder" && x[i].checked)
            list+=x[i].id+"@#$#@";
    if(list==""){
        alert("No field selected.");
        return;
    }
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/move"+document.getElementsByClassName("dirlist")[0].id;
    hlabel=document.createElement("input");
    hlabel.type="hidden";
    hlabel.name="move";
    hlabel.value=list;
    mform.appendChild(hlabel);
    mform.submit();
}

function copy(){    
    list="";
    var x=document.getElementsByTagName("input");
    for(var i=0;i<x.length;i++)
        if(x[i].classList=="folder" && x[i].checked)
            list+=x[i].id+"@#$#@";
    if(list==""){
        alert("No field selected.");
        return;
    }
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/copy"+document.getElementsByClassName("dirlist")[0].id;
    hlabel=document.createElement("input");
    hlabel.type="hidden";
    hlabel.name="copy";
    hlabel.value=list;
    mform.appendChild(hlabel);
    mform.submit();
}

function paste(){
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/paste"+document.getElementsByClassName("dirlist")[0].id;
    mform.submit();
}

function rename(){
    value="";
    var x=document.getElementsByTagName("input");
    for(var i=0;i<x.length;i++)
        if(x[i].classList=="folder" && x[i].checked)
            if(value=="")
                value=x[i].id;
            else{
                alert("You can select only one.");
                return;
            }
    if(value==""){
        alert("No field selected.");
        return;
    }
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/rename"+document.getElementsByClassName("dirlist")[0].id;
    hlabel=document.createElement("input");
    hlabel.type="hidden";
    hlabel.name="rename";
    nname=prompt("Enter new name:",value.substr(value.lastIndexOf("/")+1));
    if(nname==null)
        return;
    if(nname==""){
        alert("Name field cannot be empty.");
        return;
    }
    if(existData(nname)){
        alert(nname+" exist.");
        return;
    }
    hlabel.value=value+"@#$#@"+nname;
    mform.appendChild(hlabel);
    mform.submit();
}

function remove(){
    list="";
    var x=document.getElementsByTagName("input");
    for(var i=0;i<x.length;i++)
        if(x[i].classList=="folder" && x[i].checked)
            list+=x[i].id+"@#$#@";
    if(list==""){
        alert("No field selected.");
        return;
    }
    mform=document.getElementById("method");
    mform.action="http://127.0.0.1:8000/dirmode/remove"+document.getElementsByClassName("dirlist")[0].id;
    hlabel=document.createElement("input");
    hlabel.type="hidden";
    hlabel.name="remove";
    hlabel.value=list;
    mform.appendChild(hlabel);
    mform.submit();
}

function hide(){
    if($("input.hide_view").is(":checked"))
        $("input.hide_view").prop("checked",false);
    else
        $("input.hide_view").prop("checked",true);
    localStorage.checked=$("input.hide_view").is(":checked")
    showTable();
}

function newfolder(post_url, embed_url){
    var new_dir = prompt("Enter folder name:");
    if(existData(new_dir) || new_dir == ''){
        alert("Folder exists.");
        return;
    }
    var perform = function(returned_data) {};
    postAJAX(post_url, new_dir, perform);
    addRow(new_dir, embed_url + new_dir + '/', 0, 'Folder');
    showTable();
}

function execute(){
    var modal=document.getElementById("myModal");
    var span=document.getElementsByClassName("close")[0];
    modal.style.display="none";
    var post_url=span.id.split('@#$')[0];
    var embed_url=span.id.split('@#$')[1];
    var file=document.getElementById("newfile");
    for(var i=0;i<file.files.length;i++)
        if(existData(file.files[i].name))
            file.files[i].name=file.files[i].name+'(1)';
    var formData = new FormData();
    formData.enctype = "multipart/form-data";
    for (var i=0;i<file.files.length;i++)
    formData.append("upload", file.files[i]);
    var perform = function(returned_data) {
        alert(returned_data);
        addRow(file.files[i].name, embed_url + file.files[i].name + '/', file.files[i].size, 'Folder');
        showTable();
    };
    postAJAX(post_url, formData, perform);
}

function uploadfile(post_url, embed_url) {
    var modal=document.getElementById("myModal");
    var span=document.getElementsByClassName("close")[0];
    span.id=post_url+'@#$'+embed_url;
    modal.style.display="block";
    span.onclick=function() {
        modal.style.display="none";
    }
    window.onclick=function(event) {
        if(event.target == modal)
            modal.style.display="none";
    }
}

function addRow(name, link, size, type){
    dataTable.push([name, size, type, link]);
}

function modifyRow(old_name,new_name){
    for (var i = 0; i < dataTable.length; i++)
        if (dataTable[i][0] == old_name){
            dataTable[i][0] = new_name;
            break;
        }
}

function deleteRow(name){
    for (var i = 0; i < dataTable.length; i++)
        if (dataTable[i][0] == name){
            dataTable.splice(i, 1);
            break;
        }
}

function fileSize(bytes) {
    var thresh = 1024;
    if(Math.abs(bytes) < thresh) {
        return bytes + ' B';
    }
    var units = ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    var u = -1;
    do {
        bytes /= thresh;
        ++u;
    } while(Math.abs(bytes) >= thresh && u < units.length - 1);
    return bytes.toFixed(1) + ' ' + units[u];
}

function createTable(index){
    idlist = ["name", "size", "type"];
    for (var i = 0;i < 3; i++)
        if (i == index)
            if (document.getElementById(idlist[index]).className == "" || document.getElementById(idlist[index]).className == "fas fa-arrow-down"){
                document.getElementById(idlist[index]).className = "fas fa-arrow-up";
                dataTable.sort(function(a, b) {
                    if(a[index] < b[index]) { return -1; }
                    if(a[index] > b[index]) { return 1; }
                    return 0;
                });
            }
            else{
                document.getElementById(idlist[index]).className = "fas fa-arrow-down";
                dataTable.sort(function(a, b) {
                    if(a[index] < b[index]) { return 1; }
                    if(a[index] > b[index]) { return -1; }
                    return 0;
                });
            }
        else
            document.getElementById(idlist[i]).className = "";
    showTable();
}

function showTable(){
    $("#tb").empty();
    tby = document.getElementById("tb");
    for (var i = 0; i < dataTable.length; i++)
        if((dataTable[i][0].charAt(0) == "." && $("input.hide_view").is(":checked")) || dataTable[i][0].charAt(0) != "."){
            var tr = document.createElement("tr");
            var td0 = document.createElement("td");
            cbox = document.createElement("input");
            cbox.type = "checkbox";
            cbox.id = dataTable[i][0];
            cbox.className = "folder";
            cbox.onclick = deselect;
            td0.appendChild(cbox);
            td0.appendChild(document.createTextNode("\u2003"));
            alink = document.createElement("a");
            alink.style = "text-decoration : none;";
            alink.href = dataTable[i][3];
            alink.appendChild(document.createTextNode(dataTable[i][0]));
            td0.appendChild(alink);
            tr.appendChild(td0);
            var td1 = document.createElement("td");
            td1.appendChild(document.createTextNode(fileSize(dataTable[i][1])));
            tr.appendChild(td1);
            var td2 = document.createElement("td");
            td2.appendChild(document.createTextNode(dataTable[i][2]));
            tr.appendChild(td2);
            tby.appendChild(tr);
        }
}
tableCreate();
