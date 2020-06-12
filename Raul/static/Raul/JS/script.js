
 var mybutton = document.getElementById("scrollTop");

 window.onscroll = function() {scrollFunction()};

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

 function openCategory(){
     document.getElementById("category").style.height = "20%";
 }

 function closeCategory(){
     document.getElementById("category").style.height = "0%";
 }
