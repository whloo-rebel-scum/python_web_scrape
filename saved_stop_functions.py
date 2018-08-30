import pandas as pd


# creates a new saved_stops.csv file
def create_saved_stops():
    routes = list()
    stops = list()
    saved_stops = pd.DataFrame({
        "Route": routes,
        "Stop": stops
    })
    saved_stops.to_csv("bus_stop_options.csv", encoding='utf-8', index=False)


# returns data frame read in from saved_stops.csv
def load_saved_stops():
    return pd.read_csv('saved_stops.csv')


# add an entry to saved_stops.csv
def add_to_saved_stops():
    print("Placeholder")
    # add to data frame
    # write data frame to file
    # or write directly to file in csv format?