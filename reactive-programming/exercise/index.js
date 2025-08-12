"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var rxjs_1 = require("rxjs");
var operators_1 = require("rxjs/operators");
function randomCar() {
    var names = ['Speedster', 'Roadster', 'Cruiser', 'Phantom', 'Falcon'];
    var models = ['X1', 'GT', 'Turbo', 'Z', 'RS'];
    var brands = ['Tesla', 'Ford', 'BMW', 'Toyota', 'Honda', 'Hyundai', 'Scoda'];
    var colors = ['black', 'white', 'red', 'blue', 'grey'];
    return {
        name: names[Math.floor(Math.random() * names.length)],
        model: models[Math.floor(Math.random() * models.length)],
        yearOfRelease: 1975 + Math.floor(Math.random() * 51),
        brand: brands[Math.floor(Math.random() * brands.length)],
        color: colors[Math.floor(Math.random() * colors.length)],
    };
}
var observable1 = new rxjs_1.Observable(function (subscriber) {
    var interval = setInterval(function () {
        subscriber.next(randomCar());
    }, 1000);
});
var observable2 = observable1.pipe((0, operators_1.filter)(function (car) { return car.color === 'black' && car.yearOfRelease < 2000; }), (0, operators_1.map)(function (car) {
    return car;
}));
var observable3 = observable2.pipe((0, operators_1.map)(function (car) {
    return {
        brand: car.brand,
        yearOfRelease: car.yearOfRelease,
    };
}));
var carObserver = {
    next: function (car) {
        console.log(car);
    },
    error: function (err) {
        console.error('Error:', err);
    },
    complete: function () {
        console.log('Completed');
    }
};
var scrapObserver = {
    next: function (scrap) {
        console.log(scrap);
    },
    error: function (err) {
        console.error('Error:', err);
    },
    complete: function () {
        console.log('Completed');
    }
};
observable3.subscribe(scrapObserver);
