function alternate(){
    if(document.getElementsByTagName("table") && document.getElementsByTagName("table").length > 0){
        var table = document.getElementsByTagName("table")[0];
        var rows = table.getElementsByTagName("tr");
        for(i = 0; i < rows.length; i++){
            if(i % 2 == 0){
                rows[i].className = "even"; 
            }
            else {
                rows[i].className = "odd"; 
            }
        }
    }
};

function createOption(i) {
    var option = document.createElement("option");
    option.value = cats[i][2];
    option.innerHTML = cats[i][0];
    return option
};

$(document).ready(function() {
    // create category links
    for(var i=0; i < cats.length; i++) {
        link = document.createElement("a");
        link.href = '/category/' + cats[i][1];
        link.innerHTML = cats[i][0];
        $("#cats").append(link);
        if(i != cats.length - 1) { $("#cats").append(" | ");}
    };
    var tbody = document.getElementById("posts");
    if(tbody != null) {
    // create rows of posts
    var num_posts = posts.length;
    for(var i=0; i < num_posts; i++){
        var tr = document.createElement("tr");
        var td1 = document.createElement("td");
        //if(is_admin) {
        //    td1.innerHTML = '<a href="/admin/hn/post/'+ posts[i][0] +'/">' + (25*(page_num-1) + (i+1)) +'</a>';
        //}
        //else {
        td1.innerHTML = 25*(page_num-1) + (i+1); 
        //}
        var td2 = document.createElement("td");
        var upvote = document.createElement("a");
        upvote.onclick = Function('return upvotePost(' + posts[i][0] + ')');
        upvote.id = 'v' + posts[i][0];
        upvote.href = '';
        var img = document.createElement("img");
        img.src = "/media/images/arrow2.png";
        //img.id = 'i-' + posts[i][0];
        upvote.appendChild(img);
        td2.appendChild(upvote);
        var td3 = document.createElement("td");
        td3.className = "cell";
        var post_link = document.createElement("a");
        if(posts[i][1].substring(0,22) == 'http://www.youtube.com') {
        post_link.href = posts[i][1];
        post_link.onclick = Function('return embed(this)');
        }
        else if (posts[i][1] != '') post_link.href = posts[i][1];
        else post_link.href = '/post/' + posts[i][0];
        //post_link.href=''; //new
        //post_link.target = "blank";
        post_link.innerHTML = posts[i][2];
        td3.appendChild(post_link)
        var td4 = document.createElement("td");
        td4.id = posts[i][0];
        td4.innerHTML = '+' + posts[i][3];

        var td5 = document.createElement("td");
        var comm_link = document.createElement("a");
        comm_link.href='/post/' + posts[i][0] + '#disqus_thread';
        comm_link.className = 'comm';
        var disqus_attr = document.createAttribute("data-disqus-identifier");
        disqus_attr.nodeValue = 'p-' + posts[i][0];
        comm_link.setAttributeNode(disqus_attr);
        comm_link.innerHTML = 'comments'
        td5.appendChild(comm_link);
        var span = document.createElement("span");
        span.className = "comm";
        span.innerHTML = ' by ' + '<a href="profile/'+ posts[i][4]+'">' + posts[i][4] + '</a>';
        td5.appendChild(span);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        tr.appendChild(td4);
        tr.appendChild(td5);
        tbody.appendChild(tr);
        $("#p-t").fadeIn();
    };//endfor
    //DISQUS OPTIONS
    window.disqus_shortname = 'bjjlinks'; // required: replace example with your forum shortname
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://bjjlinks.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
    }; // end if 
    // create cat options only
    var uncat = document.getElementById("uncat");
    if(uncat != null){
        $("#uncat").show();
    }
    
    //alternate row colors
    alternate();
    // fade in points
    var belt='';
    var points = parseInt($('#pts').html());
    if (points < 25) {
    belt = 'white';
    }
    else if (points >= 25 && points < 100) {
    belt = 'blue';
    }
    else if (points >= 100 && points < 500) {
    belt = 'purple';
    }
    else if (points >= 500 && points < 1000) {
    belt = 'brown';
    }
    else {
    belt = 'black';
    }
    $('#w').html($('#w').html() + 'You are a <span class="' + belt + '">'+ belt + '</span> belt.');
    $("#pts").fadeIn();
    
    //add current class to current page
    var curr = '';
    if(path == '/'){$("#home").addClass("currentHome"); }
    else if(path == '/latest') {$("#latest").addClass("current"); }
    else if(path == '/top-contributers'){ $("#top").addClass("current"); }
    else if(path == '/add-post') { $("#add_post").addClass("current");}
    else {} 
});

function createOptions(i){
    option1 = createOption(i);
    $("#id_category").append(option1);
};

function togQ(){
    $('#query').toggle();
    return false;
};

function togVid(n){
    var el = $(n);
    el.toggle();
};

function embed(node){
var hash = node.href.substring(31,42);
e = $('#'+hash);
if (e.length > 0) {
e.toggle();
return false; 
}
var url='http://www.youtube.com/v/' + hash + '?version=3';
var obj = document.createElement("object");
obj.id = hash;
obj.innerHTML = '<param name="movie" value="'+ url + '"> <param name="allowFullScreen" value="true"> <param name="allowScriptAccess" value="always"> <embed src="' + url + '" type="application/x-shockwave-flash" allowfullscreen="true" allowScriptAccess="always" width="610" height="373">';
node.parentNode.appendChild(obj);
return false;
};

$(document).ready(function() {
    openid.init('openid_identifier');
    $.ajaxSetup({
         beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                    if (document.cookie && document.cookie != '') {
                        var cookies = document.cookie.split(';');
                        for (var i = 0; i < cookies.length; i++) {
                            var cookie = jQuery.trim(cookies[i]);
                            // Does this cookie string begin with the name we want?
                            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                            }
                        }
                    }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
});

function logoutFb() {
    FB.logout(function(response) {
    return true;
    });

};

function handleFbookLogin() {
  FB.getLoginStatus(function(response) {
     if (response.session) {
        window.reload();
        alert('reloading'); }
     else {
        alert('replacing');
        window.location('{{FBREDIRECTURL}}'); // FIX THISSSS
     }
  });
};

function upvotePost(post_id) {
        if (auth) {
        var post = $('#'+post_id);
        $.ajax({
            type: "POST",
            data: ({ 'post_id': post_id }),
            url: '/post/upvote',
            success: function(response){
                // get respect td of postid and increase by one
                //var post = $('#'+post_id);
                // remove upvote button
                $('#v'+post_id).hide();
                post.fadeOut('fast', function() {
                post.html('+'+(parseInt(post.html())+1)).addClass("yellow")
                post.fadeIn('slow');
                });
                //$('#'+post_id).html(parseInt($('#'+post_id).html())+1);                
            },
            error: function(){
                alert('Could not upvote.');
            }
        });
    }
    else { alert('not auth');}
return false;
};

