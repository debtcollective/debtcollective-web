var app = angular.module('myDebtIs', [
    'ngCookies',
    'duScroll'
]);

app.run(function run($http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
})

app.value('duScrollDuration', 1000)
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.controller('myDebtIsCtrl', function ($scope) {
    $scope.debtType = 'salliemae';

    $scope.resetState = function() {
        $scope.total = 0;
        $scope.secondaryMarketDebt = 0;
        $scope.totalInterest = 0;
        $scope.BEGINNING_PRINCIPAL = 0;
        $scope.ESTIMATED_INTEREST = .068;
        $scope.ESTIMATED_YEARS = 20;
    }
    $scope.resetState()

    var getDebtMarketPrice = function() {
        var price = 1
        switch($scope.debtType) {
            case 'federal':
                price = 1.05
                break
            case 'salliemae':
                price = .15
                break
        }
        return $scope.BEGINNING_PRINCIPAL * price
    }

    var calculateDebt = function(debt, interest, yearsLeft) {
        if (yearsLeft <= 0) {
            $scope.total = $scope.BEGINNING_PRINCIPAL + interest
            $scope.totalInterest = interest
            $scope.secondaryMarketDebt = getDebtMarketPrice()
            return
        }
        var interestPaid = debt * $scope.ESTIMATED_INTEREST
        return calculateDebt(debt - interestPaid, interest + interestPaid, yearsLeft - 1)
    }

    $scope.submit = function() {
        debt = parseFloat($scope.debt.replace(',', ''))
        if (!isNaN(debt) && debt != '') {
            $scope.BEGINNING_PRINCIPAL = debt
            calculateDebt(debt, 0, $scope.ESTIMATED_YEARS);
            $scope.showValues = true
        }
        else {
            $scope.showValues = false
            $scope.resetState()
        }
    };
});
