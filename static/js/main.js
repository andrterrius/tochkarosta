$(document).delegate('.zoom-img', 'click', function() {
    var imageSrc = $(this).attr('src');
    $('.modal-image').attr('src', imageSrc);
    $('#imgmodal').modal('show');
});
$('.img-close').on('click', function() {
    $('#imgmodal').modal('hide');
});
