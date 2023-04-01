const elements = window.parent.document.getElementsByTagName('footer');
elements[0].innerHTML = "&copy; Omdena project " + new Date().getFullYear();

const manageTerminal = window.parent.document.getElementsByClassName('styles_terminalButton__3xUnY');
manageTerminal[0].innerHTML = "hello"