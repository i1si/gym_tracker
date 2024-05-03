async function sendNewTraining(data) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return await fetch(window.location.origin + '/api/v1/trainings/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
			'X-CSRFToken': csrfToken,
			'Content-Type': 'application/json;charset=utf-8'
		},
        mode: "same-origin"
    })
}

async function handleFormSubmit(event) {
    event.preventDefault()
    const spinner = document.getElementById("add-trn-spnr");
    spinner.classList.remove("visually-hidden");
    document.getElementById("add-trn-btn").disabled = true;
    const training_name = document.getElementById('trn-name').value;
    const exercises = document.getElementsByName("exr-name");
    const exerciseList = []
    for (let i = 0; i < exercises.length; i++) {
        exerciseList.push({"name": exercises[i].value})
    }
    const data = {
        "name": training_name,
        "exercises": exerciseList
    }
    const response = await sendNewTraining(data);
    if (response.ok) {
        getTrainings();
        document.getElementById("add-trn-cls").click();
        trainingForm.reset();
    } else {
        await response.json()
            .then(err => {
				console.log(err)
            })
    }
    spinner.classList.add("visually-hidden");
    document.getElementById("add-trn-btn").disabled = false;
}

function addExerciseInput() {
    const exerciseTemplate = 
        `
        <li class="list-group-item d-flex align-items-center p-0 ps-3">
            <div class="ms-2 w-100">
                <input name="exr-name" type="text" class="form-control border-0" placeholder="Название">
            </div>
        </li>
        `
    document.getElementById("add-exrc-btn").insertAdjacentHTML('beforebegin', exerciseTemplate);
}

const trainingForm = document.getElementById('add-t-form');
trainingForm.addEventListener('submit', handleFormSubmit);