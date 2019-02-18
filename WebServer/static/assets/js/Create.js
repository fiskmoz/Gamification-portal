var missionType = ""; 


function onload()
{
    // missionName = document.getElementById('id_missionname');
    // missionDesc = document.getElementById('id_missiondescription');
    document.getElementById('quizform').style.display = "none";
    document.getElementById('id_quiztable').style.display = "none";
    document.getElementById('id_quizsubmitstage1').style.display = "none";
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
    document.getElementById('id_headertext').innerHTML = "You have chosen: " + missionType;
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
    // CHECK MISSION NAME UNIQUE
    var repeats = document.getElementById('id_numberofquestions').value; 
    alert(repeats);
    if(repeats < 1 || repeats > 35)
    {
        console.log(repeats);
        return;
    }
    document.getElementById('id_quiztable').style.display = "none";
    document.getElementById('id_quizsubmitstage1').style.display = "none";
    document.getElementById('quizform').style.display = "table";
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

function quizstage2()
{
    var data = $('quizform').serialize();
    $.post('url', data,);
}