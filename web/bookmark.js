
function loadgist(gistid, filename) {
    $.ajax({
        url: 'https://api.github.com/gists/'+gistid,
        type: 'GET',
        dataType: 'jsonp',
        cache: true,
        jsonpCallback: 'myCallback',
        timeout: 1000
    }).success( function(gistdata) {
        var content = gistdata.data.files[filename].content;
        parseJSON(JSON.parse(content));
    }).error( function(e) {
        console.log(e);
        $.getJSON("bookmark.json", function(json) {
            parseJSON(json);
        });
    });
}

function genTemplateTable(channel, links) {
    var length4 = (links.length + 3) & ~3;
    var colspan = length4 / 4;
    var text = '';

    text += '<table>';
    text += '<tr><th colspan='+colspan+'>'+channel+'</th></tr>';
    for (var i=0; i<4; i++) {
        text += '<tr>';
        for (var j=0; j<colspan; j++) {
            var idx = i + j * 4;
            if (idx < links.length) {
                text += '<td><a href="view.py?p='+links[idx].link+'">'+links[idx].title+'</a></td>';
            } else {
                text += '<td></td>';
            }
        }
        text += '</tr>';
    }
    text += '</table>';

    return text;
}

function genCustomTable() {
    var text = '';
    var username = localStorage.getItem('username');

    if (username && username.length > 0) {
        links = [
            {'title' : 'playlists', 'link' : 'https://www.youtube.com/user/'+username+'/playlists'},
            {'title' : 'channels', 'link': 'https://www.youtube.com/user/'+username+'/channels'},
            {'title' : 'videos', 'link' : 'https://www.youtube.com/user/'+username+'/videos'}
        ];
        text += genTemplateTable(username, links);
    }

    return text;
}


function parseJSON(obj) {
    var text = '';

    text += genCustomTable();

    for (var i=0; i<obj.channels.length; i++) {
        var channel = obj.channels[i];
        text += genTemplateTable(channel.channel, channel.links);
    }

    $('#result').html(text);
}

function onTimeout () {
    console.log('timeout');
    $.getJSON("bookmark.json", parseJSON);
}

function loadAll() {
    //loadgist("30f6cc0f78ee246c1e28bd537764d6c4", "bookmark.json");
    var jsonURL = 'https://gist.githubusercontent.com/JiasHuang/30f6cc0f78ee246c1e28bd537764d6c4/raw/bookmark.json';

    var bookmark = localStorage.getItem('bookmark');
    if (bookmark && bookmark.length > 0) {
        jsonURL = bookmark;
    }

    $.ajax({
        url: 'access.py?j='+jsonURL,
        dataType: 'json',
        error: onTimeout,
        success: parseJSON,
        timeout: 2000
    });
}

