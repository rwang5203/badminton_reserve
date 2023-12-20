import requests

from availability_check import availability_check
from config import format_viewbook_url
from data import Data

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_prefs(session: requests.Session):

    """
    Get the reservation preferences for a given date.

    Args:
        session (requests.Session): The request session to use.
    """
        
    # [气膜："Qimo", 综体："Zongti", 西体："Xiti"]
    # 1. Select Preferred Gym
    Data.prefGymNameEN = "Qimo"
    # Data.prefGymNameEN = "Zongti"
    # Data.prefGymNameEN = "Xiti"
    # Data.prefGymNameEN = "Tennis"

    if Data.prefGymNameEN == "Qimo":
        # 气膜羽毛球
        Data.prefGymNameCN = "气膜馆羽毛球场"
        Data.prefGymID = "3998000"
        Data.prefItemID = "4045681"

        # Qimo Courts: [羽01, 羽02, 羽03, 羽04, 羽05, 羽06, 羽07, 羽08, 羽09, 羽10, 羽11, 羽12]
        #       +--+--+--+--+--+--+
        #       |12|11|10|09|08|07|
        #  +----+--+--+--+--+--+--+
        #   ENTR|01|02|03|04|05|06|
        #  +----+--+--+--+--+--+--+
        
        # 2. Select Preferred Fields
        # PREF_FIELDS = [ "羽10", "羽09", "羽11", "羽08", "羽12", "羽07", "羽04", "羽03", "羽05", "羽02", "羽06", "羽01"]
        PREF_FIELDS = ["羽07", "羽06", "羽05"]
        
        Data.viewbookURL = format_viewbook_url(Data.prefGymID, Data.prefItemID, Data.book_date)
        resp = session.get(Data.viewbookURL)
        qimo_tot_courts, qimo_cur_court_ids = availability_check(resp.text)
        
        PREF_SESSIONS = list(qimo_tot_courts.keys())
        PREF_SESSIONS.reverse()
        
        # [3, 2, 1, 0]
        # PREF_SESSIONS[0], PREF_SESSIONS[3] = PREF_SESSIONS[3], PREF_SESSIONS[0]
        # PREF_SESSIONS[1], PREF_SESSIONS[2] = PREF_SESSIONS[2], PREF_SESSIONS[1]

        for i in PREF_SESSIONS:
            for j in PREF_FIELDS:
                if qimo_tot_courts[i][j]["Court ID"] in qimo_cur_court_ids and qimo_tot_courts[i][j]["Court Cost"] != "0.0":
                    Data.prefCourtCosts.append(qimo_tot_courts[i][j]["Court Cost"])
                    Data.prefCourtIDs.append(qimo_tot_courts[i][j]["Court ID"])
                    Data.prefCourtInfos.append(i + " " + j)
                    Data.prefCourtTokens.append(qimo_tot_courts[i][j]["Court Token"])
    
    elif Data.prefGymNameEN == "Zongti":
        # 综体羽毛球
        Data.prefGymNameCN = "综体羽毛球场"
        Data.prefGymID = "4797914"
        Data.prefItemID = "4797899"

        # Zongti Courts: [羽1, 羽2, 羽3, 羽4, 羽5, 羽6, 羽7, 羽8, 羽9, 羽10]
        #   +--+--+--+--+--+
        #   |06|07|08|09|10|
        #   +--+--+--+--+--+
        #   |01|02|03|04|05|
        #   +--+--+--+--+--+
        #    |ENTR|  |ENTR|
        #   +--+--+--+--+--+
        
        # 2. Select Preferred Fields
        PREF_FIELDS = ["羽2", "羽1", "羽3", "羽7", "羽6", "羽8"]
        # PREF_FIELDS = ["羽4", "羽5", "羽9"]
        
        Data.viewbookURL = format_viewbook_url(Data.prefGymID, Data.prefItemID, Data.book_date)
        resp = session.get(Data.viewbookURL)
        zongti_tot_courts, zongti_cur_court_ids = availability_check(resp.text)

        PREF_SESSIONS = list(zongti_tot_courts.keys())
        PREF_SESSIONS.reverse()

        # Sessions Swap: [2, 1, 0, 3] instead of [0, 1, 2, 3]
        PREF_SESSIONS[0], PREF_SESSIONS[2] = PREF_SESSIONS[2], PREF_SESSIONS[0]
        # PREF_SESSIONS[1], PREF_SESSIONS[3] = PREF_SESSIONS[3], PREF_SESSIONS[1]

        for i in PREF_SESSIONS:
            for j in PREF_FIELDS:
                if zongti_tot_courts[i][j]["Court ID"] in zongti_cur_court_ids and zongti_tot_courts[i][j]["Court Cost"] != "0.0":
                    Data.prefCourtCosts.append(zongti_tot_courts[i][j]["Court Cost"])
                    Data.prefCourtIDs.append(zongti_tot_courts[i][j]["Court ID"])
                    Data.prefCourtInfos.append(i + " " + j)
                    Data.prefCourtTokens.append(zongti_tot_courts[i][j]["Court Token"])
    
    elif Data.prefGymNameEN == "Xiti":
        # 西体羽毛球
        Data.prefGymNameCN = "西体羽毛球场"
        Data.prefGymID = "4836273"
        Data.prefItemID = "4836196"

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
        PREF_FIELDS = ["羽5", "羽4", "羽6", "羽3", "羽2", "羽8", "羽7"]

        Data.viewbookURL = format_viewbook_url(Data.prefGymID, Data.prefItemID, Data.book_date)
        resp = session.get(Data.viewbookURL)
        xiti_tot_courts, xiti_cur_court_ids = availability_check(resp.text)
        
        PREF_SESSIONS = list(xiti_tot_courts.keys())
        PREF_SESSIONS.reverse()
        PREF_SESSIONS[0], PREF_SESSIONS[1] = PREF_SESSIONS[1], PREF_SESSIONS[0]

        for i in PREF_SESSIONS:
            for j in PREF_FIELDS:
                if xiti_tot_courts[i][j]["Court ID"] in xiti_cur_court_ids and xiti_tot_courts[i][j]["Court Cost"] != "0.0":
                    Data.prefCourtCosts.append(xiti_tot_courts[i][j]["Court Cost"])
                    Data.prefCourtIDs.append(xiti_tot_courts[i][j]["Court ID"])
                    Data.prefCourtInfos.append(i + " " + j)
                    Data.prefCourtTokens.append(xiti_tot_courts[i][j]["Court Token"])

    elif Data.prefGymNameEN == "Tennis":
        # 紫网测试
        Data.prefGymNameCN = "紫荆网球场(测试)"
        Data.prefGymID = "5843934"
        Data.prefItemID = "5845263"

        PREF_COURTS = ["单打16", "单打15", "单打14", "单打13", "双打12"]

        Data.viewbookURL = format_viewbook_url(Data.prefGymID, Data.prefItemID, Data.book_date)
        resp = session.get(Data.viewbookURL)
        test_tot_courts, test_cur_court_ids = availability_check(resp.text)
        
        PREF_SESSIONS = list(test_tot_courts.keys())
        PREF_SESSIONS.reverse()

        for i in PREF_SESSIONS:
            for j in PREF_COURTS:
                if test_tot_courts[i][j]["Court ID"] in test_cur_court_ids and test_tot_courts[i][j]["Court Cost"] != "0.0":
                    Data.prefCourtCosts.append(test_tot_courts[i][j]["Court Cost"])
                    Data.prefCourtIDs.append(test_tot_courts[i][j]["Court ID"])
                    Data.prefCourtInfos.append(i + " " + j)
                    Data.prefCourtTokens.append(test_tot_courts[i][j]["Court Token"])