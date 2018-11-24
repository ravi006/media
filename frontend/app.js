var myApp = angular.module("myApp", ["ngRoute", "ngResource", "myApp.services"]);

var services = angular.module("myApp.services", ["ngResource"])
services
.factory('Band', function($resource) {
    return $resource('http://localhost:5000/api/v1/bands/:id', {id: '@id'}, {
        get: { method: 'GET' },
        delete: { method: 'DELETE' }
    });
})
.factory('Bands', function($resource) {
    return $resource('http://localhost:5000/api/v1/bands', {}, {
        query: { method: 'GET', isArray: true },
        create: { method: 'POST', }
    });
})
.factory('Youtubelist', function($resource) {
    return $resource('http://localhost:5000/api/v1/youtube/:id', {id: '@id'}, {
        get: { method: 'GET' }
    });
})
.factory('AfiremediaSearch', function($resource) {
    return $resource('http://localhost:5000/api/v1/afiresearch', {q: '@q'}, {
        query: { method: 'GET', isArray: true}
    });
});

myApp.config(function($routeProvider) {
    $routeProvider
    .when('/afiremedia', {
        templateUrl: 'pages/afire_main.html',
        controller: 'afireMainController'
    })
    .when('/afiremedia/newBand', {
        templateUrl: 'pages/band_new.html',
        controller: 'newBandController'
    })
    .when('/afiremedia/bands', {
        templateUrl: 'pages/bands.html',
        controller: 'bandListController'
    })
    .when('/afiremedia/bands/:id', {
        templateUrl: 'pages/band_details.html',
        controller: 'bandDetailsController'
    })
});

myApp.filter('filterStyles', function() {
  return function(input) {
    var output = new Array();
    for (i=0; i<input.length; i++) {
        if (input[i].checked == true) {
            output.push(input[i].name);
        }
    }
    return output;
  }
});


myApp.controller(
    'afireMainController',
    function ($scope, AfiremediaSearch) {
        $scope.search = function() {
            q = $scope.searchString;
            if (q.length > 1) {
                $scope.results = AfiremediaSearch.query({q: q});
            }
        };
    }
);

myApp.controller(
    'newBandController',
    function ($scope, YoutubeList, Bands, $location, $timeout, $filter) {
        $scope.bandname = Youtubelist.query();
        $scope.insertBeer = function () {
            $scope.band.bandname = $filter('filterStyles')($scope.YoutubeList);
            Bands.create($scope.band);
            $timeout(function (){
                $location.path('/bands').search({'created': $scope.band.bandname});
            }, 500);
        };
        $scope.cancel = function() {
            $location.path('/bands');
        };
    }

);

myApp.controller(
    'bandListController',
    function ($scope, Bands, Band, $location, $timeout) {
        if ($location.search().hasOwnProperty('created')) {
            $scope.created = $location.search()['created'];
        }
        if ($location.search().hasOwnProperty('deleted')) {
            $scope.deleted = $location.search()['deleted'];
        }
        $scope.deleteBand = function(band_id) {
            var deleted = Band.delete({id: band_id});
            $timeout(function(){
                $location.path('/bands').search({'deleted': 1})
            }, 500);
        };
        $scope.bands = Bands.query();
    }
);

myApp.controller(
    'bandDetailsController', ['$scope', 'Band', '$routeParams',
    function ($scope, Band, $routeParams) {
        $scope.band = Band.get({id: $routeParams.id});
    }
]);


