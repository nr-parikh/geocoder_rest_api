$(document).ready(function() {

  $("#search").click(function() {
    var $position = document.querySelector(".position")
    var searchReq = $.get("/sendRequest/" + $("#query").val());
    searchReq.done(function(data) {
      $("#url").attr("href", data.result);
      position = JSON.stringify(data.position);
      $position.innerHTML = position;
    });
  });

});