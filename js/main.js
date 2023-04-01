
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return n;
  }
const elements = window.parent.document.getElementsByTagName('footer')
elements[0].innerHTML = "&copy; Omdena project <em></em>" 
const date = window.parent.document.getElementsByTagName("em")
date[0] = todayDate()