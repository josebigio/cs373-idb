// Jumbotron stuff
var jumboHeight = $('.jumbotron').outerHeight();
        function parallax(){
            var scrolled = $(window).scrollTop();
            $('.bg').css('height', (jumboHeight-scrolled) + 'px');
        }

        $(window).scroll(function(e){
            parallax();
        });


// Sidebar stuff
$('#sidebar').affix({
      offset: {
        top: 245
      }
});

var $body   = $(document.body);
var navHeight = $('.navbar').outerHeight(true) + 10;

$body.scrollspy({
	target: '#leftCol',
	offset: navHeight
});