const elements = window.parent.document.getElementsByTagName('footer');
elements[0].innerHTML = "&copy; Omdena project " + new Date().getFullYear();

const manageTerminal = window.parent.document.getElementsById('manage-app-button');
manageTerminal.classList.remove('styles_terminalButton__3xUnY')