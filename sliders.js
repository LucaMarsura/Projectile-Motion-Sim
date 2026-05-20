const checkbox = document.getElementById("bool_ivelocity");
const slider = document.getElementById("ivelocity");

checkbox.addEventListener("change", function () {

    if (checkbox.checked) {
        slider.removeAttribute("disabled");
    } else {
        slider.setAttribute("disabled", true);
    }

});