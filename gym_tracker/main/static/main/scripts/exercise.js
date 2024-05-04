var tID = document.currentScript.getAttribute('tID');
var eID
const btns = ['add-set-btn', 'exrc-fnsh-btn', 'exrc-next-btn']

function addSetInput() {
    const setTemplate = 
    `
    <li class="list-group-item d-flex align-items-center p-0 ps-3">
        <div class="ms-2 w-100">
            <div class="input-group">
                <input name="exr-name" type="text" class="form-control form-control-lg border-0" placeholder="Вес">
                <input name="exr-name" type="text" class="form-control form-control-lg border-0 border-start" placeholder="Повторений">
            </div>
        </div>
    </li>
    `
    document.getElementById("add-set-btn").insertAdjacentHTML('beforebegin', setTemplate);
}

function enableButtons() {
    btns.map((btn) => {
        document.getElementById(btn).classList.remove("disabled");
    })
}

function disableButtons(){
    btns.map((btn) => {
        document.getElementById(btn).classList.add("disabled");
    })
}

function getExercise(exerciseID) {
    path = '/api/v1/exercises/?tID=' + tID
    if (exerciseID) {
        path += '&eID=' + exerciseID
    }
    console.log(path)
    fetch(document.location.origin + path)
        .then(res => res.json())
        .then(data => {
            if (!data['next']) {
                window.location.replace(document.location.origin + '/trainings/?f=true')
            }
            console.log(data)
            eID = data['id']
            var exerciseEl = document.getElementById("exrc-name");
            exerciseEl.innerHTML = data["name"];
            exerciseEl.classList.remove("placeholder-glow");
            enableButtons()
        }
    )
}

async function sendExerciseSets() {
    const setWeights = document.getElementsByName("set-weight");
    const setReps = document.getElementsByName("set-repeats");
    const sets = [];
    for (let i = 0; i < setWeights.length; i++) {
        sets.push({
            "set": i,
            "weight": setWeights[i].value,
            "repetitions": setReps[i].value
        })
        setWeights[i].value = "";
        setReps[i].value = "";
    }
    const data = {
        "training_id": tID,
        "exercise_id": eID,
        "finished_sets": sets,
    };
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    return await fetch(document.location.origin + '/api/v1/exercises/', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
			'X-CSRFToken': csrfToken,
			'Content-Type': 'application/json;charset=utf-8'
		},
        mode: "same-origin"
    })
}

async function nextExercise(){
    disableButtons()
    response = await sendExerciseSets()
    if (response.ok) {
        getExercise(eID)
    } else {
        await response.json()
            .then(err => {
				console.log(err)
            }
        )
    }
    enableButtons()
}

getExercise()