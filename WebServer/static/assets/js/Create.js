

var missionName = ""; 
var missionDesc = "";
var missionType = ""; 

var header = "";
var alternatives = "";

var quiztable = "";
var missionName = "";
var missionDesc = "";
var quizsubmitstage1 = "";
var quizform = "";


function onload()
{
    alternatives = document.getElementById('alternatives');
    header = document.getElementById('id_headertext');

    quiztable = document.getElementById('id_quiztable');
    missionName = document.getElementById('id_missionname');
    missionDesc = document.getElementById('id_missiondescription');
    quizsubmitstage1 = document.getElementById('id_quizsubmitstage1');
    quizform = document.getElementById('quizform');
    
    quizform.style.display = "none";
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
    var repeats = document.getElementById('id_numberofquestions').value; 
    if(repeats < 1 || repeats > 35)
    {
        console.log(repeats);
        return;
    }
    quiztable.style.display = "none";
    quizsubmitstage1.style.display = "none";
    quizform.style.display = "table";
    var quizentry = document.getElementById('id_createquiztable');
    var i;
    for (i = 0; i < repeats; i++) 
    { 
        var node = document.createElement("LI");
        var cln = quizentry.cloneNode(true);
        node = node.appendChild(cln);
        document.getElementById('id_quizlist').appendChild(node);
    }
    // GENERATE QUIZES DEPENDING ON REPEATS
}