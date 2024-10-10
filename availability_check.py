# import datetime
import re
import requests
from typing import Dict, List, Tuple

import globals
from utils import log


def search_reserved(text: str):
    total_reserved = re.findall(
        "(?<=markResStatus\('\d{8}',')(.*?)(?=',')", text
    )
    return total_reserved


def search_total(text: str):
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


def get_available_courts(text: str) -> Tuple[Dict, List[int]]:
    reserved_ids = search_reserved(text)
    (
        total_court_ids,
        all_time_sessions,
        total_field_names,
        total_costs,
        total_tokens,
    ) = search_total(text)
    all_data = {}
    all_time_sessions = list(all_data.fromkeys(all_time_sessions))
    count = 0
    for time_sessions in range(len(all_time_sessions)):
        if (
            int(len(total_field_names) / len(all_time_sessions))
            == int(len(total_court_ids) / len(all_time_sessions))
            == int(len(total_costs) / len(all_time_sessions))
        ):
            avg = int(len(total_court_ids) / len(all_time_sessions))
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
        all_data[all_time_sessions[time_sessions]] = item_time_sessions

    all_court_ids = []
    prefs = list(all_data.keys())
    prefs.reverse()

    for key0, value in all_data.items():
        for key1 in value.items():
            all_court_ids.append(key1[1]["Court ID"])

    available_ids = [x for x in all_court_ids if x not in reserved_ids]

    return all_data, available_ids


def availability_update():
    session = requests.Session()
    res = session.get(globals.view_book_url)
    _, new_available_court_ids = get_available_courts(res.text)
    # new_available_court_ids.reverse()

    valid_indices = [
        globals.target_court_ids.index(x)
        for x in new_available_court_ids
        if x in globals.target_court_ids
    ]

    globals.target_court_ids = [globals.target_court_ids[i] for i in valid_indices]
    globals.target_court_costs = [globals.target_court_costs[i] for i in valid_indices]
    globals.target_court_tokens = [globals.target_court_tokens[i] for i in valid_indices]
    globals.target_court_infos = [globals.target_court_infos[i] for i in valid_indices]
    log(f"Remaining courts: {globals.target_court_infos}")


if __name__ == "__main__":
    session = requests.Session()
    testurl = "https://50.tsinghua.edu.cn/gymsite/cacheAction.do?ms=viewBook&gymnasium_id=3998000&item_id=4045681&time_date=2023-10-24&userType=1"
    res = session.get(testurl)
    get_available_courts(res.text)
