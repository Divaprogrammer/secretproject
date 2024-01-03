$( document ).ready(function() {
    if($('#category_page').length || $('#index_page').length)
    {
    $('#trending4').removeClass("col-md-4");
    $('#trending4').addClass("col-md-6");
    $('#trending5').removeClass("col-md-4");
    $('#trending5').addClass("col-md-3");
    $('#trending6').removeClass("col-md-4");
    $('#trending6').addClass("col-md-3");
    }
    if($('#index_page').length)
    {
    $('#latest0').removeClass("col-md-4");
    $('#latest0').addClass("col-md-6");
    $('#latest2').removeClass("col-md-4");
    $('#latest2').addClass("col-md-2");
    $('#latest4').removeClass("col-md-4");
    $('#latest4').addClass("col-md-3");
    $('#latest5').removeClass("col-md-4");
    $('#latest5').addClass("col-md-7");
    $('#latest7').removeClass("col-md-4");
    $('#latest7').addClass("col-md-6");
    $('#latest8').removeClass("col-md-4");
    $('#latest8').addClass("col-md-2");
    }

});