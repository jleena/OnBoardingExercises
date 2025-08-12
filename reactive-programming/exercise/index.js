"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var rxjs_1 = require("rxjs");
function randomCar() {
    var names = ['Speedster', 'Roadster', 'Cruiser', 'Phantom', 'Falcon'];
    var models = ['X1', 'GT', 'Turbo', 'Z', 'RS'];
    var brands = ['Tesla', 'Ford', 'BMW', 'Toyota', 'Honda', 'Hyundai', 'Scoda'];
    var colors = ['black', 'white', 'red', 'blue', 'grey'];
    return {
        name: names[Math.floor(Math.random() * names.length)],
        model: models[Math.floor(Math.random() * models.length)],
        yearOfRelease: 2000 + Math.floor(Math.random() * 25),
        brand: brands[Math.floor(Math.random() * brands.length)],
        color: colors[Math.floor(Math.random() * colors.length)],
    };
}
// Create an Observable1 which emits a new car every Interval of 1s. (using the previous function)
var observable1 = new rxjs_1.Observable(function (subscriber) {
    var interval = setInterval(function () {
        subscriber.next(randomCar());
    }, 1000);
});
var Observer = {
    next: function (value) {
        console.log("New car emitted: ".concat(JSON.stringify(value)));
    },
    error: function (err) {
        console.error("Error occurred: ".concat(err));
    },
    complete: function () {
        console.log('Observable completed');
    }
};
observable1.subscribe(Observer);
