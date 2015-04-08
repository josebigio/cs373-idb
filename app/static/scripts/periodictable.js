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
for(var i=0; i< l.length; i++){
    var element = l[i];
    if (element.className == 'empty'){
        continue;
    } else {
        element.onclick = onClick(element);
    }
}

function onClick(element){
    return function () {
        var substring = element.innerHTML.split('<span>');
        var elementName = substring[1];
        elementName = elementName.replace("</span>", "").toLowerCase();

    window.open("element/"+ elementName, "_self");
    }

}
