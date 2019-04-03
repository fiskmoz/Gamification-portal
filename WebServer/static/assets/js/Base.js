function DisplayResults(request)
{
    request.done(function(msg) {
        Swal.fire({
            title: 'Saved successfully!',
            type: 'success',
            showCancelButton: false,
          }).then(() => {
            window.location.replace("http://127.0.0.1:8000/");
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

var prevScrollpos = window.pageYOffset;
window.onscroll = function() {
var currentScrollPos = window.pageYOffset;
  if (prevScrollpos > currentScrollPos) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-60px";
  }
  prevScrollpos = currentScrollPos;
}

var DEBUG = false;
var APIUrl = 'http://127.0.0.1:7000/API/';
var APIFileUrl = 'http://127.0.0.1:7000/media/';
var HOMEURL = 'http://127.0.0.1:8000/';