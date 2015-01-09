app.controller('corinthianCtrl',
  function ($scope, $http) {
    $scope.debtors = 13415;
    $scope.debt = 354135;
    $scope.money = 24194;

    $scope.loading = true;

    $http.get('/static/js/strikers.json').then(function (resp) {
      $scope.loading = false;
      $scope.data = resp.data;
    });
});
