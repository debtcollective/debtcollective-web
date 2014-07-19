var app = angular.module('myDebtIs', []);

app.controller('myDebtIsCtrl', function ($scope) {

    $scope.debt = 0;
    $scope.total = 0;
    $scope.secondaryMarketDebt = 0;
    $scope.debtType = 'Private';

    $scope.BEGINNING_PRINCIPAL = 0;
    $scope.ESTIMATED_INTEREST = .068;
    $scope.ESTIMATED_YEARS = 20

    var calculateDebt = function(debt, interest, yearsLeft) {
        if (yearsLeft <= 0) {
            return $scope.BEGINNING_PRINCIPAL + interest
        }
        var interestPaid = debt * $scope.ESTIMATED_INTEREST
        return calculateDebt(debt - interestPaid, interest + interestPaid, yearsLeft - 1)
    }

    $scope.submit = function() {
        debt = parseFloat($scope.debt)
        if (!isNaN(debt) && debt != '') {
            $scope.BEGINNING_PRINCIPAL = debt
            $scope.total = calculateDebt(debt, 0, $scope.ESTIMATED_YEARS);
            $scope.secondaryMarketDebt = $scope.total * .05
        }
    };
});

app.filter('humanize', function(){
    return function humanize(number) {
        if(number < 1000) {
            return number;
        }
        var si = ['K', 'M', 'G', 'T', 'P', 'H'];
        var exp = Math.floor(Math.log(number) / Math.log(1000));
        var result = number / Math.pow(1000, exp);
        result = (result % 1 > (1 / Math.pow(1000, exp - 1))) ? result.toFixed(2) : result.toFixed(0);
        return result + si[exp - 1];
    };
});
