import requests

from availability_check import availability_check
from config import format_viewbook_url
import globals
from args import Args

from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


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
    },
}


def parse_fields(args: Args):
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
    # 1. Select Preferred Gym
    # globals.prefGymNameEN = "Qimo"
    # globals.prefGymNameEN = "Zongti"
    # globals.prefGymNameEN = "Xiti"
    # globals.prefGymNameEN = "Tennis"
    globals.prefGymNameEN = args.gym
    pref_fields = parse_fields(args)
    print("Target Gym:", args.gym)
    print("Target Courts:", pref_fields)

    if globals.prefGymNameEN == "Qimo":
        # 气膜羽毛球
        globals.prefGymNameCN = "气膜馆羽毛球场"
        globals.prefGymID = "3998000"
        globals.prefItemID = "4045681"

        # Qimo Courts: [羽01, 羽02, 羽03, 羽04, 羽05, 羽06, 羽07, 羽08, 羽09, 羽10, 羽11, 羽12]
        #       +--+--+--+--+--+--+
        #       |12|11|10|09|08|07|
        #  +----+--+--+--+--+--+--+
        #   ENTR|01|02|03|04|05|06|
        #  +----+--+--+--+--+--+--+

        # 2. Select Preferred Fields
        # pref_fields = ["羽10", "羽09", "羽11", "羽08", "羽12", "羽07", "羽04", "羽03", "羽05", "羽02", "羽06", "羽01"]
        # pref_fields = [
        #     "羽07",
        #     "羽06",
        #     "羽05",
        #     "羽04",
        #     "羽03",
        #     "羽02",
        #     "羽01",
        #     "羽12",
        #     "羽11",
        #     "羽10",
        #     "羽09",
        #     "羽08",
        # ]

        globals.viewbookURL = format_viewbook_url(
            globals.prefGymID, globals.prefItemID, globals.book_date
        )
        resp = session.get(globals.viewbookURL)
        qimo_tot_courts, qimo_cur_court_ids = availability_check(resp.text)

        PREF_SESSIONS = list(qimo_tot_courts.keys())
        PREF_SESSIONS.reverse()

        # [3, 2, 1, 0]
        # PREF_SESSIONS[0], PREF_SESSIONS[3] = PREF_SESSIONS[3], PREF_SESSIONS[0]
        # PREF_SESSIONS[1], PREF_SESSIONS[2] = PREF_SESSIONS[2], PREF_SESSIONS[1]

        for i in PREF_SESSIONS:
            for j in pref_fields:
                if (
                    qimo_tot_courts[i][j]["Court ID"] in qimo_cur_court_ids
                    and qimo_tot_courts[i][j]["Court Cost"] != "0.0"
                ):
                    globals.prefCourtCosts.append(
                        qimo_tot_courts[i][j]["Court Cost"]
                    )
                    globals.prefCourtIDs.append(qimo_tot_courts[i][j]["Court ID"])
                    globals.prefCourtInfos.append(i + " " + j)
                    globals.prefCourtTokens.append(
                        qimo_tot_courts[i][j]["Court Token"]
                    )

    elif globals.prefGymNameEN == "Zongti":
        # 综体羽毛球
        globals.prefGymNameCN = "综体羽毛球场"
        globals.prefGymID = "4797914"
        globals.prefItemID = "4797899"

        # Zongti Courts: [羽1, 羽2, 羽3, 羽4, 羽5, 羽6, 羽7, 羽8, 羽9, 羽10]
        #   +--+--+--+--+--+
        #   |06|07|08|09|10|
        #   +--+--+--+--+--+
        #   |01|02|03|04|05|
        #   +--+--+--+--+--+
        #    |ENTR|  |ENTR|
        #   +--+--+--+--+--+

        # 2. Select Preferred Fields
        # pref_fields = ["羽2", "羽1", "羽3", "羽7", "羽6", "羽8"]
        # pref_fields = ["羽4", "羽5", "羽9"]

        globals.viewbookURL = format_viewbook_url(
            globals.prefGymID, globals.prefItemID, globals.book_date
        )
        resp = session.get(globals.viewbookURL)
        zongti_tot_courts, zongti_cur_court_ids = availability_check(resp.text)

        PREF_SESSIONS = list(zongti_tot_courts.keys())
        PREF_SESSIONS.reverse()

        # Sessions Swap: [2, 1, 0, 3] instead of [0, 1, 2, 3]
        PREF_SESSIONS[0], PREF_SESSIONS[2] = PREF_SESSIONS[2], PREF_SESSIONS[0]
        # PREF_SESSIONS[1], PREF_SESSIONS[3] = PREF_SESSIONS[3], PREF_SESSIONS[1]

        for i in PREF_SESSIONS:
            for j in pref_fields:
                if (
                    zongti_tot_courts[i][j]["Court ID"] in zongti_cur_court_ids
                    and zongti_tot_courts[i][j]["Court Cost"] != "0.0"
                ):
                    globals.prefCourtCosts.append(
                        zongti_tot_courts[i][j]["Court Cost"]
                    )
                    globals.prefCourtIDs.append(
                        zongti_tot_courts[i][j]["Court ID"]
                    )
                    globals.prefCourtInfos.append(i + " " + j)
                    globals.prefCourtTokens.append(
                        zongti_tot_courts[i][j]["Court Token"]
                    )

    elif globals.prefGymNameEN == "Xiti":
        # 西体羽毛球
        globals.prefGymNameCN = "西体羽毛球场"
        globals.prefGymID = "4836273"
        globals.prefItemID = "4836196"

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

        # 2. Select Preferred Fields
        # pref_fields = ["羽5", "羽4", "羽6", "羽3", "羽2", "羽8", "羽7"]

        globals.viewbookURL = format_viewbook_url(
            globals.prefGymID, globals.prefItemID, globals.book_date
        )
        resp = session.get(globals.viewbookURL)
        xiti_tot_courts, xiti_cur_court_ids = availability_check(resp.text)

        PREF_SESSIONS = list(xiti_tot_courts.keys())
        PREF_SESSIONS.reverse()
        PREF_SESSIONS[0], PREF_SESSIONS[1] = PREF_SESSIONS[1], PREF_SESSIONS[0]

        for i in PREF_SESSIONS:
            for j in pref_fields:
                if (
                    xiti_tot_courts[i][j]["Court ID"] in xiti_cur_court_ids
                    and xiti_tot_courts[i][j]["Court Cost"] != "0.0"
                ):
                    globals.prefCourtCosts.append(
                        xiti_tot_courts[i][j]["Court Cost"]
                    )
                    globals.prefCourtIDs.append(xiti_tot_courts[i][j]["Court ID"])
                    globals.prefCourtInfos.append(i + " " + j)
                    globals.prefCourtTokens.append(
                        xiti_tot_courts[i][j]["Court Token"]
                    )

    elif globals.prefGymNameEN == "Tennis":
        # 紫网测试
        globals.prefGymNameCN = "紫荆网球场(测试)"
        globals.prefGymID = "5843934"
        globals.prefItemID = "5845263"

        # PREF_COURTS = [
        #     # "单打16",
        #     # "单打15",
        #     # "单打14",
        #     # "单打13",
        #     # "双打12",
        #     "双打11",
        #     "双打10",
        # ]

        globals.viewbookURL = format_viewbook_url(
            globals.prefGymID, globals.prefItemID, globals.book_date
        )
        resp = session.get(globals.viewbookURL)
        test_tot_courts, test_cur_court_ids = availability_check(resp.text)

        PREF_SESSIONS = list(test_tot_courts.keys())
        PREF_SESSIONS.reverse()

        for i in PREF_SESSIONS:
            for j in pref_fields:
                if (
                    test_tot_courts[i][j]["Court ID"] in test_cur_court_ids
                    and test_tot_courts[i][j]["Court Cost"] != "0.0"
                ):
                    globals.prefCourtCosts.append(
                        test_tot_courts[i][j]["Court Cost"]
                    )
                    globals.prefCourtIDs.append(test_tot_courts[i][j]["Court ID"])
                    globals.prefCourtInfos.append(i + " " + j)
                    globals.prefCourtTokens.append(
                        test_tot_courts[i][j]["Court Token"]
                    )
