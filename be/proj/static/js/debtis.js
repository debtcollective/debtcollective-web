var app = angular.module('myDebtIs', [
    'ngCookies'
]);

app.run(function run($http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
})

app.controller('splashBodyCtrl', function ($scope, $http, util_svc) {

    $scope.email = null;
    $scope.username = null

    $scope.onSubmitClick = function () {
        $scope.username = util_svc.generateUUID();

        data = {
            'username': $scope.username,
            'password': $scope.email,
        }

        $http.post('/signup/', data).then(function (resp) {

        });
    }
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

app.filter('humanize', function(){
    return function humanize(number) {
        if(number < 1000) {
            return Math.round(number);
        }
        var si = ['K', 'M', 'G', 'T', 'P', 'H'];
        var exp = Math.floor(Math.log(number) / Math.log(1000));
        var result = number / Math.pow(1000, exp);
        result = (result % 1 > (1 / Math.pow(1000, exp - 1))) ? result.toFixed(2) : result.toFixed(0);
        return result + si[exp - 1];
    };
});
