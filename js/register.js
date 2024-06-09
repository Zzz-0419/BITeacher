// 添加一个jquery的库

// 先绑定一个点击事件
// 整个网页加载完毕之后再执行

function bindEmailCaptchaClick(){
    $("#get-captcha").click(function (event){
        // $this代表当前按钮的jquery对象
        var $this = $(this);
        // 组织默认的事件
        event.preventDefault();
        var email = $("input[name='email']").val();
        $.ajax({
            url:"/auth/capture/email?email="+email,
            method:"POST",
            success: function (result){
               var code = result['code'];
               if(code == 200){
                    // 倒计时
                    var countdown = 60;
                    // 取消点击事件
                    $this.off("click");
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -= 1;
                        if(countdown <= 0){
                            clearInterval(timer);
                            $this.text("获取验证码");
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    //alert("验证码发送成功哦");
               }else{
                    alert(result['message']);
               }
            },
            fail: function (error){
                console.log(error);
            }
        })
    });
}

$(function (){
    bindEmailCaptchaClick();
});