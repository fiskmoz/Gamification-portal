

var missionName = ""; 
var missionDesc = "";
var missionType = ""; 

var header = "";
var alternatives = "";

var quiztable = "";
var missionName = "";
var missionDesc = "";
var quizsubmitstage1 = "";


function onload()
{
    alternatives = document.getElementById('alternatives');
    header = document.getElementById('id_headertext');

    quiztable = document.getElementById('id_quiztable');
    missionName = document.getElementById('id_missionname');
    missionDesc = document.getElementById('id_missiondescription');
    quizsubmitstage1 = document.getElementById('id_quizsubmitstage1');
    quiztable.style.display = "none";
    quizsubmitstage1.style.display = "none";
}

function validate(name)
{
    missionType = name; 

    // CHECK IF MISSION NAME IS UNIQUE
    alternatives.style.display = 'none';
    switch(missionType)
    {
        case "quiz": 
            quiz();
        break; 
    }
}

function quiz()
{
    quiztable.style.display = "table";
    quizsubmitstage1.style.display ="block";
    header.innerHTML = "You have chosen: " + missionType;
    
}

function quizstage1()
{
    // CHECK MISSION NAME UNIQUE
    var repeatsString = document.getElementById('id_numberofquestions'); 
    var repeats = parseInt(repeatsString + "<br>");
    if(repeats < 1 || repeats > 35)
    {
        return;
    }
    quiztable.style.display = "none";
    quizsubmitstage1.style.display = "none";
    // GENERATE QUIZES DEPENDING ON REPEATS
}