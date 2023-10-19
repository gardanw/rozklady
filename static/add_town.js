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
        // document.getElementById('new-town').style.display = 'block';
        const newTown = await response.json();
        const newTownList = document.getElementById('new-town-list');
        const newTownElement = document.createElement('li');
        const newLinkTownName = document.createElement('a')
        newLinkTownName.setAttribute('class',"town-name")
        newLinkTownName.setAttribute('href',`/towns/${newTown.id}`)
        newLinkTownName.textContent = newTown.town_name;
        newTownElement.appendChild(newLinkTownName)
        newTownElement.setAttribute('town-id', newTown.id);

        const newDelButton = document.createElement("button");
        newDelButton.textContent = "Usuń";
        newDelButton.setAttribute("onclick", `deleteTown("${newTown.id}")`);
        newDelButton.setAttribute("class", `delete`);

        const newEditButton = document.createElement("button");
        newEditButton.setAttribute("onclick", `editTown("${newTown.id}")`);
        newEditButton.setAttribute("class", `edit`);
        newEditButton.textContent = "Edytuj";

        newTownElement.appendChild(newEditButton)
        newTownElement.appendChild(newDelButton)
        newTownList.appendChild(newTownElement);
        document.getElementById('town-name').value = '';
    } else {
        // Obsłuż błąd
    }
});