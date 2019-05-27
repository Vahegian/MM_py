
function stopRightClick(){
    document.addEventListener('contextmenu', event => event.preventDefault());
}

function isWindowClosed() {
    if (window.closed) { 
        console.log("yes")
        {{ exit }}		
    } else {
        console.log("no")		
  }
    
}

function checkIfWindowClosed(){
    windowClosed = setInterval(isWindowClosed, 1000);
}