
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return window.parent.document.getElementsByTagName("em").innerHTML = n;
  }
const elements = window.parent.document.getElementsByTagName('footer')
elements[0].innerHTML = "&copy;" 
elements[1].innerHTML =" <em></em>"
elements[2].innerHTML = "Omdena project"