import requests
from availability_check import availability_check
from config import format_viewbook_url
import globals
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from utils import log

urllib3.disable_warnings(InsecureRequestWarning)

# Qimo Courts: [羽01, 羽02, 羽03, 羽04, 羽05, 羽06, 羽07, 羽08, 羽09, 羽10, 羽11, 羽12]
#       +--+--+--+--+--+--+
#       |12|11|10|09|08|07|
#  +----+--+--+--+--+--+--+
#   ENTR|01|02|03|04|05|06|
#  +----+--+--+--+--+--+--+


# Zongti Courts: [羽1, 羽2, 羽3, 羽4, 羽5, 羽6, 羽7, 羽8, 羽9, 羽10]
#   +--+--+--+--+--+
#   |06|07|08|09|10|
#   +--+--+--+--+--+
#   |01|02|03|04|05|
#   +--+--+--+--+--+
#    |ENTR|  |ENTR|
#   +--+--+--+--+--+

# Xiti Courts: [羽1, 羽2, 羽3, 羽4, 羽5, 羽6, 羽7, 羽8]
#       +--+--+
#       |04|08|
#  +----+--+--+----+
#   HOOP|03|07|HOOP
#  +----+--+--+----+
#       |02|06|
#  +----+--+--+
#   ENTR|01|05|
#  +----+--+--+


FIELDS = {
    "Qimo": {
        1: "羽01",
        2: "羽02",
        3: "羽03",
        4: "羽04",
        5: "羽05",
        6: "羽06",
        7: "羽07",
        8: "羽08",
        9: "羽09",
        10: "羽10",
        11: "羽11",
        12: "羽12",
    },
    "Zongti": {
        1: "羽1",
        2: "羽2",
        3: "羽3",
        4: "羽4",
        5: "羽5",
        6: "羽6",
        7: "羽7",
        8: "羽8",
        9: "羽9",
        10: "羽10",
    },
    "Xiti": {
        1: "羽1",
        2: "羽2",
        3: "羽3",
        4: "羽4",
        5: "羽5",
        6: "羽6",
        7: "羽7",
        8: "羽8",
    },
    "Tennis": {
        16: "单打16",
        15: "单打15",
        14: "单打14",
        13: "单打13",
        12: "双打12",
        11: "双打11",
        10: "双打10",
        9: "双打9",
        8: "双打8",
        7: "双打7",
        6: "双打6",
        5: "双打5",
        4: "双打4",
        3: "双打3",
        2: "双打2",
        1: "双打1",
    },
}

GYN_NAME_CN = {
    "Qimo": '气膜馆羽毛球场',
    "Zongti": '综体羽毛球场',
    "Xiti": '西体羽毛球场',
    "Tennis": '紫荆网球场（测试）',
}

GYM_ID = {
    "Qimo": '3998000',
    "Zongti": '4797914',
    "Xiti": '4836273',
    "Tennis": '5843934',
}

ITEM_ID = {
    "Qimo": '4045681',
    "Zongti": '4797899',
    "Xiti": '4836196',
    "Tennis": '5845263',
}


def parse_fields(args):
    fields = []
    for field in args.fields:
        if isinstance(field, int):
            fields.append(FIELDS[args.gym][field])
        elif isinstance(field, str):
            fields.append(field)
        else:
            raise TypeError(f"Invalid court: {field}")
    assert len(fields) == len(args.fields)
    return fields


def get_prefs(session: requests.Session, args):
    """
    Get the reservation preferences for a given date.

    Args:
        session (requests.Session): The request session to use.
    """
    # [气膜："Qimo", 综体："Zongti", 西体："Xiti"]
    globals.prefGymNameEN = args.gym
    pref_fields = parse_fields(args)
    log(f"Target Gym: {args.gym}")
    log(f"Target Courts: {pref_fields}")

    globals.prefGymNameCN = GYN_NAME_CN[args.gym]
    globals.prefGymID = GYM_ID[args.gym]
    globals.prefItemID = ITEM_ID[args.gym]
    globals.viewbookURL = format_viewbook_url(
        globals.prefGymID, globals.prefItemID, globals.book_date
    )
    resp = session.get(globals.viewbookURL)
    empty_courts, empty_court_ids = availability_check(resp.text)
    pref_sessions = list(empty_courts.keys())
    pref_sessions.reverse()  # Prioritize later sessions

    if globals.prefGymNameEN == "Qimo":
        pass
    elif globals.prefGymNameEN == "Zongti":
        pref_sessions[0], pref_sessions[2] = pref_sessions[2], pref_sessions[0]
    elif globals.prefGymNameEN == "Xiti":
        pref_sessions[0], pref_sessions[1] = pref_sessions[1], pref_sessions[0]
    elif globals.prefGymNameEN == "Tennis":
        pass

    # Find preferred fields and sessions
    for i in pref_sessions:
        for j in pref_fields:
            if (
                empty_courts[i][j]["Court ID"] in empty_court_ids
                and empty_courts[i][j]["Court Cost"] != "0.0"
            ):
                globals.prefCourtCosts.append(
                    empty_courts[i][j]["Court Cost"]
                )
                globals.prefCourtIDs.append(
                    empty_courts[i][j]["Court ID"]
                )
                globals.prefCourtInfos.append(i + " " + j)
                globals.prefCourtTokens.append(
                    empty_courts[i][j]["Court Token"]
                )
