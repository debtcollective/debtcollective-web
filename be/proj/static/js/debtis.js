var app = angular.module('myDebtIs', [
    'ngRoute',
    'ngCookies',
    'duScroll',
    'ui.bootstrap'
]);

app.run(function run($http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
})

app.value('duScrollDuration', 1000)
app.config(function($interpolateProvider, $routeProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});