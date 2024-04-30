function serializeForm(formNode) {
    return new FormData(formNode)
}

async function sendNewTraining(data) {
    return await fetch(window.location.origin + '/api/v1/trainings/', {
        method: 'POST',
        body: data,
    })
}

async function handleFormSubmit(event) {
    event.preventDefault()
    // const spinner = document.getElementById("spnr");
    // spinner.classList.remove("visually-hidden");
    // button = document.getElementById("lgn-btn").disabled = true;
    const data = serializeForm(trainingForm);
    const response = await sendNewTraining(data);
    if (response.ok) {
        console.log(response)
    } else {
        await response.json()
            .then(err => {
				console.log(err)
                // document.getElementById("invalid-fbck-usrnm").innerHTML = err["err"];
            })
    }
    // spinner.classList.add("visually-hidden");
    // button = document.getElementById("lgn-btn").disabled = false;
}

const trainingForm = document.getElementById('add-t-form');
trainingForm.addEventListener('submit', handleFormSubmit);