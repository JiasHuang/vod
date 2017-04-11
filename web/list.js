
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

function onPageNav(e) {
    switch(e.which) {
        case 37: // left
            prev = document.getElementById('page_prev');
            if (prev)
                window.location.href = prev.href;
            break;
        case 39: // right
            next = document.getElementById('page_next');
            if (next)
                window.location.href = next.href;
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
    var windowHeight = $(window).innerHeight();
    var windowWidth = $(window).innerWidth();
    var imageHeight = windowHeight * 90 / entryMax / 100;
    var imageWidth = windowHeight * 120 / entryMax / 100;
    var titleWidth = windowWidth - imageWidth - 32;
    $('.imageContainer').css('height', imageHeight);
    $('.imageContainer').css('width', imageWidth);
    $('h2').css('left', imageWidth);
    $('h2').css('width', titleWidth);
    $('h2').css('height', imageHeight);
};

function onReady() {

    var slider = localStorage.getItem('slider');
    var entryMax = parseInt(localStorage.getItem('entryMax') || '5');

    if (slider != 'no' && $('.bxslider').length > 0 &&  $('.imageContainer').length > entryMax) {
        setEntryCluster(entryMax);
        setWidthHeight(entryMax);
        bxslider = $('.bxslider').bxSlider();
        $(document).keydown(onKeyDown);
    }

    else if ($('.pageno').length > 0) {
        $(document).keydown(onPageNav);
    }

    $('#loadingMessage').hide();
}

