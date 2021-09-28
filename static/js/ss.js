const requestURL = 'https://jsonplaceholder.typicode.com/users'

const xhr = new XMLHttpRequest()

xhr.open('GET', requestURL)

xhr.send()