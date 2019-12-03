const fs = require('fs');
const _ = require('lodash');

// const prittyPrint = object => JSON.stringify(object, '', 2);
const data = JSON.parse(fs.readFileSync(process.env.DATA_FILE));
const { itinerary, fares } = data;


const completedVsItinerary = completed => {
    const completedList = getRoutesAsList(completed);

    return !itinerary.every(route => {
        return JSON.stringify(completedList).includes(JSON.stringify(route));
    });
};

const getRoutesAsList = routeObjects => {
    return routeObjects.reduce((acc, route) => {
        route.routes.forEach(r => {
            acc.push(r);
        });
        return acc;
    }, []);
};

const getLowestPricedRoute = validOptions => {
    const totalPriceAndOption = validOptions.map(validOption => {
        return validOption.reduce((acc, option) => {
            acc.price += option.price;
            acc.option.push(option);
            return acc;
        }, { price: 0, option: [] })
    });

    const bestOption = totalPriceAndOption.reduce((acc, data) => {
        return data.price < acc.price ? data : acc;
    }, totalPriceAndOption[0]);

    return bestOption.option.map(o => o.fid).sort((a, b) => +a - +b);
};


const { startingRoutes, considerLater } = fares.reduce((acc, fare) => {
    if (_.isEqual(fare.routes[0], itinerary[0])) {
        acc.startingRoutes.push(fare);
    } else {
        acc.considerLater.push(fare);
    }

    return acc;
}, { startingRoutes: [], considerLater: [] });

const allPossibleValidRoutes = startingRoutes.map(startingRoute => {
    let completedRoute = [_.cloneDeep(startingRoute)];

    while (completedVsItinerary(completedRoute)) {
        considerLater.forEach(option => {
            const completedRouteList = getRoutesAsList(completedRoute);
            const optionRouteList = getRoutesAsList([option]);

            if (optionRouteList.every(route => {
                return !completedRouteList.some(cRoute => {
                    return _.isEqual(cRoute, route);
                });
            })) {
                completedRoute.push(_.cloneDeep(option));
            }
        });
    }
    return completedRoute;
});

console.log(getLowestPricedRoute(allPossibleValidRoutes));
fs.writeFileSync(process.env.RESULT_FILE, getLowestPricedRoute(allPossibleValidRoutes));
