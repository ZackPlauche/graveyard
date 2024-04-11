var toggle = document.querySelector(".toggle");
var links = document.querySelector(".navbar").querySelector(".nav-links").getElementsByTagName("li");

for (i = 0; i < links.length; i++) {
    links[i].onclick = function() {
        if (toggle.checked === false) {
            toggle.checked = true;
        } else {
            toggle.checked = false;
        };

    };
};