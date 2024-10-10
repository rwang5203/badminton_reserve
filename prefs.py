import requests
from availability_check import get_available_courts
from config import format_viewbook_url
import globals
from urllib3.exceptions import InsecureRequestWarning
import urllib3
from typing import List
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

GYM_NAMES_ZH = {
    "Qimo": "气膜馆羽毛球场",
    "Zongti": "综体羽毛球场",
    "Xiti": "西体羽毛球场",
    "Tennis": "紫荆网球场（测试）",
}

GYM_IDS = {
    "Qimo": "3998000",
    "Zongti": "4797914",
    "Xiti": "4836273",
    "Tennis": "5843934",
}

ITEM_IDS = {
    "Qimo": "4045681",
    "Zongti": "4797899",
    "Xiti": "4836196",
    "Tennis": "5845263",
}


def parse_fields(fields: List[int], target_gym_name: str) -> List[str]:
    parsed_fields = []
    for field in fields:
        if isinstance(field, int):
            parsed_fields.append(FIELDS[target_gym_name][field])
        elif isinstance(field, str):
            parsed_fields.append(field)
        else:
            raise TypeError(f"Invalid court: {field}")
    assert len(fields) == len(fields)
    return parsed_fields


def get_available_target_courts(
    session: requests.Session,
    target_gym_name: str,
    fields: List[int],
    preference: str = "late",
    accept_free_courts: bool = False,
) -> dict:
    """
    Get the reservation preferences for a given date.

    Args:
        session (requests.Session): The request session to use.
    """
    # [气膜："Qimo", 综体："Zongti", 西体："Xiti"]
    globals.target_gym_name = target_gym_name
    pref_fields: List[str] = parse_fields(
        fields,
        target_gym_name=target_gym_name,
    )
    log(f"Target gym: {target_gym_name}")
    log(f"Target courts: {pref_fields}")

    globals.target_gym_name_zh = GYM_NAMES_ZH[target_gym_name]
    globals.target_gym_id = GYM_IDS[target_gym_name]
    globals.target_gym_item_id = ITEM_IDS[target_gym_name]
    globals.view_book_url = format_viewbook_url(
        globals.target_gym_id,
        globals.target_gym_item_id,
        globals.target_date,
    )
    resp = session.get(globals.view_book_url)

    log("Checking for availability...")
    all_court_data, empty_court_ids = get_available_courts(resp.text)
    log(f"{empty_court_ids = }")
    target_sessions = list(all_court_data.keys())

    if preference == 'early':
        target_sessions = target_sessions[3:]
    elif preference == 'noon':
        target_sessions = target_sessions[len(target_sessions) // 2 :]  # 约中午
    elif preference == 'late':
        target_sessions.reverse()  # Prioritize later sessions

    log(f"Target sessions (ordered by priority): {target_sessions}")

    if globals.target_gym_name == "Qimo":
        pass
    elif globals.target_gym_name == "Zongti":
        target_sessions[0], target_sessions[2] = target_sessions[2], target_sessions[0]
    elif globals.target_gym_name == "Xiti":
        target_sessions[0], target_sessions[1] = target_sessions[1], target_sessions[0]
    elif globals.target_gym_name == "Tennis":
        pass

    # Find preferred fields and sessions
    target_costs: List[str] = []
    target_infos: List[str] = []
    target_ids: List[str] = []
    target_tokens: List[str] = []
    for i in target_sessions:
        for j in pref_fields:
            if (
                all_court_data[i][j]["Court ID"] in empty_court_ids
            ):
                if all_court_data[i][j]["Court Cost"] != "0.0" or accept_free_courts:
                    target_costs.append(all_court_data[i][j]["Court Cost"])
                    target_ids.append(all_court_data[i][j]["Court ID"])
                    target_infos.append(i + " " + j)
                    target_tokens.append(all_court_data[i][j]["Court Token"])
    return {
        "costs": target_costs,
        "infos": target_infos,
        "ids": target_ids,
        "tokens": target_tokens,
    }
