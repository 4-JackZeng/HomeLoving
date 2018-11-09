function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}





$(document).ready(function () {


    $.get('/user/show_id/',function (data) {
    $('#real-name').val(data.id_name);
    $('#id-card').val(data.id_card);
    if(data.id_name!=null && data.id_card!=null) {
        alert(data.id_name)
        $('.btn-success').hide();
    }
});

    $('#form-auth').submit(function (e) {
        e.preventDefault()
        $.ajax({
            url:'/user/auth/',
            type:'post',
            dataType:'json',
            data:{
                id_name:$('#real-name').val(),
                id_card:$('#id-card').val()
            },
            success:function (data) {
                alert('45')
                if (data.code=='200'){
                     alert(data.msg)
                }

            },
            error:function () {
                alert('gg')
            }
        });
    });

})

// TODO:实名认证能够保存但是一直进入error:function