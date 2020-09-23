# TDX Bulk Group Creation Script 1.0.0

## DISCLAIMER ##
This is **not an official TeamDynamix script** written by TeamDynamix engineers or developers. This was written by a non-developer to supplement the TDX-built and TDX-sanctioned scripts at https://www.github.com/TeamDynamix.

## Overview ##
This Python script will read user data from a .CSV file, connect to the TeamDynamix API , and create groups based on the parameters in this .CSV via the API. Responses from the API are logged to a CSV file that is automatically created.

## TeamDynamix Version Support ##
This script has been tested and validated on all TeamDynamix instances version **11.0 and higher.** If you run this on an earlier version of TeamDynamix, please let me know and I'll update the documentation!

## Dependencies ##
This script uses the Requests and Pandas libraries. You can install both by doing
```python
python -m pip install requests
```
and
```python
python -m pip install pandas
```

## CSV File Requirements ##
**CSV files must be in comma-separated format. Semicolons, pipes or any other delimiter are not supported.**

The CSV should include these columns, in this order:
**Name (Required)**</br>
*Data Type: String*</br>
The name of the group

**Description**</br>
*Data Type: String*</br>
Optional description for the group. Max 1,000 characters.

**Is Active**</br>
*Data Type: Boolean*</br>
Whether or not the group is active. Defaults to True.

**External ID**</br>
*Data Type: String*</br>
An alternate ID or code used to reference the group.

**Platform Applications**</br>
*Data Type: List of int*</br>
A comma-separated list of application IDs. Only ticketing applications are currently supported. You can find the ticketing application ID in TDAdmin under Applications.

## Script Parameters ##
This script requires all of the following parameters to be set:

**-f (filename=)**</br>
*Data Type: String*</br>
The file path to the CSV file of users to be added to the group. The file must contain one column (name irrelevant).

**-u (url=)**</br>
*Data Type: String*</br>
The base URL to the TeamDynamix Web API (typically ending with "/TDWebApi/"). Be sure to use your organization's custom domain URL for best results.
*SaaS Production Example: https://yourTeamDynamixDomain/TDWebApi/*
*SaaS Sandbox Example: https://yourTeamDynamixDomain/SBTDWebApi/*
*Install (On-Prem) Example: https://yourUrlToTDWebServer/TDWebApi/*

**-b (beid=)**</br>
*Data Type: String*</br>
The TeamDynamix Web Services BEID value. This is found in the TDAdmin application organization details page. In this page, there is a Security box or Tab which shows the Web Services BEID value if you have the Admin permission to **Add BE Administrators.** You will need to generate a web services key and enabled key-based services for this value to appear.

**-w (wskey=)**</br>
*Data Type: String*</br>
The TeamDynamix Web Services Key value. This is found in the TDAdmin application organization details page. In this page, there is a Security box or Tab which shows the Web Services Key value if you have the Admin permission to **Add BE Administrators.** You will need to generate a web services key and enabled key-based services for this value to appear.

**-g (groupID=)**</br>
*Data Type: Integer*</br>
The Group ID of the group you want to add these users to. Currently only accepts one group ID. Group IDs can be found in TDAdmin > Users & Roles > Groups.


## Usage Example ##
```python
python .\bulk-group-create.py -f "pathToImportData\importData.csv" -a "https://yourTeamDynamixDomain/TDWebApi/" -b "BEIDFromTDAdmin" -w "WSKeyFromTDAdmin" -g 123
```

## Feedback ##
Please direct all feedback to carrie.willis@teamdynamix.com.
