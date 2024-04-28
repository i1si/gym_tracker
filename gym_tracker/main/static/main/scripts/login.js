function serializeForm(formNode) {
    return new FormData(formNode)
  }
  
  async function sendData(data) {
      return await fetch(window.location.origin + '/api/v1/users/login', {
          method: 'POST',
          body: data,
      })
  }
  
  async function handleFormSubmit(event) {
    event.preventDefault()
    const spinner = document.getElementById("spnr");
    spinner.classList.remove("visually-hidden");
    button = document.getElementById("lgn-btn").disabled = true;
    const data = serializeForm(applicantForm);
    const response = await sendData(data);
    if (response.ok) {
          location.reload();
      } else {
          await response.json()
          .then (err => {
              document.getElementById("invalid-fbck-usrnm").innerHTML = err["err"];
          })
      }
    spinner.classList.add("visually-hidden");
    button = document.getElementById("lgn-btn").disabled = false;
  }
  
  const applicantForm = document.getElementById('reg_form');
  applicantForm.addEventListener('submit', handleFormSubmit);
