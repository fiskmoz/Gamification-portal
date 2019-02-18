var newsType = "";

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
    
}