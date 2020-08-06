"""
        Bulk Group Membership Tool
        for TeamDynamix 11.1
        by carrodactyl

"""

import requests, json
import csv
import pandas as pd
import time, sys, getopt
from datetime import datetime

def jprint(obj):
    text = json.dumps(obj, sort_keys=False, indent=4)
    print(text)

def loadData(src):
    #df = pd.read_csv(src)
    #df = df.applymap(str)

    users = []
    with open(src) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        # This skips the first row of the CSV file.
        next(csvReader)
        for row in csvReader:
            users.append(row[0])

    return users

def exportData(data, columns):
    output = pd.DataFrame(data, columns = columns)
    try:
        with open('logs.csv', 'a') as f:
            output.to_csv(f, mode = 'a', header=False)
    except IOError:
        output.to_csv('logs.csv', header=columns)

def auth(gurl, beid, wskey):
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

########################################
##  Populate group with users in CSV
########################################

def populateGroup(headers, gurl, users, groupID):
    logs = []
    print(headers, gurl, users, groupID)

    bulkParameters = {"UserUIDs" : users, "GroupIDs" : groupID, "RemoveOtherGroups" : False}
    parameters = json.dumps(bulkParameters, indent = 4)
    print(parameters)
    response = requests.post(
        url = gurl + "/api/people/bulk/managegroups",
        headers = headers,
        json = bulkParameters
    )
    logs.append([datetime.now(), response.status_code, response.reason, response.content])
    exportData(logs, ["Time", "Code", "Reason", "Content"])
    print(response)

    time.sleep(1) # to avoid rate limitation


def main(argv):
    src = ""
    gurl = ""
    beid = ""
    wskey = ""
    groupID = []
    if len(sys.argv) < 6:
        print("Please enter all required arguments.")
        sys.exit(2)
    try:
        opts, args = getopt.getopt(argv,"f:u:b:w:g:", ["filename=", "url=", "beid=", "wskey=", "groupid="])
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
        elif opt == "-g":
            groupID.append(int(arg))

    users = loadData(src)
    headers = auth(gurl, beid, wskey)
    print(headers)
    populateGroup(headers, gurl, users, groupID)

if __name__ == "__main__":
    main(sys.argv[1:])
