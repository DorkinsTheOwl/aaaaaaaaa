import json
import os

problem = True


def get_result(routes):
    prices = [sum([a['price'] for a in route]) for route in routes]
    routes_prices = zip(prices, routes)
    sorted_routes_by_price = sorted(routes_prices, key=lambda x: x[0])
    best_option = [a['fid'] for a in sorted_routes_by_price[0][1]]
    return sorted(best_option, key=int)


def get_route_list(completed_route):
    r = []
    for item in completed_route:
        for route in item['routes']:
            r.append(route)

    return r


def filter_invalid_options(routes, itinerary):
    routes_list = get_route_list(routes)

    return len(routes_list) == len(itinerary) and all(elem in itinerary for elem in routes_list)


def completed_vs_itinerary(completed, itinerary):
    completed_itinerary = get_route_list(completed)
    return len(completed_itinerary) >= len(itinerary)


def solve_it():
    with open(os.environ["DATA_FILE"], 'r') as f:
        data = json.loads(f.read())

    # with open("./input.json", 'r') as f:
    #     data = json.loads(f.read())

    itinerary = data['itinerary']
    fares = data['fares']

    start = []
    consider_later = []

    # separate possible starting points from other options, they can't overlap anyways
    for fare in fares:
        if fare['routes'][0] == itinerary[0]:
            start.append(fare)
        else:
            consider_later.append(fare)

    # print(start)
    # print(consider_later)

    all_possible_valid_routes = []
    # for each item in starting options
    for item in start:
        # add it to completed route to begin with
        completed_route = [item]

        # check if completed route is not shorted than itinerary
        while not completed_vs_itinerary(completed_route, itinerary):
            # go through possible route options that we separated earlier
            for option in consider_later:
                # create list of routes from our dictionaries
                completed_route_list = get_route_list(completed_route)
                option_route_list = get_route_list([option])

                # if no routes in options are equal to routes in our completed route list, add those options
                if not any(r in completed_route_list for r in option_route_list):
                    completed_route.append(option)

        # add our completed route to all possible valid routes
        all_possible_valid_routes.append(completed_route)

    # check if routes are same length are same flights as itinerary
    filtered_results = [route for route in all_possible_valid_routes if filter_invalid_options(route, itinerary)]
    answer = get_result(filtered_results)

    with open(os.environ["RESULT_FILE"], 'w') as f:
        f.write(json.dumps(answer))


def main():
    if problem:
        solve_it()


if __name__ == "__main__":
    main()
