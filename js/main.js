
function insertParagraph(){
    var newElement = window.parent.document.createElement("p");
    // var node = document.createTextNode("new text");
    // newElement.appendChild(node);
    var element = window.parent.document.getElementsByTagName("footer");
    element.appendChild(newElement);
}
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return window.parent.document.getElementsByTagName('p').innerHTML=n;
  }
const elements = window.parent.document.getElementsByTagName('footer')
elements[0].innerHTML = "&copy; Omdena project"
insertParagraph()
