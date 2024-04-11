// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {
    37: 1,
    38: 1,
    39: 1,
    40: 1
}
var toggle = document.querySelector('.mobile-menu-toggle');
var links = document.querySelector('.navbar-menu').querySelectorAll('.nav-link');
var body = document.body


function closeMobileMenu() {
    if (toggle.checked === true) {
        toggle.checked = false;
        enableScroll()
    }
};

for (i = 0; i < links.length; i++) {
    links[i].onclick = closeMobileMenu
}

toggle.onclick = function () {
    if (toggle.checked === true) {
        disableScroll()
    } else {
        enableScroll()
    }
}

function disableScroll() {
    window.addEventListener('DOMMouseScroll', preventDefault, false);
    window.addEventListener(wheelEvent, preventDefault, wheelOpt);
    window.addEventListener('touchmove', preventDefault, wheelOpt);
    window.addEventListener('keydown', preventDefaultForScrollKeys, false);
}

function enableScroll() {
    window.removeEventListener('DOMMouseScroll', preventDefault, false);
    window.removeEventListener(wheelEvent, preventDefault, wheelOpt);
    window.removeEventListener('touchmove', preventDefault, wheelOpt);
    window.removeEventListener('keydown', preventDefaultForScrollKeys, false);
}

function preventDefault(e) {
    e.preventDefault();
}

function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
        preventDefaultForScrollKeys(e);
        return false;
    }
}
// modern Chrome requires { passive: false } when adding event
var supportsPassive = false;

try {
    window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
        get: function () {
            supportsPassive = true;
        }
    }));
} catch (e) {}

var wheelOpt = supportsPassive ? {
    passive: false
} : false;

var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';

