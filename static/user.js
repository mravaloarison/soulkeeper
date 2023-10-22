const arrOfDir = document.querySelectorAll(".dir");

arrOfDir.forEach(element => {
    const dataLink = element.getAttribute("data-link");
    element.addEventListener("click", function () {
        location.href = `/${dataLink}`;
    });
});
