let leftbar: HTMLElement | null = document.getElementById("leftbar");
let rightbar: HTMLElement | null = document.getElementById("rightbar");
let topbar: HTMLElement | null = document.getElementById("topbar");
let bod: HTMLElement | null = document.getElementById("restofbody");

function inIframe(): boolean {
    try {
        return window.self !== window.top;
    } catch (e) {
        return true;
    }
}

if (inIframe()) {
    leftbar.style.display = "none";
    rightbar.style.display = "none";
    topbar.style.display = "none";
} else {
    bod.style.marginLeft = "150px";
    bod.style.marginRight = "150px";
    bod.style.marginTop = "25px";
}