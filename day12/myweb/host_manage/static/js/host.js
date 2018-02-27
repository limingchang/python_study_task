$("#show_modal").click(function(){
    $(".shadow").show();
    $(".modal").slideDown();
    $(".modal").find("input")[0].focus();

});
$("#cancel").click(function(){
    $(".shadow").hide();
    $(".modal").hide();
    $(".modal").find(".errmsg").html("");
    $(".modal").find("input").val("");
});