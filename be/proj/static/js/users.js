app.service('users', function (util_svc, $http) {
  var self = this

  this.createAnonymousUser = function (userData, cb) {
    userData.username = util_svc.generateUUID()
    userData.password = userData.email
    self.create(userData, function (resp) {
      cb(resp, userData.username)
    })
  }

  this.create = function (userData, cb) {
    console.log('creating user', userData)
    $http.post('/signup/', userData).then(function (resp) {
      console.log(resp)
      cb(resp)
    });
  }

  this.gDocsCollectiveCounter = function (salliemae, corinthian) {
    /**
      Add a row (a user) to the collectives that are displayed on the front page.
      salliemae, corinthian are either 1 or 0
    **/
    var googleForm = $(window).jqGoogleForms({"formKey": "1Vk1WIqyyj4-tHetXZIqCvuoLDmPoDL6QTPQTZ4disUY"});
    var data = {
      'entry.71652265': salliemae,
      'entry.256870148': corinthian
    }
    googleForm.sendFormData(data)
  };

});