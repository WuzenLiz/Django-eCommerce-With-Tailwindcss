$("#registerForm").validate({
 rules:{
  username: {
   required: true,
   minlength: 5,
  },
  email:{
   required: true,
   email:true,
  },
  password:{
   minlength: 6
  },
  password_confirm:{
   equalTo: "#password"
  }
 },
 messages:{
  username:{
   required: 'Tên đăng nhập không được để trống.',
   minlength: jQuery.validator.format('Tên đăng nhập cần có tối thiểu {0} ký tự.'),
  },
  email:{
   required: 'Email không được để trống.',
   email: 'Email không hợp lệ.',
  },
  password:{
   minlength: jQuery.validator.format('Password cần có tối thiểu {0} ký tự.'),
  },
  password_confirm:{
   equalTo: 'Không trùng khớp',
  }
 },
 onsubmit: true,
 onfocusout: function(e) {
  console.log($(e).valid());
 },
 focusInvalid: true,
 errorClass: "text-error input-error",
 validClass: "valid",
 submitHandler: function (f) {
  if (f.valid) {
   console.log('GOOD')
  } else {
   console.log('BAD')
  }
 },
 invalidHandler: function(e,validator) {
  
 }
});
$(".password_show").on('change',function(){
 var pw = $("#"+$(".password_show").data("id"));
 if (pw.attr('type') === 'password') {
  pw.attr('type','text');
 }else{
  pw.attr('type','password');
 }
});