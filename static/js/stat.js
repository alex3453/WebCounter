const requestURL = 'http://localhost:5000/about'

document.addEventListener("DOMContentLoaded", sendUserStat);

function sendUserStat(){
  const headers = {
    'Content-Type': 'application/json;charset=utf-8'
  }
  const user = {
    name: 'John',
    surname: 'Smith'
  }

  fetch(requestURL, {
    method: 'POST',
    body: JSON.stringify(user),
    headers: headers
  }).then(data => console.log(data))
    .catch(err => console.log(err))
}
