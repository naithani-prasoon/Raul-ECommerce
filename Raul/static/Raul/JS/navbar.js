
 function navbarFunction() {
    if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {

        document.getElementById("hideOnScroll").style.background = "transparent";
        document.getElementById("hideOnScroll").style.display = "none";
        document.getElementById("headerOnScroll").style.height = "4.5em";
        document.getElementById("headerOnScroll").style.boxShadow = "0px 0px 5px 1px black";
        
    } else {
        document.getElementById("hideOnScroll").style.display = "flex";
        document.getElementById("headerOnScroll").style.height = "7.5em";
        document.getElementById("headerOnScroll").style.background = "#6d6d6d";
        document.getElementById("headerOnScroll").style.boxShadow = "0px 0px 0px 0px";
    }
}
 
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

 function mobileDropDown() {
    document.getElementById("mobile-dropdown").classList.toggle("show");
  }


  function mobileDropDown2() {
    document.getElementById("mobile-dropdown2").classList.toggle("show");
  }

  function mobileDropDown3() {
    document.getElementById("mobile-dropdown3").classList.toggle("show");
  }

  function mobileDropDown4() {
    document.getElementById("mobile-dropdown4").classList.toggle("show");
  }

  function mobileDropDown5() {
    document.getElementById("mobile-dropdown5").classList.toggle("show");
  }

  function mobileDropDown6() {
    document.getElementById("mobile-dropdown6").classList.toggle("show");
  }


 
 

function openCity(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();

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

function openProfile(){
  document.getElementById("profileDrop").style.height = "100%";
  document.getElementById("profileDrop").style.padding = "250px 0";
}

function closeProfile(){
  document.getElementById("profileDrop").style.height = "0%";
  document.getElementById("profileDrop").style.padding = "0";
}

