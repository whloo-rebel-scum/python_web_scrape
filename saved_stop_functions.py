import pandas as pd
import csv


# creates a new saved_stops.csv file
def create_saved_stops():
    routes = list()
    stops = list()
    saved_stops = pd.DataFrame({
        "Route": routes,
        "Stop": stops
    })
    saved_stops.to_csv("saved_stops.csv", encoding='utf-8', index=False)


# returns data frame read in from saved_stops.csv
# dependent on create_saved_stops
def load_saved_stops():
    # use while loop instead to reduce number of lines?
    try:
        saved_stops = pd.read_csv('saved_stops.csv')
        return saved_stops
    except FileNotFoundError:  # create a new saved_stops file if none exists
        create_saved_stops()
        saved_stops = pd.read_csv('saved_stops.csv')
        return saved_stops


# add an entry to saved_stops.csv
def add_to_saved_stops(route, stop):
    # format a new row, write to the csv file
    new_stop = [route, stop]
    with open(r'saved_stops.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(new_stop)
    print("Stop saved. Saved stops: ")
    print(load_saved_stops().to_string(index=False))


# write a data frame back to saved_stops.csv
def write_to_saved_stops(df):
    df.to_csv("saved_stops.csv", encoding='utf-8', index=False)


# remove a stop from the csv file
def remove_saved_stop(saved_stops):
    print(saved_stops.to_string(index=True))
    remove_choice = input("Choose a stop to remove (by index): ")
    remove_choice = remove_choice.replace(' ', '')  # eliminate whitespace
    # load data frame
    ss = load_saved_stops()
    # remove by index
    ss.drop(ss.index[int(remove_choice)], inplace=True)
    print("New saved stops list: ")
    if ss.empty:
        print("No stops saved.")
    else:
        print(ss.to_string(index=False))
    write_to_saved_stops(ss)
