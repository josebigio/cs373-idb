/**
 * Created by tehreemsyed on 3/26/15.
 */
 $(function(){
    $('li[class^="type-"]').mouseover(function(){
      var currentClass = $(this).attr('class').split(' ')[0];
      if(currentClass != 'empty'){
      	$('.main > li').addClass('deactivate');
      	$('.' + currentClass).removeClass('deactivate');
      }
    });

   $('li[class^="cat-"]').mouseover(function(){
      var currentClass = $(this).attr('class').split(' ')[0];
      	$('.main > li').addClass('deactivate');
      	$('.' + currentClass).removeClass('deactivate');
    });

    $('.main > li').mouseout(function(){
      var currentClass = $(this).attr('class').split(' ')[0];
       $('.main > li').removeClass('deactivate');
    });

});

var l = document.getElementById('periodic-table').getElementsByTagName('li');
var l2 = document.getElementById('lanthanide-actinide').getElementsByTagName('li');
for(var i=0; i< l.length; i++){
    var element = l[i];
    if (element.className == 'empty'){
        continue;
    } else {
        element.onclick = onClick(element);
    }
}
for(var i=0; i< l2.length; i++){
    var element = l2[i];
    if (element.className == 'empty'){
        continue;
    }

    else {
        element.onclick = onClick(element);
    }
}


function onClick(element){
    return function () {
        var substring = element.innerHTML.split('<span>');
        var elementName = substring[1];
        elementName = elementName.replace("</span>", "").toLowerCase();

        var dataPosition = element.getAttribute("data-pos");
        if(dataPosition == '57-71')
             window.open("group/8", "_self");
        else if(dataPosition == '89-103')
            window.open("group/9","_self");
        else
            window.open("element/"+ dataPosition, "_self");
    }


}
