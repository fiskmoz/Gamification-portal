var missionType = ""; 
var myTableArray = [];
var repeats = 0;

function validate(name)
{
    missionType = name; 
    // CHECK IF MISSION NAME IS UNIQUE¨
    $('#alternatives').hide();
    switch(missionType)
    {
        case "quiz": 
            $('#quiz_section1').fadeIn(200).removeClass('hidden');
            break;
        case "article":
            $('#news_article').fadeIn(200).removeClass('hidden');
        break; 
    }
    $('#id_headertext').innerHTML = "You have chosen a " + missionType;
}

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE¨
    $('#quiz_section1').addClass('hidden');
    $('#quiz_section2').fadeIn(200).removeClass('hidden');
    myTableArray.push($('#id_missionname').value);
    myTableArray.push($('#id_missiondescription').value);
    $('#id_headertext').fadeOut(function (){ $(this).innerHTML = "You have chosen a " + missionType + " with " + repeats.toString() + " questions!";}).fadeIn();
    $('#quizform').fadeIn(200).css('display','table');
}

function quizstage2()
{
    myTableArray.push($('#id_quizquestion').value);
    myTableArray.push($('#id_answereA').value);
    myTableArray.push($('#id_answereB').value);
    myTableArray.push($('#id_answereC').vlaue);
    myTableArray.push($('#id_correctanswer').value);

    $('#id_quizquestion').value = "";
    $('#id_answereA').value = "";
    $('#id_answereB').value = "";
    $('#id_answereC').value = "";
    $('input[name=correctanswer]').attr('checked',false);

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
      document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType + " with " + repeats.toString() + " questions!";
}
function quizexit()
{
    var myJson = {};
    myJson['Quizname'] = myTableArray[0];
    myJson['Description'] = myTableArray[1];
    var i;
    for(i=2; i<myTableArray.length;i++)
    {
        myJson[i] = myTableArray[i];
    }
    var request = $.ajax({
    url: "http://127.0.0.1:7000/v1/quiz/",
    type: "POST",
    data: myJson
    });
    
    DisplayResults(request);
}

function submitArticle()
{
    var myJson = {};
    myJson["ArticleTitle"] = $('#articleTitle').value; 
    myJson["ArticleDescription"] = $('#articleDesc').value;
    myJson["ArticleQuiz"] = $('select#quizSelection option:selected').val();
    $("#fileuploader").uploadFile({
        url:"http://127.0.0.1:7000/v1/news/fileupload/",
        fileName:"myfile"
        });
    // alert(JSON.stringify(myJson));
    var request = $.ajax({
        url: "http://127.0.0.1:7000/v1/news/",
        type: "POST",
        data: myJson
        });

    DisplayResults(request);
}

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

$(document).ready(function()
{
    $("#fileuploader").uploadFile({
    url:"http://127.0.0.1:7000/v1/news/fileupload/",
    fileName:"myfile"
    });
});

$('select[data-source]').each(function() {
    var $select = $(this);
    
    $select.append('<option></option>');
    
    $.ajax({
        url: $select.attr('data-source'),
    }).then(function(options) {
        options.map(function(option) {
        var $option = $('<option>');
        
        $option
            .val(option[$select.attr('data-valueKey')])
            .text(option[$select.attr('data-displayKey')]);
        
        $select.append($option);
        });
    });
});