//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/house/search/?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName="";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
    alert(url)
}

$(document).ready(function(){
    $(".top-bar>.register-login").show();
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    }); 
    $(".area-list a").click(function(e){
        $("#area-btn").html($(this).html());
        $(".search-btn").attr("area-id", $(this).attr("area-id"));
        $(".search-btn").attr("area-name", $(this).html());
        $("#area-modal").modal("hide");
    });
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.get('/house/hindex/', function(data){
        if(data.code == '200'){
                $('.register-login').hide()
                $('.user-info').show()
                $('.user-name').html(data.name)
            }
             else{
                $('.register-login').show();
                $('.user-info').hide()
            }

            // 地区信息

            var area_html=template('home-area-list',{areas:data.alist});
            $('.area-list').html(area_html);


            // 点击地区事件
            $('.area-list a').click(function (e) {
                $('#area-btn').html($(this).html());

                $('.search-btn').attr('area-id',$(this).attr('area-id'));
                $('.search-btn').attr('area-name',$(this).html());
                $('#area-modal').modal('hide');
            });

            // 展示前5个房屋信息

            var swiper_html=template('house_list',{hlist:data.hlist});
            $('.swiper-wrapper').html(swiper_html);



            // for(var i=0;i<data.houses_info.length; i++){
            //      var banner = '<div class="swiper-slide">'
            //      banner += '<img src="/static/media/' + data.houses_info[i].image + '">'
            //      banner += '<div class="slide-title">' + data.houses_info[i].title + '</div></div>'
            //     $('.swiper-wrapper').append(banner)
            // }
            //

            // 轮播图效果
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true
            });
    });

});


function logout() {
    $.ajax({
        url: '/user/logout/',
        type: 'DELETE',
        success: function (data) {
            if (data.code == '200') {
                $(".user-info").hide();
                $(".register-login").show();
            }
        }
    });
}
