var missionType = ""; 
var articleDescription;
var uploadObj;


$(document).ready(function()
{
    articleDescription = new Quill('#articleDescription', {
        theme: 'snow'
    });
    uploadObj = $("#fileuploader").uploadFile({
        allowedTypes:"jpg,txt,pdf,docx",
        url:"http://127.0.0.1:7000/v1/news/fileupload/",
        autoSubmit:false,
        fileName:"myfile",
        maxFileCount:1
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
});

function submitArticle()
{
    var myJson = {};
    var linkItems = {};
    myJson["ArticleTitle"] = $('#articleTitle').val(); 
    myJson["ArticleDescription"] = articleDescription.container.innerHTML;
    myJson["ArticleQuiz"] = $('select#quizSelection option:selected').val();
    
    uploadObj.startUpload();

    alert(JSON.stringify(myJson));
    var request = $.ajax({
        url: "http://127.0.0.1:7000/v1/news/",
        type: "POST",
        data: myJson
        });

    DisplayResults(request);
}