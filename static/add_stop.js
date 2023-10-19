function addStop(townId) {
        const stopName = document.getElementById('stop-name').value;

        fetch(`/towns/${townId}/stops/`, {
            method: 'POST',
            body: JSON.stringify({stop_name: stopName}),
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            }
        })
            .then(async response => {
                if (response.ok) {
                    const newStop = await response.json();
                    const newStopList = document.getElementById('new-stop-list');
                    const newStopElement = document.createElement('li');
                    const newLinkStopName = document.createElement('a')
                    newLinkStopName.setAttribute('class', "stop-name")
                    newLinkStopName.setAttribute('href',`/stops/${newStop.id}`)
                    newLinkStopName.textContent = newStop.stop_name;
                    newStopElement.appendChild(newLinkStopName)
                    newStopElement.setAttribute('stop-id', newStop.id);

                    const newDelButton = document.createElement("button");
                    newDelButton.textContent = "Usuń";
                    newDelButton.setAttribute("onclick", `deleteStop("${newStop.id}")`);
                    newDelButton.setAttribute("class", `delete`);

                    const newEditButton = document.createElement("button");
                    newEditButton.setAttribute("onclick", `editStop("${newStop.id}")`);
                    newEditButton.setAttribute("class", `edit`);
                    newEditButton.textContent = "Edytuj";

                    newStopElement.appendChild(newEditButton)
                    newStopElement.appendChild(newDelButton)
                    newStopList.appendChild(newStopElement);
                    document.getElementById('stop-name').value = '';
                } else {
                    // Obsłuż błąd
                }
            })
            .catch(error => {
            console.error(error);
        });
}