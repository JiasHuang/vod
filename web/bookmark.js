
function syncAll() {
    var username = localStorage.getItem('username');
    if (username && username.length > 0) {
        document.getElementById("playlists").href="view.py?p=https://www.youtube.com/user/"+username+"/playlists";
        document.getElementById("channels").href="view.py?p=https://www.youtube.com/user/"+username+"/channels";
        document.getElementById("videos").href="view.py?p=https://www.youtube.com/user/"+username+"/videos";
    }
}

