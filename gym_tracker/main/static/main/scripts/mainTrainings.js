// const CurrTrainingTemplate = 
// `
// <button
// 	class="list-group-item list-group-item-action list-group-item-primary d-flex justify-content-between align-items-center">
// 	<div class="text-start">
// 		<div class="fw-bold">
// 			${}
// 		</div>
// 		текущая
// 	</div>
// 	<span class="badge text-bg-primary rounded-pill">7 дней назад</span>
// </button>
// `


const btnTemplate =
	`
	<button type="button" class="list-group-item list-group-item-action list-group-item-light"
	data-bs-toggle="modal" data-bs-target="#addTraining">
	<img src="${document.location.origin}/static/main/img/plus.svg"/>
		Добавить
	</button>
	`

fetch(document.location.origin + '/api/v1/trainings/')
	.then(res => res.json())
	.then(data => {
		displayTrainings(data)
	})

function displayTrainings(trainings_json) {
	var trainingList = document.getElementById('training_list')
	if (trainings_json.length) {
		const content = trainings_json.map((list) => {
			var trainingName = list['name']
			if (list['finished_trainings']) {
				var trainingStartedAt = list['finished_trainings']['started_at']
				diff = dateDiff(trainingStartedAt)
				if (diff == 0) {
					lastTraining = 'недавно'
				} else {
					var lastTraining = getDaysTitle(dateDiff(trainingStartedAt))
				}
			} else {
				var lastTraining = 'никогда'
			}
			const trainingTemplate =
				`
				<button
					class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
					<div class="text-start">
						<div class="fw-bold">
							${trainingName}
						</div>
					</div>
					<span class="badge text-bg-primary rounded-pill">${lastTraining}</span>
				</button>
				`
			return trainingTemplate
		})
		content.push(btnTemplate)
		trainingList.innerHTML = content.join('')
	} else {
		trainingList.innerHTML = '<p>Пока что тренировок нет</p>' + btnTemplate
	}
}

function dateDiff(datetime) {
	var t1 = new Date(datetime).getTime();
	var t2 = new Date().getTime();
	diff = Math.floor((t2-t1)/86400000);
	if (86400000 > diff > 43200000) {
		return 1
	}
	return diff;
}

function getDaysTitle(count) {
    function declination(number, titles) {
    cases = [2, 0, 1, 1, 1, 2];
    return titles[ (number%100>4 && number%100<20)? 2:cases[(number%10<5)?number%10:5] ];
    }
    title = declination(count, [' день назад', ' дня назад', ' дней назад']);
    return count + title;
}