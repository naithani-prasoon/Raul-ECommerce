
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
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
        document.getElementById("hideOnScroll").style.color = "white";
        document.getElementById("categoryP").style.opacity = "1";
        document.getElementById("headerOnScroll").style.height = "7.5em";
        document.getElementById("headerOnScroll").style.background = "#333333";
        document.getElementById("headerOnScroll").style.boxShadow = "0px 0px 5px 1px black";
        
    } else {
        document.getElementById("hideOnScroll").style.background = "transparent";
        document.getElementById("categoryP").style.opacity = "0";
        document.getElementById("hideOnScroll").style.color = "transparent";
        document.getElementById("headerOnScroll").style.background = "transparent";
        document.getElementById("headerOnScroll").style.height = "7.5em";
        document.getElementById("headerOnScroll").style.boxShadow = "0px 0px 0px 0px";
        
        
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

