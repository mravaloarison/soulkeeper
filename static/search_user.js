const input = document.getElementById('by-user-name');
const outputDiv = document.querySelector('.user_search_output');

input.addEventListener('input', async function () {
    const searchTerm = input.value.toLowerCase();

    try {
        const response = await fetch('/search_user?q=' + searchTerm);
        const filteredData = await response.json();

        // Clear the existing content
        outputDiv.innerHTML = '';

        if (filteredData.length > 0) {
            filteredData.forEach(item => {
                // Create a div for each item
                const userDiv = document.createElement('div');
                userDiv.classList.add('user-result');

                // Create HTML content for the div
                userDiv.innerHTML = `
                <article class="grid">
                    <img style="width: 150px; height: 150px;" src="${item.avatar_url}" alt="${item.name} Avatar">
                    <hgroup class="user-info">
                        <h3>${item.name}</h3>
                        <p>${item.personality_type}</p>
                        <a href="/avatar/${item.name}"><small><cite>Look</cite></small></a>
                    </hgroup>
                </article>
                `;

                // Append the div to the output container
                outputDiv.appendChild(userDiv);
            });
        } else {
            outputDiv.innerHTML = '<p>No matching users found.</p>';
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
});
