
$(document).ready(function(){

    $('#sub-button').click(function(e) {
        let $btn = $(this);
        $('#result').empty();

        $btn.button('loading');
        let text = $("#comment").val().toString();
        console.log(text);
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = response;
        xhttp.open("POST", "http://127.0.0.1:5000/text", true);
        xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xhttp.send(text);
    });
});


function response() {


    if (this.readyState === 4 && this.status === 200) {
        let images = JSON.parse(this.responseText);
        $('#sub-button').button('reset');
        for (let image of images) {
            console.log(image);
            $('#result').append(
                "<div class=\"col-md-3 col-sm-6 mb-4\">" +
                "<a href=\"#\">" +
                "<img class=\"img-fluid\" src=\"http://127.0.0.1:5000/image/"+ image +"\"  alt=\"\"></a>" +
                "</div>");
        }
    }



}

