
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return document.getElementById("date").innerHTML = n;
  }
const elements = window.parent.document.getElementsByTagName('footer')
elements[0].innerHTML = "&copy; <em id='"+data+"'></em>Omdena project"