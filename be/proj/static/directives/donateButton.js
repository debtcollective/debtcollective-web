app.directive('donateButton', function ($window, $http) {
  return {
    restrict: 'E',
    scope: {
      'amount': '@',
      'flexbile': '='
    },
    transclude: true,
    replace: true,
    templateUrl: '/static/directives/donateButton.html',
    controller: function ($scope, $element, $attrs) {
      var handler = StripeCheckout.configure({
        key: 'pk_live_7W0RkZvaAs7dMs3vGkdSLTJh',
        token: function (token) {
          $http.post('/stripe_endpoint', {
            amount: $scope.amount,
            stripeToken: token
          })
        }

      });

      $scope.flexible = !!$attrs.flexible
      $scope.form = {
        flexibleAmount: ''
      }

      var panel = 'Donate'

      $element.find('button').on('click', function(e) {
        if ($scope.flexible) $scope.amount = $scope.form.flexibleAmount

        handler.open({
          name: 'Debt Collective',
          description: "$" + $scope.amount + " to the strike fund!",
          amount: $scope.amount * 100,
          panelLabel: panel,
          allowRememberMe: false
        });
        e.preventDefault();
      });

      // Close Checkout on page navigation
      $window.addEventListener('popstate', function() {
        handler.close();
      });
    }
  }
})