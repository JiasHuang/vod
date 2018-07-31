
var act = ''
var num = ''
var playbackMode = 'Normal'

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
    if (statusTxt == "error")
        alert("Error: " + xhr.status + ": " + xhr.statusText);
}

function showStuff (id, btn = null) {
    document.getElementById(id).style.display = 'block';
    if (btn)
        document.getElementById(btn).style.display = 'none';
}

function setPlaybackMode (mode) {
    if (playbackMode.toLowerCase() == mode.toLowerCase())
        playbackMode = 'Normal';
    else
        playbackMode = mode;
    $("#result").load("view.py?a=playbackMode&n="+playbackMode, onLoadCompleted);
    highlightPlaybackMode(playbackMode);
}

function initPlaybackMode () {
    playbackMode = document.getElementById('playbackMode').getAttribute('playbackMode');
    highlightPlaybackMode(playbackMode);
}

function highlightPlaybackMode (mode) {
    mode = mode.toLowerCase();
    document.getElementById('btn_autoNext').classList.remove("btn_hl");
    document.getElementById('btn_loopAll').classList.remove("btn_hl");
    document.getElementById('btn_loopOne').classList.remove("btn_hl");
    if (mode == 'autonext')
        document.getElementById('btn_autoNext').classList.add("btn_hl");
    if (mode == 'loopall')
        document.getElementById('btn_loopAll').classList.add("btn_hl");
    if (mode == 'loopone')
        document.getElementById('btn_loopOne').classList.add("btn_hl");
}
