import { Observable, Subject } from 'rxjs';
import { map, filter } from 'rxjs/operators';

interface Car {
    name: string;
    model: string;
    yearOfRelease: number;
    brand: string;
    color: string;
}

interface Scrap {
    brand: string,
    yearOfRelease: number
}

function randomCar(): Car {
  const names = ['Speedster', 'Roadster', 'Cruiser', 'Phantom', 'Falcon'];
  const models = ['X1', 'GT', 'Turbo', 'Z', 'RS'];
  const brands = ['Tesla', 'Ford', 'BMW', 'Toyota', 'Honda', 'Hyundai', 'Scoda'];
  const colors = ['black', 'white', 'red', 'blue', 'grey'];

  return {
    name: names[Math.floor(Math.random() * names.length)],
    model: models[Math.floor(Math.random() * models.length)],
    yearOfRelease: 1975 + Math.floor(Math.random() * 51),
    brand: brands[Math.floor(Math.random() * brands.length)],
    color: colors[Math.floor(Math.random() * colors.length)],
  };
}

const observable1 = new Observable<Car>(subscriber => {
    const interval = setInterval(() => {
        subscriber.next(randomCar());
    }, 1000);
})

const observable2 = observable1.pipe(
    filter(car => car.color === 'black' && car.yearOfRelease < 2000),
    map(car => {
        return car;
    })
);

const observable3 = observable2.pipe(
    map(car => {
        return {
            brand: car.brand,
            yearOfRelease: car.yearOfRelease,
        };
    })
);

const carObserver = {
    next: (car: Car) => {
        console.log(car);
    },
    error: (err: any) => {
        console.error('Error:', err);
    },
    complete: () => {
        console.log('Completed');
    }
}
const scrapObserver = {
    next: (scrap: Scrap) => {
        console.log(scrap);
    },
    error: (err: any) => {
        console.error('Error:', err);
    },
    complete: () => {
        console.log('Completed');
    }
};

observable3.subscribe(scrapObserver);