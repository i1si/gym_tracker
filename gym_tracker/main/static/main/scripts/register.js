function serializeForm(formNode) {
  return new FormData(formNode)
}

async function sendData(data) {
	return await fetch(window.location.origin + '/api/v1/users/', {
		method: 'POST',
		body: data,
	})
}

async function handleFormSubmit(event) {
  event.preventDefault()
  const data = serializeForm(applicantForm)
  const response = await sendData(data)
  if (response.ok) {
		location.reload()
	} else {
		await response.json()
		.then (err => {
			document.getElementById("floatingInput").classList.add("is-invalid")
			document.getElementById("invalid-fbck-usrnm").innerHTML = err["username"][0]
		})
	}
}

const applicantForm = document.getElementById('reg_form')
applicantForm.addEventListener('submit', handleFormSubmit)
