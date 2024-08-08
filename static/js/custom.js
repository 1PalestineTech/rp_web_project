// ===== Scroll to Top ==== 
$(window).scroll(function () {
    if ($(this).scrollTop() >= 50) { // If page is scrolled more than 50px
        $('#return-to-top').fadeIn(200); // Fade in the arrow
    } else {
        $('#return-to-top').fadeOut(200); // Else fade out the arrow
    }
});
$('#return-to-top').click(function () {
    // When arrow is clicked

    $('body, html').animate({
        scrollTop: 0 // Scroll to top of body
    }, 500);
});
function change_nav(){

const url = window.location.href
const capturingRegex = /http:\/\/localhost:5000\/(?<id>[A-Z]*).*/i;
const found = url.match(capturingRegex);

const ID = found.groups.id || 'index';
const element=document.getElementById(ID);
element.classList.add("active");

}
change_nav();