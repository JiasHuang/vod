
var act = ''
var num = ''

function addCode(key) {
	num = num + key;
}

function resetCode() {
	num = '';
}

function setAct(key) {

    act = key;

    if (key == "pause" && num != "") {
        act = "percent"
    }
    else if (key == "forward" && num == "") {
        num = "150";
    }
    else if (key == "backward" && num == "") {
        num = "150";
    }
    else if (key == "forward" && num == "#") {
        act = "playlist-next";
        num = "";
    }
    else if (key == "backward" && num == "#") {
        act = "playlist-prev";
        num = "";
    }
    else if (key == "forward" && num == "*") {
        act = "sub-next";
        num = "";
    }
    else if (key == "backward" && num == "*") {
        act = "sub-prev";
        num = "";
    }
    else if (key == "stop" && num == "*") {
        act = "sub-remove";
        num = "";
    }

    $("#result").load("view.py?a="+act+"&n="+num, onLoadCompleted);

    act = '';
    num = '';
}

function onLoadCompleted (responseTxt, statusTxt, xhr) {
    if (statusTxt == "success")
        showServerMessage();
    if(statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText);
}
