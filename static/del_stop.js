function deleteStop(stopId) {
    // Wyświetl komunikat z potwierdzeniem
    const confirmed = confirm(`Czy jesteś pewien, że chcesz usunąć wybrany przystanek?`);

    if (confirmed) {
        // Jeśli użytkownik potwierdził, wyslij żądanie DELETE do odpowiedniego endpointu
        fetch(`/stops/${stopId}`, {
            method: 'DELETE'
        })
            .then(response => {
                if (response.ok) {
                    // Jeśli usunięcie zakończyło się sukcesem, usuń przystanek z listy stop-id="{{ stop.id }}"
                    const stopElement = document.querySelector(`[stop-id="${stopId}"]`)
                    if (stopElement) {
                        stopElement.remove();
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