function deleteTown(townId) {
    // Wyświetl komunikat z potwierdzeniem
    const confirmed = confirm(`Czy jesteś pewien, że chcesz usunąć wybrane miasto?`);

    if (confirmed) {
        // Jeśli użytkownik potwierdził, wyslij żądanie DELETE do odpowiedniego endpointu
        fetch(`/towns/${townId}`, {
            method: 'DELETE'
        })
            .then(response => {
                if (response.ok) {
                    // Jeśli usunięcie zakończyło się sukcesem, usuń miasto z listy town-id="{{ town.id }}"
                    const townElement = document.querySelector(`[town-id="${townId}"]`)
                    if (townElement) {
                        townElement.remove();
                    }
                } else {
                    // Obsłuż błąd
                }
            })
            .catch(error => {
                console.error(error);
            });
    }
}