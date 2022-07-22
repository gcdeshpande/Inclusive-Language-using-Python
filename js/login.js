$(document).ready(function () {
    $("#login").click(function () {
      if ($("#email-id").val() == "") {
        alert("Please Enter email");
        return false;
      }
      if ($("#password").val() == "") {
        alert("Please Enter Password");
        return false;
      }
    });
  });