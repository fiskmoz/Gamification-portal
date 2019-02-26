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

var DEBUG = false;