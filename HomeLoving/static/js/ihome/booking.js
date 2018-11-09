function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    $('.submit-btn').click(function () {
        var search=document.location.search
        h_id=search.split('=')[1]
        // 获取入住时间
        var startDate=$('#start-date').val();
        var endDate=$('#end-date').val();

        // 下单
        $.ajax({
            url:'/order/order/',
            data:{'begin_date':startDate,'end_date':endDate,'house_id':h_id},
            dataType:'json',
            type:'POST',
            success:function (data) {
                    alert('32333');
                    location.href='/order/orders/';
            },error:function (data) {
                alert('跳转失败')
            }

        });
    });

});

// $(document).ready(function () {
//
//     var path=window.location.search;
//     var h_id=path.split('&')[0].split('=')[1];
//     $.get('house/getbookingbyid/'+ h_id + '/',function (data) {
//         alert('1234')
//         $('.house-info img').attr('src', data.house.image);
//
//
//     })
//
// })