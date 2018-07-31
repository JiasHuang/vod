
var settings = {
    'slider' : {
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' :'yes',
    },
    'entryMax' : {
        'type' : 'select',
        'vals' : ['3', '4', '5', '6', '7'],
        'defs' : '5',
    },
    'format' : {
        'type' : 'select',
        'vals' : ['1080p', '720p', '480p', '360p', 'bestaudio'],
        'defs' : '720p',
    },
    'autosub' : {
        'type' : 'select',
        'vals' : ['yes', 'no'],
        'defs' : 'no',
    },
    'youtubeID' : {
        'type' : 'input',
        'defs' : '',
    },
    'bookmarkURL' : {
        'type' : 'input',
        'defs' : '',
    },
};

var settings_cookies = ['format', 'autosub'];

function saveCookies() {
    var lists = settings_cookies;
    for (var i=0; i<lists.length; i++) {
        saveCookie(lists[i], $('#'+lists[i]).val());
    }
}

function save() {
    for (var id in settings) {
        localStorage.setItem(id, $('#'+id).val());
    }
    saveCookies();
    window.location.href = 'view.py';
}

function resetSettings() {
    for (var id in settings) {
        localStorage.removeItem(id);
    }
    saveCookies();
    location.reload();
}

function cancel() {
    window.location.href = 'view.py';
}

function getValue(id) {
    var val = localStorage.getItem(id);
    if (val === null) {
        val = settings[id]['defs'];
    }
    if ('sync' in settings[id]) {
        var sync_val = $('#'+settings[id]['sync']).attr('value');
        if (sync_val && sync_val.length > 0) {
            val = sync_val;
        }
    }
    return val;
}

function onLangSelect()
{
    localStorage.setItem("lang", $(this).val());
    onDocumentReady();
}

function onActinSelect()
{
    var r = confirm("Are you sure ?");
    if (r == true) {
        cmd = $(this).val();
        if (cmd == 'ClearHistory') {
            localStorage.removeItem('pages');
        } else if (cmd == 'ResetSettings') {
            resetSettings();
        } else if (cmd == 'Update') {
            window.location.href = 'view.py?c=update';
        }
    }
    $(this).val('');
}

function select(id) {
    var text = '';
    text += '<select id="'+id+'">';
    for (var i in settings[id]['vals']) {
        text += '<option value="'+settings[id]['vals'][i]+'">'+getLangLog(settings[id]['vals'][i])+'</option>';
    }
    text += '</select>';
    return text;
}

function input(id) {
    return '<input type="text" id="'+id+'">';
}

function result() {
    var text = '<table>';
    for (var id in settings) {
        if (settings[id]['type'] == 'select') {
            text += '<tr><th>'+getLangLog(id)+'</th><td>'+select(id)+'</td></tr>';
        } else if (settings[id]['type'] == 'input') {
            text += '<tr><th>'+getLangLog(id)+'</th><td>'+input(id)+'</td></tr>';
        }
    }
    text += '</table>';
    return text;
}

function onDocumentReady() {

    $('#'+getLangLog('lang')).prop('checked', true);

    $('#Result').html(result());
    for (var id in settings) {
        $('#'+id).val(getValue(id));
    }

    var options = $('#actionSelect').children().toArray();
    for (var i in options) {
        $(options[i]).text(getLangLog($(options[i]).val()));
    }
}

