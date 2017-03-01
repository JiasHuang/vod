
function onKeyDown(e) {
    switch(e.which) {
        case 37: // left
            slider.goToPrevSlide();
            break;
        case 39: // right
            slider.goToNextSlide();
            break;
        default:
            return;
    }
    e.preventDefault(); // prevent the default action
}

function setWidthHeight() {
    windowHeight = $(window).innerHeight();
    $('.imageContainer').css('height', windowHeight * 18 / 100);
    $('.imageContainer').css('width', windowHeight * 24 / 100);
};

function onReady() {
    var slider = localStorage.getItem('Slider');
    if (slider && slider == 'no') {
        return;
    }
    if ($('.entryCluster').length > 1) {
        setWidthHeight();
        slider = $('.bxslider').bxSlider();
        $(document).keydown(onKeyDown);
    }
}

