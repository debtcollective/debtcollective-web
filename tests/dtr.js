var request = require('request')

var CLIENTS = 50
var HOST = 'http://localhost:8000'
//var HOST = 'http://stage.debtcollective.org'
var PATH = '/corinthian/dtr_generate'

function sendOne(cb) {
  var params = {
    method: 'POST',
    uri: HOST + PATH,
    json: {
      ssn_1: '334',
      ssn_2: '434',
      ssn_3: '455',
      name: 'hello'
    }
  }
  request(params, cb)
}

for (var i = 0; i < CLIENTS; i++) {
  console.log('sending one')
  sendOne(function (err, resp, body) {
    if (err) console.log('error!')
    console.log('got one!', body)
  })
}