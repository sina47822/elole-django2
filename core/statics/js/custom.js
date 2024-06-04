function changePage(page_number) {
    let current_url_params = new URLSearchParams(window.location.search)
    current_url_params.set("page", page_number)
    let new_url = window.location.pathname + "?" + current_url_params.toString()
    window.location.href = new_url
}

function formatPriceInToman(element) {
    let rawPrice = parseFloat(element.innerText);
    let formatter = new Intl.NumberFormat('fa-IR');
    let formattedPrice = formatter.format(rawPrice);
    element.innerText = `${formattedPrice} تومان`;
}

document.addEventListener("DOMContentLoaded", function() {
    let priceElements = document.querySelectorAll('.formatted-price');
    priceElements.forEach(element => formatPriceInToman(element));
});

$(document).ready(function() {
    $("#news-slider").owlCarousel({
        items : 6,
        itemsDesktop:[1199,6],
        itemsDesktopSmall:[980,3],
        itemsMobile : [600,1],
        navigation:true,
        navigationText:["",""],
        pagination:true,
        autoPlay:true,
        rtl: true,
        autoplay:true, 
        autoplayTimeout:6000,
        autoplayHoverPause:true, 
        animateOut: 'fadeOut',
  
    });
  });
  $(document).ready(function() {
    $("#news-slider-2").owlCarousel({
        items : 6,
        itemsDesktop:[1199,6],
        itemsDesktopSmall:[980,3],
        itemsMobile : [600,1],
        navigation:true,
        navigationText:["",""],
        pagination:true,
        autoPlay:true,
        rtl: true,
        autoplay:true, 
        autoplayTimeout:4000,    
        autoplayHoverPause:true, 
        animateOut: 'fadeOut',
  
    });
  });
  
  $(document).ready(function(){
  
     $('.pks_slider').owlCarousel({
      margin:0,
      autoplay:true, 
      autoplayTimeout:1500,    
      autoplayHoverPause:false, 
      animateOut: 'fadeOut',
      // animateIn: 'fadeIn',
      loop:true,   
      nav:false,   
      items: 1,  
      rtl: true,  
       
    })
  });