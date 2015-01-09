app.controller('corinthianCtrl',
  function ($scope, $http, $document, $window, util_svc) {
    $scope.debtors = 13415;
    $scope.debt = 354135;
    $scope.money = 24194;
    $scope.profileIndex = 0;
    $scope.data = [];

    function populateStrikers() {
      var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1JWrE9ca5aU9NbGHoioVIhsJJhY9r09T7TCQw220XhgM/pubhtml?gid=0&single=true'
      $scope.loading = true;

      if (!Tabletop) {
        return populateStrikers()
      }

      Tabletop.init( { key: public_spreadsheet_url,
                       callback: showInfo,
                       simpleSheet: true } )
    }

    function showInfo(data) {
      $scope.loading = false;
      $scope.data = data;
    }

    populateStrikers();
});
