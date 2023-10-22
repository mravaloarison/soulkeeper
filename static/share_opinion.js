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
        // Clone the HTML structure inside the loop
        const form = document.createElement("form");
        form.action = `/get_idea/${e.id}`;
        form.innerHTML = `
            <blockquote>
                "${data.articles[i].description}"
                <footer>
                    <textarea name="user_idea_input" placeholder="Share your idea"></textarea>
                    <textarea style="display: none;" name="title">${data.articles[i].title}</textarea>
                    <label class="grid">
                        <button type="submit" class="outline">Submit</button>
                        <div></div><div></div><div></div><div></div>
                    </label>
                </footer>
            </blockquote>
        `;
    
        // Append the form to the container
        blockquoteContainer.appendChild(form);
    }
    

    blockquoteContainer.style.display = "block";
}