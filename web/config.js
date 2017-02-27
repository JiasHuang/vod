
function SaveConfig() {
    localStorage.setItem('DisableSlider', $('#DisableSlider').val());
    window.history.back();
}

function CancelConfig() {
    window.history.back();
}

function select_disableslider() {

    var DisableSlider = localStorage.getItem('DisableSlider') || 'no';

    var select = '<select id=DisableSlider>'
    if (DisableSlider == 'no') {
        select += '<option value="yes">yes</option>';
        select += '<option value="no" selected>no</option>';
    } else {
        select += '<option value="yes" selected>yes</option>';
        select += '<option value="no">no</option>';
    }
    select += '</select>'

    return select;
}


function ShowConfig() {

    var text = '<table>';
    text += '<tr><th>DisableSlider</th><td>'+select_disableslider()+'</td></tr>';
    text += '</table>';

    $('#ConfigResult').html(text);
}

