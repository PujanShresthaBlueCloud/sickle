
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return window.parent.document.getElementsByTagName("em").innerHTML = n;
  }
const elements = window.parent.document.getElementsByTagName('footer')
elements[0].innerHTML = "&copy; Omdena project" 
elements[1].innerHTML = todayDate()
