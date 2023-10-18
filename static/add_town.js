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
        const newSpanTownName = document.createElement('span')
        newSpanTownName.setAttribute('class',"town-name")
        newSpanTownName.textContent = newTown.town_name;
        newTownElement.appendChild(newSpanTownName)
        newTownElement.setAttribute('town-id', newTown.id);

        const newDelButton = document.createElement("button");
        newDelButton.textContent = "Usuń";
        newDelButton.setAttribute("onclick", `deleteTown("${newTown.id}", "${newTown.town_name}")`);
        newDelButton.setAttribute("class", `delete`);

        const newEditButton = document.createElement("button");
        newEditButton.setAttribute("onclick", `editTown("${newTown.id}", "${newTown.town_name}")`);
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