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
            document.getElementById('section1').classList.remove('hidden');
            document.getElementById('id_headertext').innerHTML = "You have chosen a " + missionType;
        break; 
    }
}

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE¨
    document.getElementById('section1').classList.add('hidden');
    document.getElementById('section2').classList.remove('hidden');
    
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
        
        // request.done(function(msg) {
        //     alert("Request successfull!");
        //     window.location.replace("http://127.0.0.1:8000/");
        // });
        
        // request.fail(function(jqXHR, textStatus) {
        //     alert( "Request failed :( " + " IT MIGHT STILL WORK THO" );
        //     window.location.replace("http://127.0.0.1:8000/");
        // });

        Swal.fire({
            title: 'Saved successfully!',
            type: 'success',
            showCancelButton: false,
          }).then(() => {
            window.location.replace("http://127.0.0.1:8000/");
          })
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