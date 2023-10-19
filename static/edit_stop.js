function editStop(stopId) {
    // Znajdź element <li> z nazwą przystanku
    const stopElement = document.querySelector(`[stop-id="${stopId}"]`);

    if (stopElement) {
        // Zmień tekst na pole tekstowe do edycji
        const stopNameText = stopElement.querySelector('.stop-name');
        stopNameText.style.display = 'none';
        const delButton = stopElement.querySelector('.delete');
        const editButton = stopElement.querySelector('.edit');
        delButton.style.display = 'none';
        editButton.style.display = 'none';

        const stopNameInput = document.createElement('input');
        stopNameInput.value = stopNameText.textContent;
        stopElement.appendChild(stopNameInput);

        // Pokaż przycisk "Zapisz"
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Zapisz';
        saveButton.className = 'save'
        saveButton.onclick = () => {
            const updatedName = stopNameInput.value;
            updateStopName(stopId, updatedName);
        };
        stopElement.appendChild(saveButton);
    }
}

function updateStopName(stopId, updatedName) {
    // Wyślij zapytanie PUT do zmiany nazwy przystanku
    fetch(`/stops/${stopId}`, {
        method: 'PUT',
        body: JSON.stringify({
            stop_name: updatedName,
        }),
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
        },
    })
        .then(response => {
            if (response.ok) {
                // Zaktualizuj tekst w liście
                const stopElement = document.querySelector(`[stop-id="${stopId}"]`);
                const stopNameText = stopElement.querySelector('.stop-name');
                stopNameText.style.display = 'inline-block';
                stopNameText.textContent = updatedName;
                const delButton = stopElement.querySelector('.delete');
                const editButton = stopElement.querySelector('.edit');
                delButton.style.display = 'inline-block';
                editButton.style.display = 'inline-block';

                // Usuń pole tekstowe i przycisk "Zapisz"
                const stopNameInput = stopElement.querySelector('input');
                const saveButton = stopElement.querySelector('.save');
                stopNameInput.remove();
                saveButton.remove();
            } else {
                // Obsłuż błąd
            }
        })
        .catch(error => {
            console.error(error);
        });
}
