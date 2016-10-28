/**
 * Created by samuel on 10/27/16.
 */

$(document).ready(function(){
    get_body();
});

function clear_content(){
    while ($('#content').firstChild){
        $('#content').removeChild($('#content').firstChild)
    }
    $('#content').text('');
}

function get_body(){
    $('#content').text("There is nothing to see here. Would you like to make some changes?");
    $('#content').append('<br><br><l onclick=edit()>&lt;Edit&gt;</edit>');

    var params = '?url=' + encodeURIComponent(window.location.href) + '&tex=False';

    var http = new XMLHttpRequest();
    http.open("GET", '/_request'+params, true);
    http.onreadystatechange = function()
    {
        if(http.readyState == 4 && http.status == 200) {
            if (http.responseText!='0'){
                render_body(http.responseText);
            }
        }
    };
    http.send();
}

function render_body(text){
    clear_content();

    $('#content').append(text);
    $('#content').append('<br><br><l onclick=edit()>&lt;Edit&gt;</edit>')
}

function edit(){
    var url = "/_request";
    var params = '?url=' + encodeURIComponent(window.location.href) + '&tex=True';
    var http = new XMLHttpRequest();
    http.open("GET", url+params, true);
    http.onreadystatechange = function()
    {
        if(http.readyState == 4 && http.status == 200) {
            render_tex(http.responseText);
        }
    };
    http.send();
}

function render_tex(tex){
    clear_content();
    $('#content').append('<textarea id="text"></textarea>');
    $('#content').append('<button id="submit" onclick="submit()">Submit Changes</button>');
    $('#content').append('<button id="submit" onclick="cancel()">Cancel</button>');

    if (tex=='0'){
        $('textarea').val('placeholder')
    }else{
        $('textarea').val(tex)
    }

}

function submit(){
    var http = new XMLHttpRequest();
    http.open('POST', '/_post/', true);
    http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    http.onreadystatechange = function(){
        if(http.readyState == 4 && http.status == 200) {
            if (http.responseText!='0'){
                render_body(http.responseText);
            }
        }
    };

    var vars = 'url=' + encodeURIComponent(window.location.href) +
                   '&tex=' +  encodeURIComponent($('textarea').val());
    
    http.send(vars);
}

function cancel(){
    clear_content();
    get_body();
}