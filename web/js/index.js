$(function () {
    $('.searchBtn1').on('click', function () {
        $('.column1 p').fadeToggle(300)
        $('.column1 infoBox').fadeToggle(300)
        $.get('http://127.0.0.1:5000', { flowerName: $('.search').val() }, function (res) {
            console.log(res.data);
        })
    })
    $('.searchBtn2').on('click', function () {
        $('.column2 p').fadeToggle(300)
        $('.column2 infoBox').fadeToggle(300)
        $.get('http://127.0.0.1:5000', { flowerName: $('.search').val() }, function (res) {
            console.log(res.data);
        })
    })
    $('.showHuayu').on('click', function() {
        $('.huayu').slideToggle(300)
    })
})