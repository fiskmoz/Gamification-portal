var missionType = ""; 
var articleDescription;
var uploadObj;
var id = 0;

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
        maxFileCount:1,
        afterUploadAll : function(response)
        {
            var responses = uploadObj.getResponses();
            myJson2 = {};
            myJson2['ArticleID'] = id;
            myJson2['FileID'] = responses[0].id;
            var request = $.ajax({
                url: "http://127.0.0.1:7000/v1/news/fileupload/",
                type: "PUT",
                data : myJson2,
                success : function(result)
                {
                    DisplayResults(request);
                }
            })
        }
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
    alert(JSON.stringify(myJson));
    var request = $.ajax({
        url: "http://127.0.0.1:7000/v1/news/",
        type: "POST",
        data: myJson,
        success: function(data) {
            id = data;
            uploadObj.startUpload();
        }
        });
}