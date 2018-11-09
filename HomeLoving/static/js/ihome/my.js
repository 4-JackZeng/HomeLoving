function logout() {
    $.ajax({
        url:"/user/logout/",
        type:'DELETE',
        success:function(data){
            if (data.code=='200') {
            location.href = "/house/index";
        }

        }

    });

}
//
// $(document).ready(function(){
// })