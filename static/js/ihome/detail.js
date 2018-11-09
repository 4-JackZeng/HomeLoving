function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    $('.book-house').show();
    // location.search返回URL的查询部分(问号之后的部分)
    var search_url=location.search
    house_id=search_url.split('=')[1]
    $.get('/house/detail/'+house_id+'/',function (data) {
        if (data.code=='200'){

            // var booking_temp=template('')
            // console.log(data.house_detail)
            for (var i=0;i<data.house_detail.images.length;i++){

                var swiper_li='<li class="swiper-slide"><img src="'+data.house_detail.images[i]+'"></li>'

                $('.swiper-wrapper').append(swiper_li)

            }
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            })

            $('.house-price span').html(data.house_detail.price)
            $('.book-house').attr('href', '/house/booking/?house_id=' + house_id)
            $('.house-info-address').html(data.house_detail.address)
            $('.house-title').html(data.house_detail.title)
            $('.landlord-name').html('房东： <span>' + data.house_detail.user_name + '</span>')
            $('.landlord-pic').html('<img src="' + data.house_detail.user_avatar + '">')
            $('.house-type-detail').html('<h3>出租' + data.house_detail.room_count + '间</h3><p>房屋面积:' + data.house_detail.acreage + '平米</p><p>房屋户型:' + data.house_detail.unit + '</p>')
            $('.house-capacity').html('<h3>宜住' + data.house_detail.capacity + '人</h3>')

            $('.house-bed').html('<h3>卧床配置</h3><p>' + data.house_detail.beds + '</p>')

            var house_info_style = '<li>收取押金<span>' + data.house_detail.deposit + '</span></li>'
            house_info_style += '<li>最少入住天数<span>' + data.house_detail.min_days + '</span></li>'
            house_info_style += '<li>最多入住天数<span>' + data.house_detail.max_days + '</span></li>'
            $('.house-info-style').html(house_info_style)
            var house_facility_list =''
            for(var i=0;i<data.facility_list.length;i++){
                house_facility_list+='<li><span class="'+ data.facility_list[i].css + '"></span>'+data.facility_list[i].name + '</li>'
            }
            $('.house-facility-list').html(house_facility_list)
            $('.book-house').attr('href', '/house/booking/?id=' + data.house.id)

            // 判断是否显示预定按钮
            if (data.booking==0 & data.booking==1){
                $(".book-house").show();

            }else {

                $(".book-house").show();

            }
        }

    });

});