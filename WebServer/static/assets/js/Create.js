var missionType = ""; 
var myTableArray = [];
var repeats = 0;

function onload()
{
    // missionName = document.getElementById('id_missionname');
    // missionDesc = document.getElementById('id_missiondescription');
    document.getElementById('quizform').style.display = "none";
    document.getElementById('id_quiztable').style.display = "none";
    document.getElementById('id_quizsubmitstage1').style.display = "none";
    document.getElementById('id_quizsubmitstage2').style.display = "none";
}

function validate(name)
{
    missionType = name; 
    // CHECK IF MISSION NAME IS UNIQUE
    document.getElementById('alternatives').style.display = 'none';
    switch(missionType)
    {
        case "quiz": 
            quiz();
        break; 
    }
}

function quiz()
{
    document.getElementById('id_quiztable').style.display = "table";
    document.getElementById('id_quizsubmitstage1').style.display ="block";
    document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType;
}

function view()
{
    const inputOptions = new Promise((resolve) => {
          resolve({
            'A': 'A',
            'B': 'B',
            'C': 'C'
          })
      })
      

    const {value: answer} =  Swal.mixin({
    input: 'radio',
    confirmButtonText: 'Next &rarr;',
    progressSteps: ['1', '2', '3'],
    inputOptions: inputOptions,
    inputValidator: (answer) => {
      return !answer && 'You need to choose something!'
    }
    }).queue([
    {
        title: 'Is chaining easy?',
        text: 'A: yes! B: no! C: none of above'
    },
    'Question 2',
    'Question 3'
    ]).then((result) => {
    if (result.value) {
        Swal.fire({
        title: 'All done!',
        html:
            'Your answers: <pre><code>' +
            JSON.stringify(result.value) +
            '</code></pre>',
        confirmButtonText: 'Lovely!'
        })
    }
    })
}

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE¨
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
    document.getElementById('id_quiztable').style.display = "none";
    document.getElementById('id_quizsubmitstage1').style.display = "none";
    document.getElementById('quizform').style.display = "table";
    // var quizentry = document.getElementById('id_quizlistelement');

    // var i;
    // for (i = 0; i < repeats-1; i++) 
    // { 
    //     var cln = quizentry.cloneNode(true);
    //     document.getElementById('id_quizlist').appendChild(cln);
    // }
    document.getElementById('id_quizsubmitstage2').style.display = "block";
    // GENERATE QUIZES DEPENDING ON REPEATS
}

function quizstage2()
{
    var question = document.getElementById("id_quizquestion");
    var A = document.getElementById("id_aswereA");
    var B = document.getElementById("id_aswereB");
    var C = document.getElementById("id_aswereC");
    var correct = document.getElementById("id_correctanswer");

    myTableArray.push(question.value);
    myTableArray.push(A.value);
    myTableArray.push(B.value);
    myTableArray.push(C.value);
    myTableArray.push(correct.value);

    question.value = "";
    A.value = "";
    B.value = "";
    C.value = "";
    $('input[name=correctanswer]').attr('checked',false);

    // alert(myTableArray);

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
        alert(myJson);
        var request = $.ajax({
        url: "http://127.0.0.1:7000/v1/quiz/",
        type: "POST",
        data: myJson
        });
        
        request.done(function(msg) {
            alert("Request successfull!");
            window.location.replace("http://127.0.0.1:8000/");
        });
        
        request.fail(function(jqXHR, textStatus) {
            alert( "Request failed :( " + " IT MIGHT STILL WORK THO" );
            window.location.replace("http://127.0.0.1:8000/");
        });
    }
    document.getElementById('id_headertext').innerHTML = repeats.toString() + " questions left!";

    // var repeats = document.getElementById('id_numberofquestions').value; 
    // for (i = 0; i < repeats-1; i++) 
    // { 
    //     $("table#id_createquiztable tr").each(function() {
    //         // var arrayOfThisRow = [];
    //         // var tableData = $(this).find('td');
    //         // if (tableData.length > 0) {
    //         //     tableData.each(function() { arrayOfThisRow.push($(this).text()); });
    //         //     myTableArray.push(arrayOfThisRow);
    //         // }

    //     })
    // }
        



    

    // var data = $('quizform').serialize();
    // alert(data);
    // var json_text = JSON.stringify(document.getElementById('quizform'), null, 2);
    // // alert(json_text);
    // // $.post('http://127.0.0.1:7000/v1/quiz', data,);

    // var request = $.ajax({
    //     url: "http://127.0.0.1:7000/v1/quiz/",
    //     type: "POST",
    //     data: myTableArray
    //   });
      
    //   request.done(function(msg) {
    //     $("#log").html( msg );
    //   });
      
    //   request.fail(function(jqXHR, textStatus) {
    //     alert( "Request failed: " + textStatus );
    //   });
}