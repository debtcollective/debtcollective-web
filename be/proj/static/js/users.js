app.service('users', function (util_svc, $http) {
  var self = this

  this.createAnonymousUser = function (userData, cb) {
    userData.username = util_svc.generateUUID()
    userData.email = userData.email
    userData.password = userData.email
    self.create(userData, function (resp) {
      cb(resp, userData.username)
    })
  }

  this.create = function (userData, cb) {
    $http.post('/signup', userData).then(function (resp) {
      self.signupForMailingList(userData, cb)
    })
  }

  this.signupForMailingList = function (userData, cb) {
    userData.list = '8CaVcsDmVe41wdpl194UlQ',
    userData.boolean = true

    $http.post('//mail.debtcollective.org/subscribe', userData).then(function (resp) {
      cb(resp)
    })
  }

});