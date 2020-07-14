$(document).ready(function() {
    var top = $('#navcontainer').offset().top - parseFloat($('#navcontainer').css('marginTop').replace(/auto/, 100));
    $(window).scroll(function (event) {
        var y = $(this).scrollTop();
        if (y >= top) {
            $('#navcontainer').addClass('fixed');
        } else {
            $('#navcontainer').removeClass('fixed');
        }
    });
});
