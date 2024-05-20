var tID = document.currentScript.getAttribute('tID');
var eID
const btns = ['add-set-btn', 'exrc-fnsh-btn', 'exrc-next-btn']

function addSetInput() {
    const setTemplate =
        `
    <li class="list-group-item d-flex align-items-center p-0 ps-3">
        <div class="ms-2 w-100">
            <div class="input-group">
                <div class="form-floating">
                    <input name="set-weight" type="text" class="form-control" id="floatingInputGroup1" placeholder="Вес">
                    <label for="floatingInputGroup1">Вес</label>
                </div>
                <span class="input-group-text">Х</span>
                <div class="form-floating">
                    <input name="set-repeats" type="text" class="form-control" id="floatingInputGroup1" placeholder="Повторения">
                    <label for="floatingInputGroup1">Повторения</label>
                </div>
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

function disableButtons() {
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
            } else {
                eID = data['id']
                var exerciseEl = document.getElementById("exrc-name");
                exerciseEl.innerHTML = data["name"];
                exerciseEl.classList.remove("placeholder-glow");
                if (data['sets'].length > 0) {
                    console.log('fd')
                    var sets = data['sets'].map((list) => {
                        var setWeight = list['weight']
                        var setRepetitions = list['repetitions']
                        var setHTML = `<li class="list-group-item d-flex align-items-center p-0 ps-3">
                            <div class="ms-2 w-100">
                                <div class="input-group">
                                    <div class="form-floating">
                                        <input name="set-weight" type="text" class="form-control" id="floatingInputGroup1" placeholder="${setWeight}">
                                        <label for="floatingInputGroup1">${setWeight}</label>
                                    </div>
                                    <span class="input-group-text">Х</span>
                                    <div class="form-floating">
                                        <input name="set-repeats" type="text" class="form-control" id="floatingInputGroup1" placeholder="${setRepetitions}">
                                        <label for="floatingInputGroup1">${setRepetitions}</label>
                                    </div>
                                </div>
                            </div>
                        </li>
                        `
                        return setHTML
                    })
                } else {
                    console.log('f22d')
                    var sets = []
                    for (let i = 0; i < 3; i++) {
                        sets.push(`
                        <li class="list-group-item d-flex align-items-center p-0 ps-3">
                        <div class="ms-2 w-100">
                            <div class="input-group">
                                <div class="form-floating">
                                    <input name="set-weight" type="text" class="form-control" id="floatingInputGroup1" placeholder="Вес">
                                    <label for="floatingInputGroup1">Вес</label>
                                </div>
                                <span class="input-group-text">Х</span>
                                <div class="form-floating">
                                    <input name="set-repeats" type="text" class="form-control" id="floatingInputGroup1" placeholder="Повторения">
                                    <label for="floatingInputGroup1">Повторения</label>
                                    </div>
                            </div>
                            </div>
                            </li>
                            `)
                    }
                }
                sets.push(`
                <button type="button" onclick="addSetInput()" id="add-set-btn"
                class="list-group-item list-group-item-action list-group-item-light d-flex align-items-center p-1 ps-3">
                    <div class="w-100 text-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-plus" viewBox="0 0 16 16">
                        <path fill="white" d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4"/>
                    </svg>
                        Добавить
                    </div>
                </button>
                `)
                document.getElementById('exrcs').innerHTML = sets.join('');
                enableButtons()
            }
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

async function nextExercise() {
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