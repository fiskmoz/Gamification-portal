function DisplayResults(request)
{
    request.done(function(msg) {
        Swal.fire({
            title: 'Saved successfully!',
            type: 'success',
            showCancelButton: false,
          }).then(() => {
            window.location.replace(HOMEURL);
          })
    });
    
    request.fail(function(jqXHR, textStatus) {
        Swal.fire({
            title: 'Something went wrong! :(',
            type: 'error',
            showCancelButton: false,
          })
    });
}
function DisplayInputSuccess()
{
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
  })
  Toast.fire({
      type: 'success',
      title: 'Information valid!'
  });
}

function DisplayInputFailed()
{
  const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000
  })
  Toast.fire({
      type: 'error',
      title: 'Check your input again!'
  });
}


var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
  var currentScrollPos = window.pageYOffset;
    if (prevScrollpos > currentScrollPos  && $(window).scrollTop() == 0) {
      document.getElementById("navbar").style.top = "0";
    } else {
      document.getElementById("navbar").style.top = "-60px";
    }
    prevScrollpos = currentScrollPos;
}

var DEBUG = false;
var APIUrl = 'http://127.0.0.1:7000/v1/';
var APIFileUrl = 'http://127.0.0.1:7000/media/';
var HOMEURL = 'http://127.0.0.1:8000/';