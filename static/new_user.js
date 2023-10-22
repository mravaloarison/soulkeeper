// Save profile
document.getElementById("saveButton").addEventListener("click", function (event) {
    event.preventDefault();

    this.setAttribute("aria-busy", "true");

    // Gather the data you want to send in the POST request
    const avatar = document.getElementById("to-del").getAttribute("src");
    const username = document.getElementById("user-name").value;

    const data = {
        avatar: avatar,
        username: username,
    };
    
    const saveButton = document.getElementById("saveButton");
    fetch("/get_avatar_soulname", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        if (response.ok) {
            saveButton.setAttribute("aria-busy", "true");
            setTimeout(function () {
                saveButton.removeAttribute("aria-busy", "true");
                saveButton.innerHTML = "Saved";
                setTimeout(function () {
                    saveButton.style.display = "none";
                    const startTestLink = document.getElementById("start_test");
                    startTestLink.style.display = "block";
                }, 1000);
            }, 1000);

        } else {
            saveButton.setAttribute("aria-invalid", "true");
            saveButton.innerHTML = "Refresh the page";
        }
    })
    .catch(error => {
        console.error(error);
        // Handle errors here if needed
    });
});




const usernameInput = document.getElementById("user-name");
const avatarImage = document.getElementById("to-del");

// Search for avatar
usernameInput.addEventListener("input", async function () {
    let response = await fetch('/search_avatar?q=' + usernameInput.value);
    let shows = await response.text();
    const newImageUrl = shows;
    avatarImage.src = newImageUrl;
});