
var act = ''
var val = ''

function addCode(key) {
	val = val + key;
}

function resetCode() {
	val = '';
}

function setAct(key) {

    act = key;

    if (val == "*0413") {
        act = "load";
        val = "jav";
    }
    else if (val == "*0000") {
        act = "cmd";
        val = "update";
    }
    else if (key == "pause" && val != "") {
        act = "percent"
    }
    else if (key == "forward" && val == "") {
        val = "150";
    }
    else if (key == "backward" && val == "") {
        val = "150";
    }
    else if (key == "forward" && val == "#") {
        act = "playlist-next";
        val = "";
    }
    else if (key == "backward" && val == "#") {
        act = "playlist-prev";
        val = "";
    }
    else if (key == "forward" && val == "*") {
        act = "sub-next";
        val = "";
    }
    else if (key == "backward" && val == "*") {
        act = "sub-prev";
        val = "";
    }
    else if (key == "stop" && val == "*") {
        act = "sub-remove";
        val = "";
    }

    document.forms[0].act.value = act;
    document.forms[0].val.value = val;
}

