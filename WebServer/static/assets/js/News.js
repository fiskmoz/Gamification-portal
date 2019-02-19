var newsType = "";
var newsArticle ="";
var filePath = "";
var contentArray = [];

function onload()
{
    document.getElementById('chooseFile').style.display = "none";
}
function validate(name)
{
    newsType = name; 

    // CHECK IF MISSION NAME IS UNIQUE
    alternatives.style.display = 'none';
    switch(newsType)
    {
        case "createNews": 
            createNews();
            break;
        case "news":
            news();
        break; 
    }
}

function createNews()
{
    document.getElementById('chooseFile').style.display = "table";
}

function uploadnews()
{
    var photo = document.getElementById('newsFile');
    var file = photo.files[0];
    alert(file.fileName);


    console.log("File name: " + file.fileName);
    console.log("File size: " + file.fileSize);
    console.log("Binary content: " + file.getAsBinary());
    console.log("Text content: " + file.getAsText(""));
    
    // var myJson = {};
    // myJson['newsArticleName'] = document.getElementById('newsName');
    // myJson['fileToUpload'] = document.getElementById('newsFile').files[0];;


    // var request = $.ajax({
    //     url: "http://127.0.0.1:7000/v1/news/",
    //     type: "POST",
    //     data: myJson
    // });

    // request.done(function(msg) {
    //     alert("Request successfull!");
    //     window.location.replace("http://127.0.0.1:8000/");
    // });
    
    // request.fail(function(jqXHR, textStatus) {
    //     alert( "Request failed :( " + " IT MIGHT STILL WORK THO" );
    //     window.location.replace("http://127.0.0.1:8000/");
    // });
}