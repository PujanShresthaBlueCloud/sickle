
// function insertParagraph(){
//     var newElement = window.parent.document.createElement("p");
//     // var node = document.createTextNode("new text");
//     // newElement.appendChild(node);
//     var element = window.parent.document.getElementsByTagName("footer");
//     element.appendChild(newElement);
// }
function todayDate(){
    var d = new Date();
    var n = d.getFullYear() + "  ";
    return n;
  }
  

// var newElement = window.parent.document.createElement('p');
const elements = window.parent.document.getElementsByTagName('footer');
elements[0].innerHTML = "&copy; Omdena project";
elements[0].appendChild(window.parent.document.createElement('p'));
const date_element = window.parent.document.getElementsByTagName('p');
date_element[0].innerHTML = new Date();
// const element = window.parent.document.getElementsByTagName('footer');
// element[0].appendChild(window.parent.document.createElement('p'));
// window.parent.document.getElementsByTagName('p').innerHTML = todayDate()

