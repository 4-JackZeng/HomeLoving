function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){

    $.get('/house/area_facility/',function (data) {

        if (data.code=='200'){

            for (var i=0 ;i<data.areas_info.length;i++){
                var option_str='<option value="'
                option_str+=data.areas_info[i].id+'">'
                option_str+=data.areas_info[i].name+'</option>'

                $('#area-id').append(option_str)
            }

            for(var j=0;j<len(data.facility_info);j++){
                var facility_str='<li><div class="checkbox"><label>'
                facility_str+='<input type="checkbox" name="facility" value="'+data.facility_info[j].id+'">'+data.facility_info[j].name
                facility_str+='</label></div></li>'
                $('.house-facility-list').append(facility_str)
            }
        }
    })






    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $('#form-house-info').submit(function (e) {
        e.preventDefault()
        $('.error-msg text-center').hide();
        $.post('/house/newhouse/',$(this).serialize(),function (data) {
            if (data.code=='200'){
                $('#form-house-info').hide();
                $('#form-house-image').show();
                $('#house-id').val(data.house_id);
            }
            else {
                alert('gg')
            }
        });

    });

    $('#form-house-image').submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url:'/house/image/',
            type:'post',
            dataType:'json',
            success:function (data) {
                if (data.code=='200'){
                    var img='<img src="'+data.img_url+'">'
                    // jQuery里面使用append方法在制定标签后面添加内容.
                    $('.house-image-cons').append(img)
                }
            },
            error:function () {
                alert('gg')
            }

        });
    });

})