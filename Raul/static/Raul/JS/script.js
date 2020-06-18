
 var mybutton = document.getElementById("scrollTop");

 window.onscroll = function() {scrollFunction(),navbarFunction()};

 function scrollFunction() {
     if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
         mybutton.style.display = "block";
     } else {
         mybutton.style.display = "none";
     }
 }

 function topFunction() {
     document.body.scrollTop = 0;
     document.documentElement.scrollTop = 0;
 }

 
 function navbarFunction() {
    if (document.body.scrollTop > 40 || document.documentElement.scrollTop > 40) {
        document.getElementById("hideOnScroll").style.display = "none";
        document.getElementById("headerOnScroll").style.height = "4.5em";
        document.getElementById("headerOnScroll").style.borderBottom = "0.5px solid white";
    } else {
        document.getElementById("headerOnScroll").style.height = "7.5em";
        document.getElementById("hideOnScroll").style.display = "flex";
        document.getElementById("headerOnScroll").style.borderBottom = "0px";
        
    }
}

 function openNav() {
     document.getElementById("contentHam").style.height = "100%";
 }

 function closeNav() {
     document.getElementById("contentHam").style.height = "0%";
 }

 function openStore(){
     document.getElementById("store").style.height = "100%";
 }

 function closeStore(){
     document.getElementById("store").style.height = "0%";
 }

