# IoT Message Format Specification
## Basic Structure
{
    "cri": AD1024007,
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": 1, "v": 1.802},
        {"oc": 0, "sri": 2, "v": 5.706}
    ],
    "ts": 1739538240
}


## Field Definitions
### Sensor Values (sv)
SRI (Sensor Relative ID) mappings:
- sri: 1 - Flow (L/min)
- sri: 2 - PM 1
- sri: 3 - PM 1 - 10 Min Avg
- sri: 4 - PM 1 - 1.5 Hour Avg
- sri: 5 - PM 1 - 9 Hours Avg
- sri: 6 - PM 1 - 1 Day Avg
- sri: 7 - PM 2.5
- sri: 8 - PM 2.5 - 10 Min Avg
- sri: 9 - PM 2.5 - 1.5 Hour Avg
- sri: 10 - PM 2.5 - 9 Hours Avg
- sri: 11 - PM 2.5 - 1 Day Avg
- sri: 12 - PM 4.25
- sri: 13 - PM 4.25 - 10 Min Avg
- sri: 14 - PM 4.25 - 1.5 Hour Avg
- sri: 15 - PM 4.25 - 9 Hours Avg
- sri: 16 - PM 4.25 - 1 Day Avg
- sri: 17 - PM 10
- sri: 18 - PM 10 - 10 Min Avg
- sri: 19 - PM 10 - 1.5 Hour Avg
- sri: 20 - PM 10 - 9 Hours Avg
- sri: 21 - PM 10 - 1 Day Avg
- sri: 22 - TSP
- sri: 23 - TSP - 10 Min Avg
- sri: 24 - TSP - 1.5 Hour Avg
- sri: 25 - TSP - 8 Hours Avg
- sri: 26 - TSP - 1 Day Avg


### Other Fields
- cri: Sensor ID number
- mt: Message type (0)
- sc: Device count
- ts: YY/MM/DD M:SS


## Topic Format
Topic: liveaide/poc/[DEVICE_ID]/district
Example: liveaide/poc/MD1024007/district
