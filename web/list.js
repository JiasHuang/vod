
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

function onReady() {
    if ($('.entryCluster').length > 1) {
        slider = $('.bxslider').bxSlider();
        $(document).keydown(onKeyDown);
    }
}

