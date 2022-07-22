$(document).ready(function () {
    $("#register").click(function () {
      let regex = /^([_\-\.0-9a-zA-Z]+)@([_\-\.0-9a-zA-Z]+)\.([a-zA-Z]){2,7}$/;
      let pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
      let patt = /^[A-Za-z0-9]+$/;
      let s = $("#email-id").val();
      let y = $("#password").val();
      if ($("#name").val() == "") {
        alert("Please Enter Name");
        return false;
      }
      if ($("#email-id").val() == "" || regex.test(s) == 0) {
        alert("Please Enter valid Email-id");
        return false;
      }
      if ($("#password").val() == "") {
        alert("Please Enter Password");
        return false;
      } else if ($("#password").val().length < 5 || pattern.test(y) == 0) {
        alert(
          "Must contain at least one  number and one uppercase and lowercase letter, and at least 8 or more characters"
        );
        return false;
      }
  
      if ($("#confirmpassword").val() == "") {
        alert("Please Confirm your Password");
        return false;
      }
  
      if ($("#confirmpassword").val() != $("#password").val()) {
        alert("Please Enter Password and Confirm Password Same");
        return false;
      }
    });
  });