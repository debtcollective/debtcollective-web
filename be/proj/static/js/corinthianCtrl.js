app.controller('corinthianCtrl',
  function ($scope, $http) {
    $scope.debtors = 13415;
    $scope.debt = 354135;
    $scope.money = 24194;

    $scope.selectionIndex = null;
    $scope.loading = true;

    $http.get('/static/js/strikers.json').then(function (resp) {
      $scope.loading = false;
      var strikers = []
      for (i in resp.data) {
        var striker = resp.data[i]
        striker.shortBio = striker.bio.slice(0, 200);
        striker.first_name = striker.name.split(' ')[0].toLowerCase()
        strikers.push(striker)
      }
      $scope.data = strikers

    });

    $scope.showStriker = function (index, $event) {
      $scope.selectionIndex = index;
      $event.stopPropagation()
    }

    $scope.closeStriker = function ($event) {
      if ($scope.selectionIndex == null) return
      $scope.selectionIndex = null;
      $event.stopPropagation()
    }

    $scope.formVisible = function () { return true; }
});
