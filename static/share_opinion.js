async function talkAbout(e) {
    // Fetch data from a URL based on e.id
    const response = await fetch(`/search_news/${e.id}`);

    if (!response.ok) {
        // Handle the case where the response is not successful
        console.error('Failed to fetch data:', response.status);
        return;
    }

    document.querySelectorAll(".to-hide").forEach((item) => {
        item.style.display = "none";
    });
    // Parse the response as JSON
    const data = await response.json();
    const blockquoteContainer = document.getElementById("block-quote-container");

    for (let i = 0; i < 3; i++) {
        const blockquote = document.createElement("blockquote");

        blockquote.textContent = data.articles[i].description;

        blockquoteContainer.appendChild(blockquote);
    }
    blockquoteContainer.style.display = "block";
}