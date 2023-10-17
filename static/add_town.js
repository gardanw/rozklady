document.getElementById('town-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const townName = document.getElementById('town-name').value;

    const response = await fetch('/towns/', {
        method: 'POST',
        body: JSON.stringify({ town_name: townName }),
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        }
    });

    if (response.ok) {
        document.getElementById('new-town').style.display = 'block';
        const newTown = await response.json();
        const newTownList = document.getElementById('new-town-list');
        const newTownElement = document.createElement('li');
        newTownElement.textContent = newTown.town_name;
        newTownElement.setAttribute('town-id', newTown.id);
        newTownList.appendChild(newTownElement);
        document.getElementById('town-name').value = '';
    } else {
        // Obsłuż błąd
    }
});