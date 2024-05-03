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
