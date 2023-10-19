function editTown(townId) {
    // Znajdź element <li> z nazwą miasta
    const townElement = document.querySelector(`[town-id="${townId}"]`);

    if (townElement) {
        // Zmień tekst na pole tekstowe do edycji
        const townNameText = townElement.querySelector('.town-name');
        townNameText.style.display = 'none';
        const delButton = townElement.querySelector('.delete');
        const editButton = townElement.querySelector('.edit');
        delButton.style.display = 'none';
        editButton.style.display = 'none';

        const townNameInput = document.createElement('input');
        townNameInput.value = townNameText.textContent;
        townElement.appendChild(townNameInput);

        // Pokaż przycisk "Zapisz"
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Zapisz';
        saveButton.className = 'save'
        saveButton.onclick = () => {
            const updatedName = townNameInput.value;
            updateTownName(townId, updatedName);
        };
        townElement.appendChild(saveButton);
    }
}

function updateTownName(townId, updatedName) {
    // Wyślij zapytanie PUT do zmiany nazwy miasta
    fetch(`/towns/${townId}`, {
        method: 'PUT',
        body: JSON.stringify({
            town_name: updatedName,
        }),
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        },
    })
        .then(response => {
            if (response.ok) {
                // Zaktualizuj tekst w liście
                const townElement = document.querySelector(`[town-id="${townId}"]`);
                const townNameText = townElement.querySelector('.town-name');
                townNameText.style.display = 'inline-block';
                townNameText.textContent = updatedName;
                const delButton = townElement.querySelector('.delete');
                const editButton = townElement.querySelector('.edit');
                delButton.style.display = 'inline-block';
                editButton.style.display = 'inline-block';

                // Usuń pole tekstowe i przycisk "Zapisz"
                const townNameInput = townElement.querySelector('input');
                const saveButton = townElement.querySelector('.save');
                townNameInput.remove();
                saveButton.remove();
            } else {
                // Obsłuż błąd
            }
        })
        .catch(error => {
            console.error(error);
        });
}
