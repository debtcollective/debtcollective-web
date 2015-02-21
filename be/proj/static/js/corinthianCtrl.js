Array.prototype.chunk = function(chunkSize) {
    var array=this;
    return [].concat.apply([],
        array.map(function(elem,i) {
            return i%chunkSize ? [] : [array.slice(i,i+chunkSize)];
        })
    );
}

app.controller('corinthianCtrl',
  function ($scope, $window, $http) {
    $scope.debtors = 13415;
    $scope.debt = 354135;
    $scope.money = 24194;

    $scope.selectedStriker = null;
    $scope.loading = true;
    $scope.corinthian = false;
    $scope.strikers = []

    $http.get('/static/js/strikers.json').then(function (resp) {
      $scope.loading = false;
      for (i in resp.data) {
        var striker = resp.data[i]
        striker.first_name = striker.name.split(' ')[0].toLowerCase()
        $scope.strikers.push(striker)
      }
      $scope.strikerChunks = $scope.strikers.chunk(4)
    });

    $scope.agreeButton = function () {
      if ($scope.corinthian) {
        $window.location.href = '/corinthiansignup'
      }
      else {
        $scope.normalsignup = true
      }
    }

    $scope.showStriker = function (striker, $event) {
      striker.visible = true
      $scope.selectedStriker = striker
      $event.stopPropagation()
    }

    $scope.closeStriker = function (striker, $event) {
      $scope.selectedStriker = null
      if (striker) striker.visible = false
      else $scope.strikers.forEach(function (striker) { striker.visible = false })
      $event.stopPropagation()
    }

    $scope.formVisible = function () { return true; }
});
