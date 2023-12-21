# import datetime
import re
import requests

import globals
from utils import log


def search_reserved(text):
    total_reserved = re.findall(
        "(?<=markResStatus\('\d{8}',')(.*?)(?=',')", text
    )
    return total_reserved


def search_total(text):
    total_court_ids = re.findall(
        "(?<=resourceArray.push\(\{id:')(.*?)(?=',)", text
    )
    total_time_sessions = re.findall("(?<=time_session:')(.*?)(?=',)", text)
    total_field_names = re.findall("(?<=field_name:')(.*?)(?=',)", text)
    total_costs = []
    total_tokens = []
    for id in total_court_ids:
        total_costs.append(
            re.search(
                "(?<=addCost\('{}',')(.*?)(?='\);)".format(id), text
            ).group()
        )
        total_tokens.append(
            re.search(
                "(?<=resourcesm.put\('{}', ')(.*?)(?='\);)".format(id), text
            ).group()
        )
    return (
        total_court_ids,
        total_time_sessions,
        total_field_names,
        total_costs,
        total_tokens,
    )


def availability_check(text):
    total_reserved = search_reserved(text)
    (
        total_court_ids,
        total_time_sessions,
        total_field_names,
        total_costs,
        total_tokens,
    ) = search_total(text)
    dict = {}
    total_time_sessions = list(dict.fromkeys(total_time_sessions))
    count = 0
    for time_sessions in range(len(total_time_sessions)):
        if (
            int(len(total_field_names) / len(total_time_sessions))
            == int(len(total_court_ids) / len(total_time_sessions))
            == int(len(total_costs) / len(total_time_sessions))
        ):
            avg = int(len(total_court_ids) / len(total_time_sessions))
        item_time_sessions = {}
        for field_names in total_field_names[
            time_sessions * avg : (time_sessions + 1) * avg
        ]:
            item_field_names = {}
            item_field_names["Court ID"] = total_court_ids[count]
            item_field_names["Court Cost"] = total_costs[count]
            item_field_names["Court Token"] = total_tokens[count]
            count += 1
            item_time_sessions[field_names] = item_field_names
        dict[total_time_sessions[time_sessions]] = item_time_sessions
    total = []
    prefs = list(dict.keys())
    prefs.reverse()

    for first_key, value in dict.items():
        for sec_key in value.items():
            total.append(sec_key[1]["Court ID"])

    available_ids = [x for x in total if x not in total_reserved]

    return dict, available_ids


def availability_update():
    session = requests.Session()
    res = session.get(globals.viewbookURL)
    _, globals.validCourtIDs = availability_check(res.text)
    globals.validCourtIDs.reverse()

    valid_indices = [
        globals.prefCourtIDs.index(x)
        for x in globals.validCourtIDs
        if x in globals.prefCourtIDs
    ]

    globals.prefCourtIDs = [globals.prefCourtIDs[i] for i in valid_indices]
    globals.prefCourtCosts = [globals.prefCourtCosts[i] for i in valid_indices]
    globals.prefCourtTokens = [globals.prefCourtTokens[i] for i in valid_indices]
    globals.prefCourtInfos = [globals.prefCourtInfos[i] for i in valid_indices]
    log(f"Remaining courts: {globals.prefCourtInfos}")


if __name__ == "__main__":
    session = requests.Session()
    testurl = "https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=3998000&item_id=4045681&time_date=2023-10-24&userType=1"
    res = session.get(testurl)
    availability_check(res.text)
