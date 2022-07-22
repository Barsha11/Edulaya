

// Header fixed function
$(function() {
    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        if (scroll >= 10) {
            $("header").addClass('stickytop');
        } else {
            $("header").removeClass("stickytop");
        }
    });
  
   $('#nav').onePageNav({
        currentClass: 'current',
        changeHash: false,
        scrollSpeed: 1000,
    });
  
   $('#mobile-nav').onePageNav({
        currentClass: 'current',
        changeHash: false,
        scrollSpeed: 1000,
    });
  
   $(".mobile-menu ul>li").click(function(){
      setTimeout(function(){
        $("body").removeClass("pushy-open-left");
      }, 1000);
    });

});

$(function() {
    $('.iframe-link').magnificPopup({
     type:'iframe'
    });
});

  
// Work Carousel
    $('.banner-text').owlCarousel({
      items:1,
      margin:15,
      loop:true,
      dots:true,
      autoplay:true,
      smartSpeed:2500, 
      nav: false,
    });


// Course Carousel
$('.courses-slider').owlCarousel({
    items:4,
    margin:15,
    // loop:true,
    dots:false,
    autoHeight:true,
    autoplay:true,
    smartSpeed:2500, 
    nav: true,
    navText: ["<span><i class='fas fa-arrow-left'></i></span>","<span><i class='fas fa-arrow-right'></i></span>"],
    responsive: {
            0: {
                items: 1
            },
            480: {
                items: 1,
            },
            768: {
                items: 2,
            },
            992: {
                items:3,
            },
            1200:{
              items:4,
            },
            1355:{
              items:4,
            },
            1600:{
                items:4
            }
          }, 
  });