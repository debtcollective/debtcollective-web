var request = require('request')

var forms = require('./debtis.json')

///var HOST = 'http://localhost:8000'
var HOST = 'http://debtcollective.org'
var PATH = '/corinthian/dtr/restore/'

function sendOne(id, cb) {
  var params = {
    method: 'GET',
    uri: HOST + PATH + id,
  }
  request(params, cb)
}

for (var i = 0; i < forms.length; i++) {
  var pk = forms[i]['pk']

  sendOne(pk, function (err, resp, body) {
    if (err) console.log('error!')
      console.log(body)
  })
}
