
var act = ''
var num = ''
var playbackMode = 'Normal'

function addCode(key) {
	num = num + key;
}

function resetCode() {
	num = '';
}

function setKey(key) {

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
    else if (key == "forward" && num == "##") {
        act = "audio-next";
        num = "";
    }
    else if (key == "stop" && num == "*") {
        act = "sub-remove";
        num = "";
    }

    setAct(act, num);

    act = '';
    num = '';
}

function setAct(act, num='') {
    $.ajax({
      url: 'view.py?a='+act+'&n='+num,
      dataType: 'json',
      error: onTimeout,
      success: parseJSON,
      timeout: 20000
    });
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
    setAct('playbackMode', playbackMode)
    highlightPlaybackMode(playbackMode);
}

function initPlaybackMode () {
    playbackMode = getCookie('playbackMode')
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

function parseJSON(obj) {
  $('#result').html(getResultHTMLText(obj));
}

function onTimeout() {
  console.log('timeout');
}

function updateResult() {
  $.ajax({
    url: 'view.py' + window.location.search,
    dataType: 'json',
    error: onTimeout,
    success: parseJSON,
    timeout: 20000
  });
}

