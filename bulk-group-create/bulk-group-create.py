"""
        Bulk Group Create Tool
        for TeamDynamix 11.1+
        by github.com/carriehwillis
"""

import requests, json # Used for sending API calls
import csv # Used to read the CSV file of data to send via API
import pandas as pd # Used to format lists as CSVs; want to deprecate this
import time, sys, getopt # Allows receiving arguments from the command line
from datetime import datetime # For timestamping the logs

def jprint(obj):
    """ Prints a JSON object as text.

    Args:
        obj (JSON object): The JSON object to print.
    """

    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def loadData(src):
    """ Loads data from a CSV and returns a list.

    Args:
        src (str): The path to the CSV file to load.

    Returns:
        users (list of str): Users to add to the group
    """

    data = []
    with open(src) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # This skips the first row of the CSV file.
        next(csvReader)
        for row in csvReader:
            data.append(row)
    return data

def exportData(data, columns):
    """ Creates a Pandas dataframe from a list and exports to CSV.
    Used to create a log file for the API calls; good for troubleshooting.

    Args:
        data (list of str): The data that should be exported to CSV
        columns (list of str): The column names for the CSV
    """

    # TODO: Replace pandas with regular CSV method

    output = pd.DataFrame(data, columns = columns)
    try:
        with open('logs.csv', 'a') as f:
            output.to_csv(f, mode = 'a', header=False)
    except IOError:
        output.to_csv('logs.csv', header=columns)

def auth(gurl, beid, wskey):
    """ Formats the provided TDX information into the appropriate format,
        uses Requests to get a bearer token, then returns HTTP headers.

    Args:
        gurl (str): the API URL of the TeamDynamix environment
        beid (str): TeamDynamix environment BEID
        wskey (str): TeamDynamix environment Web Services Key

    Returns:
        headers (str): A string including the content-type and bearer token, used
            for future API calls to TDX; bearer is only valid for this session
    """

    data = {
        "BEID": beid,
        "WebServicesKey": wskey
    }

    bearer = requests.post(
        url = gurl + "/api/auth/loginadmin",
        json = data
    )

    token = str(bearer.content, "utf-8")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    return headers

def process(item):
    """ Deals with a bunch of cases of missing data and ensures correct type.

    Args:
        item (list of str): Comma-separated list of group attributes

    Returns:
        item (list): List of int, str, and list(str)
    """

    # There's got to be a more Pythonic way of doing this...

    # If IsActive is provided, make it a bool. Otherwise, default to True
    # Allows "0", "False", or "No" for False, and "1", "True", or "Yes" for True
    if str(item[3]).strip().upper() == "0" or str(item[3]).strip().upper() == "FALSE" or str(item[3]).strip().upper() == "NO":
        item[3] = False
    else:
        item[3] = True

    # Deal with case of ", " or "," delimiter; make list
    # if len(item[5]) > 0:
    #     item[5] = item[5].replace(" ", "").split(",")
    # TODO: Allow for multiple platform apps; right now only accepts one
        # Method for this: split item[5] on "," (" ,") and replace item[5]
        # with new list. Then, for entry in item[5], newlist.append(
        # "{\"AppID\": " + item + "}") -- then item[5] = newlist

    return item

def createGroup(list, headers, gurl):
    """ Makes API call to TDX to create groups, adding results of each call
    to a list, then calls method to write error list to a CSV.

    Args:
        headers (str): HTTP headers, including bearer token, for the API call
        gurl (str): the API URL of the TeamDynamix environment
        list (list of str): the parameters for the group
    """

    logs = []
    params = {
        "Name" : list[0],
        "Description" : list[1],
        "IsActive" : list[2],
        "ExternalID" : list[3],
        "PlatformApplications" : [{"GroupID" : list[0], "AppID" : list[4]}]
    }

    response = requests.post(
        url = gurl + "/api/groups/",
        headers = headers,
        json = params
    )

    print(response)
    logs.append([datetime.now(), response.status_code, response.reason, response.content])
    # Export to CSV
    exportData(logs, ["Time", "Code", "Reason", "Content"])

def main(argv):
    """ Processes the arguments and calls methods.
    Args:
        argv (list of str): Arguments from the command line
    """

    src = ""
    gurl = ""
    beid = ""
    wskey = ""
    if len(sys.argv) < 5:
        print("Please enter all required arguments.")
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv,"f:u:b:w:", ["filename=", "url=", "beid=", "wskey="])
    except getopt.GetoptError:
        print("Failed.")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-f":
            src = arg
        elif opt == "-u":
            gurl = arg
        elif opt == "-b":
            beid = arg
        elif opt == "-w":
            wskey = arg

    csv = loadData(src)
    headers = auth(gurl, beid, wskey)
    for row in csv:
        createGroup(process(row), headers, gurl)
        time.sleep(1) # to avoid rate limitation; could probably do this a better way


if __name__ == "__main__":
    main(sys.argv[1:])
