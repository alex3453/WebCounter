const requestURL = 'https://jsonplaceholder.typicode.com/users'

document.addEventListener("DOMContentLoaded", sendUserStat);

function sendUserStat(){
    const body = {
    host: window.location.host
  }

  sendRequest('POST', requestURL, body)
    .then(data => console.log(data))
    .catch(err => console.log(err))
}

function sendRequest(method, url, body = null) {
  const headers = {
    'Content-Type': 'application/json'
  }

  return fetch(url, {
    method: method,
    body: JSON.stringify(body),
    headers: headers
  }).then(response => {
    if (response.ok) {
      return response.json()
    }
  })
}

