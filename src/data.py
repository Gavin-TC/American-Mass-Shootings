import tweeter
import csv
import os
import pandas as pd
import time
from datetime import datetime
from collections import deque

import csvretriever as ret

client = tweeter.client()
csv_location = "https://www.gunviolencearchive.org/query/0484b316-f676-44bc-97ed-ecefeabae077/export-csv"

def make_comparison():
    ret.get_new_csv()
    directory = ret.working_directory
    
    # put the csvs into variables
    oldest_csv = os.path.join(directory, ret.return_oldest_csv())
    newest_csv = os.path.join(directory, ret.return_newest_csv())
    
    # initialize shootings variables
    old_shootings = 0
    new_shootings = 0
    
    # count the number of mass shootings in each csv
    with open(oldest_csv, 'r') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            old_shootings += 1
    with open(newest_csv, 'r') as file:
        csvreader = csv.DictReader(file)
        for row in csvreader:
            new_shootings += 1
    
    # the difference between the # of shootings
    dif = new_shootings - old_shootings
    
    # essentially, if there's a new shooting
    if dif > 0 or True:
        # we should look through the last 10 entries and check what is new.
        check_entries = 10
                
        old_entries = []
        new_entries = []
        
        with open(oldest_csv, 'r') as file:
            csvreader = csv.DictReader(file)
            entries = list(csvreader)
            num_entries = len(entries)

            # Print the newest 10 entries in reverse order
            num_to_print = min(check_entries, num_entries)
                  
            for i in range(num_to_print-1, -1, -1):
                row = entries[i]
                old_entries.append(row)

        print()
        
        with open(newest_csv, 'r') as file:
            csvreader = csv.DictReader(file)
            entries = list(csvreader)
            num_entries = len(entries)

            # Print the newest 10 entries in reverse order
            num_to_print = min(check_entries, num_entries)
            for i in range(num_to_print-1, -1, -1):
                row = entries[i]
                new_entries.append(row)
        
        # lets check if new_entries has an entry that old_entries doesn't (i.e. a new shooting)
        for new_entry in new_entries:
            new_entry_id = new_entry["Incident ID"]
            
            found = True
            for old_entry in old_entries:
                old_entry_id = old_entry["Incident ID"]
                
                if new_entry_id == old_entry_id:
                    found = False
                    break
            
            # if we found a missing entry, we gotta tweet it
            if found:
                date = new_entry["Incident Date"]
                state = new_entry["State"]
                city = new_entry["City Or County"]
                injured = new_entry["# Victims Injured"]
                killed = new_entry["# Victims Killed"]

                #tweeter.tweet(client, f"""
                print(f"""
                    A mass shooting has occurred on {date} in {city}, {state}.

                    {injured} people were injured.
                    {killed} people were killed.
                    """)
                
                # wait 5 seconds to make next tweet just incase theres more shootings.
                time.sleep(5)
    
    # remove the old file
    os.remove(oldest_csv)

# def compare_dates():
#     get_csv.get_new_csv()

#     oldest_csv = os.path.join(get_csv.working_directory, get_csv.return_oldest_csv())
#     latest_csv = os.path.join(get_csv.working_directory, get_csv.return_newest_csv())

#     now = datetime.now()
#     today = now.strftime("%B %d, %Y")

#     old_incidents = 0
#     new_incidents = 0
    
#     # the incidents that have been detected and tweeted
#     reported_incidents = []
    
#     # the incidents inside the downloaded csv
#     total_incidents = []
    
#     # todo: i would like to check the last 10 entries in the csv and compare those.
#     # todo: have to tweet out the date now. 
    
#     # Check oldest CSV
#     with open(oldest_csv, 'r') as file:
#         print("Oldest csv is " + str(file.name))
#         csvreader = csv.DictReader(file)
#         for row in csvreader:
#             old_incidents += 1
    
#     # Check newest CSV
#     with open(latest_csv, 'r') as file:
#         print("Newest csv is " + str(file.name))
#         csvreader = csv.DictReader(file)
#         for row in csvreader:
#            new_incidents += 1

#     print(f"{old_incidents} old incidents")
#     print(f"{new_incidents} new incidents")

#     difference = new_incidents - old_incidents
    
#     print(difference > 0)

#     # if we have any incidents today, begin checks.
#     # if old_incidents >= 0:
#     # if there is a positive difference in incidents, continue
#     if difference > 0:
#         # now we need to read the oldest of the latest incident.
#         # i.e. 1 at 3pm, 1 at 4pm. read the one at 3pm first, then 4pm.
#         with open(latest_csv, 'r') as file:
#             csvreader = csv.DictReader(file)
#             mass_shootings = []

#             for row in csvreader:
#                 for x in range(difference):
#                     date = row["Incident Date"]
#                     city = row["City Or County"]
#                     state = row["State"]
#                     injured = row["# Victims Injured"]
#                     killed = row["# Victims Killed"]
#                     mass_shootings.append({"date": date, "city": city, "state": state, "injured": injured, "killed": killed})
            
#             num_to_print = min(difference, len(mass_shootings))
            
#             for i in range(num_to_print):
#                 shooting = mass_shootings[i]
#                 date = shooting["date"]
#                 city = shooting["city"]
#                 state = shooting["state"]
#                 injured = shooting["injured"]
#                 killed = shooting["killed"]
#                 total_shootings_today = len(mass_shootings)
#                 #tweeter.tweet(client, f"""
#                 print(f"""
#                 A mass shooting has occurred on {date} in {city}, {state}.

#                 {injured} people were injured.
#                 {killed} people were killed.
#                         """)
#     else:
#         print("There has not been any shootings so far today.")
    
#     # Remove the oldest CSV effectively making the newest CSV the new oldest.
#     time.sleep(0.5)
#     os.remove(oldest_csv)
#     #get_csv.remove_csv(oldest_csv)

