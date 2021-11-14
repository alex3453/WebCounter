const requestURL = 'https://web-counter.herokuapp.com/makenode'

document.addEventListener("DOMContentLoaded", sendUserStat);

function sendUserStat(){
  const headers = {
    'Content-Type': 'application/json;charset=utf-8'
  }
  const user = {
    host: window.location.host,
    pathname: window.location.pathname,
    referrer: document.referrer,
  }

  fetch(requestURL, {
    method: 'POST',
    body: JSON.stringify(user),
    headers: headers
  }).then(data => console.log(data))
    .catch(err => console.log(err))
}