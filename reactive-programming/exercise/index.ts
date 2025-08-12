import { Observable, concat, interval } from 'rxjs';
import { map, filter, switchMap, concatMap, take, mergeMap } from 'rxjs/operators';
import axios from 'axios';

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

function apiCall(): Observable<any> {
    return new Observable(subscriber => {
        axios.get('https://jsonplaceholder.typicode.com/users')
            .then(response => {
                setTimeout(() => {
                    subscriber.next(response.data);
                    subscriber.complete();
                }, 1000);
            })
            .catch(error => {
                subscriber.error(error);
            })
    })
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

// Create an Observable4 which makes an api call to a free service every second. Ex. https://random-data-api.com/documentation (Hint: Use ‘switchMap’ operator) 

const observable4 = interval(1000).pipe(
    switchMap(() => apiCall()),
    map(data => {
        return data.map((user: any) => ({
            name: user.name
        }));
    }
    ));

const observable5 = interval(100).pipe(
    concatMap(() => apiCall()),
    map(data => {
        return data.map((user: any) => ({
            name: user.name
        }));
    })
    );

const observable6 = interval(50).pipe(
    mergeMap(() => apiCall()),
    take(5),
    map(data => {
        return data.map((user: any) => ({
            name: user.name
        }));
    })
)

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

// observable1.subscribe(carObserver);
// observable2.subscribe(carObserver);
// observable3.subscribe(scrapObserver);
// observable4.subscribe(data => console.log(data));
// observable5.subscribe(data => console.log(data));
observable6.subscribe(data => console.log(data));
