$(document).delegate('.zoom-img', 'click', function() {
    var imageSrc = $(this).attr('src');
    $('.modal-image').attr('src', imageSrc);
    $('#imgmodal').modal('show');
});
$('.img-close').on('click', function() {
    $('#imgmodal').modal('hide');
});
var offset = 0

$('#checkbtn').on('click', function(){
    $.ajax({
        url: "api/get_images",
        type: "POST",
        data: {
            offset: offset,
        },
        success: function(data) {
            if (data['success']){
                $('.row').append(data['code']);
                offset += 10;
            }
            else{
                $('#checkbtn').css("display", "None");
                swal({
                    title: 'Произошла ошибка',
                    text: data['error'],
                    confirmButtonText: 'ОК',
                    confirmButtonColor: "red"
                });
            }
        }

    });
});