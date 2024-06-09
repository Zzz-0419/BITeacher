// 添加一个jquery的库

// 先绑定一个点击事件
// 整个网页加载完毕之后再执行
$(function (){
    $("#upload-reply").click(function (event){
        // 组织默认的事件
        event.preventDefault();
        var reply = $("input[name='reply']").val();
        $.ajax({
            url:"/commend/reply?reply="+reply,
            method:"POST",
            success: function (result){
               var code = result['code'];
               if(code == 200){
                    alert("上传评论成功")；
               }
            },
            fail: function (error){
                console.log(error);
            }
        })
    });
});