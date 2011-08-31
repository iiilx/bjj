$(document).ready(function() {
  // Code adapted from http://djangosnippets.org/snippets/1389/
 
function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
 replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
  }
 
  function deleteForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    //alert('formcount = ' + formCount);
    if (formCount > 1) {
      // Delete the item/form
      $(btn).parents('.' + prefix).remove();
 
      var forms = $('.' + prefix); // Get all the forms
        //alert(forms.length); 
      // Update the total number of forms (1 less than before)
      $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
 
      var i = 0;
      // Go through the forms and set their indices, names and IDs
      for (formCount = forms.length; i < formCount; i++) {
        $(forms.get(i)).children().children().each(function() {
          if ( $(this).attr('type') == 'text' )
            updateElementIndex(this, prefix, i);
        });
      }
 
    } // End if
    else {
        alert("You have to enter at least one "+prefix+"!");
    }
    return false;
  }
 
  function addForm(btn, prefix) {
    //alert(prefix);
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    //alert(formCount); 
    if (formCount < max_choices) {
      // Clone a form (without event handlers) from the first form
      var row = $("."+prefix+":first").clone(false).get(0);
      // Insert it after the last form
      $(row).append('<p class="left_wide"><a class="delete" href="#">remove</a></p>')
      $(row).removeAttr('id').hide().insertAfter("."+prefix+":last").addClass("dot-top").slideDown(300);
 
      // Remove the bits we don't want in the new row/form
      // e.g. error messages
      $(".errorlist", row).remove();
      $(row).children().removeClass("error");
 
      // Relabel or rename all the relevant bits
      $(row).children().children().each(function() {
        updateElementIndex(this, prefix, formCount);
        $(this).val("");
      });
 
      // Add an event handler for the delete item/form link
      $(row).find(".delete").click(function() {
        return deleteForm(this, prefix);
      });
 
      // Update the total form count
      $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1); 
 
    } // End if
    else {
        var ending = ''; 
        if(prefix[prefix.length-1] == 's'){ 
            ending = 'es' 
        } 
        else {
            ending = 's'
        };
        alert("Sorry, you can only enter a maximum of " + max_choices + ' ' + prefix + ending + ".");
    }
    return false;
  }
 
  // Register the click event handlers
  $(".add").click(function() {
    var prefix = $(this).parent().next().next().next().next().attr('class').split(" ")[0];//$(this).parent().prev().attr("class")
    return addForm(this, prefix);

  });
 
  $(".delete").click(function() {
    var prefix = $(this).parent().parent().attr("class");
    return deleteForm(this, prefix);
  });
 
});

function show_reply_form(comment_id, parent_id) {
    var comment_reply = $('#' + comment_id);
    var to_add = $('<div class="response"></div>');
    var form = $('#c_form').clone();
    form.attr("id",'form'+comment_id);
    var input = form.find('input#id_parent');
    input.val(parent_id);
    to_add.append(form);
    to_add.css("display", "none");
    comment_reply.after(to_add);
    to_add.slideDown(function() {
        comment_reply.replaceWith(new Array('<a id="',
        comment_id,'" href="javascript:hide_reply_form(\'',
        comment_id, '\')">Stop Replying</a>').join(''));
    });
}

function hide_reply_form(comment_id, url) {
    var comment_reply = $('#' + comment_id);
    comment_reply.next().slideUp(function (){
        comment_reply.next('.response').remove();
        comment_reply.replaceWith(new Array('<a id="',
        comment_id,'" href="javascript:show_reply_form(\'',
        comment_id, '\')">Reply</a>').join(''));
    });
}

$(document).ready(function() {
$("#p-t tr").hover(
   function()
   {
    $(this).addClass("highlight");
   },
   function()
   {
    $(this).removeClass("highlight");
   }
  )
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
    
    if (typeof post_url !== 'undefined' && (post_url.substring(7,22) == 'www.youtube.com' || post_url.substring(7,15) == 'youtu.be')) {
       embed(post_url);
    }; 
    //add current class to current page
    var curr = '';
    if(path == '/'){$("#home").addClass("currentHome"); }
    else if(path == '/latest') {$("#latest").addClass("current"); }
    else if(path == '/top-contributers'){ $("#top").addClass("current"); }
    else if(path == '/add-post') { $("#add_post").addClass("current");}
    else if(path == '/search/') {$("#search").addClass("current");}
    else if(path == '/poll/') {$("#poll").addClass("current");}
    else if(path == '/login') {$("#login").addClass("current");}
    else {} 

    if(typeof page_num !== 'undefined' && page_num > 0) {
    for(var i=0; i<25; i++) {
    $('table#p-t tbody tr:nth-child('+ (i+1) +') td:first-child').html((25*(page_num-1) + (i+1))); 
    };
    //DISQUS OPTIONS
    window.disqus_shortname = 'bjjlinks'; // required: replace example with your forum shortname
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = 'http://bjjlinks.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
    };
});


function togQ(){
    $('#query').toggle();
    return false;
};

function togVid(n){
    var el = $(n);
    el.toggle();
};

function embed(url){
    var hash='';
    if (url.substring(7,22) == 'www.youtube.com') {
        var x = url;
        x=x.replace('feature=player_embedded&','');
        hash=x.substring(31,42);
    }
    else {
        hash=url.substring(16,url.length);
    }
    var curl='http://www.youtube.com/v/' + hash + '?version=3';
    var obj = document.createElement("object");
    obj.setAttribute('class','obj');
    obj.setAttribute('width', '640');
    obj.setAttribute('height', '390');
    obj.innerHTML = '<param name="movie" value="'+ curl + '"> <param name="allowFullScreen" value="true"> <param name="allowScriptAccess" value="always"> <embed src="' + curl + '" type="application/x-shockwave-flash" allowfullscreen="true" allowScriptAccess="always" width="640" height="390">';
    div=document.createElement("div");
    div.setAttribute('class','center')
    div.appendChild(obj)
    $('#ti').after($(div));    
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
                // remove upvote button
                if(response=='2') { alert('You already voted on this.');}
                else {post.fadeOut('fast', function() {
                    post.html('+'+(parseInt(post.html())+1)).addClass("yellow")
                    post.fadeIn('slow');
                    });
                }
                $('#v'+post_id).hide();
                //$('#'+post_id).html(parseInt($('#'+post_id).html())+1);                
            },
            error: function(){
                alert('Could not upvote.');
            }
        });
    }
    else { alert('You must login to vote');}
return false;
};

