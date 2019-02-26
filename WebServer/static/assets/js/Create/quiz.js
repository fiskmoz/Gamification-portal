var missionDescription;
var myTableArray = [];
var repeats = 1;

$(document).ready(function()
{
    missionDescription = new Quill('#quizDescription', {
        theme: 'snow'
    });
    $('#quizexitbutton').hide();
});

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE¨
    $('#section1').hide();
    $('#section2').fadeIn(200).removeClass('hidden');
    myTableArray.push($('#quizTitle').val());
    myTableArray.push(missionDescription.container.innerHTML);
    $('#headerText').fadeOut(function (){ $(this).html("Question nr: " + repeats.toString());}).fadeIn();
    $('#headerText2').fadeOut(function (){ $(this).html("Please fill out the form!");}).fadeIn();
}

function quizstage2()
{
    myTableArray.push($('#question').val());
    myTableArray.push($('#id_A').val());
    myTableArray.push($('#id_B').val());
    myTableArray.push($('#id_C').val());
    myTableArray.push($('input[name=correctanswer]:checked').val());

    $('#question').val("");
    $('#id_A').val("");
    $('#id_B').val("");
    $('#id_C').val("");
    $('input[name="correctanswer"]').prop('checked', false);

    repeats = repeats +1;
    $(window).scrollTop(0);
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000
      });
      
      Toast.fire({
        type: 'success',
        title: 'Information valid!'
      })
      $('#quizexitbutton').show();
      $('#headerText').fadeOut(function (){ $(this).html("Question nr: " + repeats.toString());}).fadeIn();
}
function quizexit()
{
    var myJson = {};
    myJson['Quizname'] = myTableArray[0];
    myJson['Description'] = myTableArray[1];
    var i;
    for(i=2; i<myTableArray.length;i++)
    {
        myJson[i-2] = myTableArray[i];
    }
    if(DEBUG)
    {
        alert(JSON.stringify(myJson));
    }
    var request = $.ajax({
    url: "http://127.0.0.1:7000/v1/quiz/",
    type: "POST",
    data: myJson
    });
    
    DisplayResults(request);
}