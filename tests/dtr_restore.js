var request = require('request')
var argv = require('minimist')(process.argv.slice(2))
var forms = require('./debtis.json')

///var HOST = 'http://localhost:8000'
var HOST = 'http://debtcollective.org'
var PATH = '/corinthian/dtr/restore/'

function sendOne(id, cb) {
  var params = {
    method: 'GET',
    uri: HOST + PATH + id,
  }
  console.log(params)
  request(params, cb)
}

if (argv._.length === 2) {
  for (var i = argv._[0]; i < argv._[1]; i++) {
    sendOne(i, function (err, resp, body) {
      if (err) console.log('error!')
        console.log(body)
    })
  }
} else {
  for (var i = 0; i < forms.length; i++) {
    var pk = forms[i]['pk']

    sendOne(pk, function (err, resp, body) {
      if (err) console.log('error!')
        console.log(body)
    })
  }
}
