var app = angular.module('myDebtIs', []);

app.controller('myDebtIsCtrl', function ($scope) {

    $scope.debt = '';
    $scope.totalDebt = '';
    $scope.secondaryMarketDebt = '';

    var calculateDebt = function() {
        var debt = $scope.debt;
        if(!isNaN(debt)) {
            $scope.totalDebt = $scope.debt * 1000
            $scope.secondaryMarketDebt = $scope.totalDebt * .05
        }
    };

    $scope.submit = function() {
        calculateDebt();
    };
});
