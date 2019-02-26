var missionType = ""; 
var myTableArray = [];
var repeats = 0;

function validate(name)
{
    missionType = name; 
    // CHECK IF MISSION NAME IS UNIQUE
    document.getElementById('alternatives').style.display = 'none';
    switch(missionType)
    {
        case "quiz": 
            document.getElementById('quiz_section1').classList.remove('hidden');
            document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType;
            break;
        case "article":
            document.getElementById("news_article").classList.remove('hidden');
            document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType;
        break; 
    }
}

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE¨
    document.getElementById('quiz_section1').classList.add('hidden');
    document.getElementById('quiz_section2').classList.remove('hidden');

    name = document.getElementById('id_missionname').value;
    desc = document.getElementById('id_missiondescription').value;
    repeats = document.getElementById('id_numberofquestions').value; 
    myTableArray.push(name);
    myTableArray.push(desc);
    myTableArray.push(repeats);

    if(repeats < 1 || repeats > 35)
    {
        console.log(repeats);
        return;
    }
    document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType + " with " + repeats.toString() + " questions!";
    document.getElementById('quizform').style.display = "table";
}

function quizstage2()
{
    myTableArray.push(document.getElementById("id_quizquestion".value));
    myTableArray.push(document.getElementById("id_aswereA").value);
    myTableArray.push(document.getElementById("id_aswereB").value);
    myTableArray.push(document.getElementById("id_aswereC").value);
    myTableArray.push(document.getElementById("id_correctanswer").value);

    document.getElementById("id_quizquestion").value = "";
    document.getElementById("id_aswereA").value = "";
    document.getElementById("id_aswereB").value = "";
    document.getElementById("id_aswereC").value = "";
    $('input[name=correctanswer]').attr('checked',false);

    repeats = repeats -1;
    $(window).scrollTop(0);
    if(repeats <= 0)
    {
        var myJson = {};
        myJson['Quizname'] = myTableArray[0];
        myJson['Description'] = myTableArray[1];
        myJson['Size'] = myTableArray[2];
        var i;
        for(i=3; i<myTableArray.length;i++)
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
    else 
    {
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
          document.getElementById('id_headertext').innerHTML = repeats.toString() + " questions left!";
    }
}

function submitArticle()
{
    var myJson = {};
    myJson["ArticleTitle"] = document.getElementById('articleTitle').value;
    myJson["ArticleDescription"] = document.getElementById('articleDesc').value;
    myJson["ArticleQuiz"] = $('select#quizSelection option:selected').val();

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