function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}



$(document).ready(function () {




    $('#form-avatar').submit(function (e) {
        e.preventDefault()
        // ajaxSubmit提交的是整个表单
        $(this).ajaxSubmit({
            url:'/user/profile/',
            type:'PUT',
            dataType:'json',
            success:function (data) {
                if (data.code =='200'){

                }
            },
            error: function (data) {

            }
        });
    });
    $('#form-name').submit(function (e) {
        e.preventDefault()
        $.ajax({
            url:'/user/profile/',
            dataType: 'json',
            type: 'put',
            data:{'name':$('#user-name').val()},
            success:function (data) {
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