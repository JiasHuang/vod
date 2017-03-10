
function onKeyDown(e) {
    switch(e.which) {
        case 37: // left
            bxslider.goToPrevSlide();
            break;
        case 39: // right
            bxslider.goToNextSlide();
            break;
        default:
            return;
    }
    e.preventDefault(); // prevent the default action
}

function setEntryCluster(entryMax) {
    for (var i = 1; i <= $('.imageContainer').length; i++) {
        if (i % entryMax == 1) {
            var old_str = '<!--Entry'+i.toString()+'-->';
            var new_str = '<div class=entryCluster>';
            if (i > entryMax) {
                new_str = '</div>'+new_str;
            }
            document.body.innerHTML = document.body.innerHTML.replace(old_str, new_str);
        }
    }
    document.body.innerHTML = document.body.innerHTML.replace('<!--EntryEnd-->', '</div>');
}

function setWidthHeight(entryMax) {
    windowHeight = $(window).innerHeight();
    windowWidth = $(window).innerWidth();
    $('.imageContainer').css('height', windowHeight * 90 / entryMax / 100);
    $('.imageContainer').css('width', windowHeight * 120 / entryMax / 100);
    $('h2').css('left', windowHeight * 135 / entryMax / 100);
    $('h2').css('width', windowWidth - (windowHeight * 135 / entryMax / 100));
    $('h2').css('height', windowHeight * 90 / entryMax / 100);
};

function onReady() {

    var slider = localStorage.getItem('slider');
    var entryMax = parseInt(localStorage.getItem('entryMax') || '5');

    if (slider == 'no') {
        return;
    }

    if ($('.bxslider').length > 0 &&  $('.imageContainer').length > entryMax) {
        setEntryCluster(entryMax);
        setWidthHeight(entryMax);
        bxslider = $('.bxslider').bxSlider();
        $(document).keydown(onKeyDown);
    }
}

