$(document).ready(function(){
    $(".auth-warn").show();
})

$(document).ready(function () {
    $.get('/house/house_info/',function (data) {
        if (data.code=='200'){
            $('.auth-warn').hide()
            alert('已完成实名认证')
            $('#houses-list').show();
            for(var i=0;i<data.house_info.length;i++){
                var house = '<li>'
                house += '<a href="/house/detail/?house_id=' + data.house_info[i].id + '">'
                house += '<div class="house-title">'
                house +=  '<h3>房屋ID:' + data.house_info[i].id + ' —— ' + data.house_info[i].title + '</h3>'
                house +=  '</div><div class="house-content">'
                house +=  '<img alt="" src="' + data.house_info[i].image + '">'
                house +=  '<div class="house-text"><ul>'
                house +=  '<li>位于：' + data.house_info[i].area + '</li><li>价格：￥' + data.house_info[i].price + '/晚</li><li>发布时间：' + data.house_info[i].create_time + '</li>'
                house += '</ul></div></div></a></li>'
                $('#houses-list').append(house)
            }
        }
        if(data.code=='1013') {
            $('#auth-warn').show()
            $('#house-list').hide()
        }
    })
})