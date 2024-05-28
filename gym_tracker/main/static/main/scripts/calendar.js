let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();
let data
let calDate


function prev() {
    let monthOffsetEl = document.getElementById('moffset');
    monthOffsetEl.value = Number(monthOffsetEl.value) - 1;
    displayCalData();
}

function forw() {
    let monthOffsetEl = document.getElementById('moffset');
    monthOffsetEl.value = Number(monthOffsetEl.value) + 1;
    displayCalData();
}

function displayCalData() {
    let monthOffset = Number(document.getElementById('moffset').value);
    calDate = new Date(date.getTime() + (2592000 * monthOffset * 1000));
    let calHTML = getCalendarHTML(calDate);
    let calMonthName = calDate.toLocaleString('default', { month: 'long' });
    document.getElementById('cal').innerHTML = calHTML;
    document.getElementById('cal-month').innerHTML = calMonthName;
}

function getFinishedTrainings() {
    fetch(document.location.origin + '/api/v1/ftrainings/')
        .then(res => res.json())
        .then(json => {
            data = json;
            displayCalData();
        })
}

function renderDateField(date, curCalDate, isInactive) {
    let isToday = '';
    if (new Date().toDateString() == new Date(`${curCalDate.getFullYear()}-${curCalDate.getMonth() + 1}-${date}`).toDateString()) {
        isToday = 'border border-2 border-primary';
    } 
    for (let i = 0; i < data.length; i++) {
        let dataDatetime = data[i]['started_at']
        if (curCalDate.getFullYear() == dataDatetime.slice(0, 4)) {
            if (curCalDate.getMonth() + 1 == Number(dataDatetime.slice(5, 7))) {
                if (date == Number(dataDatetime.slice(8, 10))) {
                    return `<td class="field-succ calfield ${isToday}">
                                <div class="text-end fw-bold">${date}</div>
                                <div class="calspace"></div>
                            </td>`   
                }
            }
        }
    }
    if (isInactive) {
        return `<td class="field-inactive calfield ${isToday}">
                    <div class="text-end fw-bold">${date}</div>
                    <div class="calspace"></div>
                </td>`
    } else {
        return `<td class="calfield ${isToday}">
                    <div class="text-end fw-bold">${date}</div>
                    <div class="calspace">
                    </div>
                </td>`
    }
}

function getCalendarHTML(calDate) {
    let calYear = calDate.getFullYear();
    let calMonth = calDate.getMonth();
    let firstDateOfMonth = new Date(calYear, calMonth, 1);
    let lastDateOfMonth = new Date(calYear, calMonth + 1, 0);
    let lastDateOfPrevMontn = new Date(calYear, calMonth, 0);
    let firstDateOfNextMonth = new Date(calYear, calMonth + 1, 1);
    let calHTML = '<tr>';
    let firstDayOfMonth = firstDateOfMonth.getDay();
    if (firstDayOfMonth == 0) {
        firstDayOfMonth = 7;
    }
    for (let i = 1; i < firstDayOfMonth; i++) {
        let calCurDate = lastDateOfPrevMontn.getDate() - (firstDayOfMonth - i) + 1;
        calHTML += renderDateField(calCurDate, lastDateOfPrevMontn, true);
    }
    let j = 1;
    for (let i = firstDayOfMonth; i < 8; i++) {
        calHTML += renderDateField(j, calDate, false);
        j++;
    }
    calHTML += '</tr>';
    while (j <= lastDateOfMonth.getDate()) {
        calHTML += '<tr>';
        for (let i = 1; i < 8; i++) {
            calHTML += renderDateField(j, calDate, false);
            if (j == lastDateOfMonth.getDate()) {
                j++;
                let k = 1;
                if (lastDateOfMonth.getDay() != 0) {
                    for (let i = lastDateOfMonth.getDay(); i < 7; i++) {
                        calHTML += renderDateField(k, firstDateOfNextMonth, true);
                        k++;
                    }
                }
                break
            }
            j++;
        }
        calHTML += '</tr>';
    }
    return calHTML
}

getFinishedTrainings()
