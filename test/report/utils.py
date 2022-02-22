from datetime import timedelta

from base.utils.time import convert_str2datetime


async def __make_report_data(date="2022-02-07 00:00:00", categories=('SELF', 'MIRACLE', 'DAILY')):
    data = {
        "routines": [
            {
                "title": "글5",
                "category": categories[0],
                "id": 6,
                "account_id": 1
            }, {
                "title": "글6",
                "category": categories[0],
                "id": 7,
                "account_id": 1
            }, {
                "title": "글7",
                "category": categories[1],
                "id": 8,
                "account_id": 1
            }, {
                "title": "글8",
                "category": categories[1],
                "id": 9,
                "account_id": 1
            }, {
                "title": "글9",
                "category": categories[2],
                "id": 10,
                "account_id": 1
            }, {
                "title": "글10",
                "category": categories[2],
                "id": 11,
                "account_id": 1
            }, {
                "title": "글11",
                "category": categories[0],
                "id": 12,
                "account_id": 1
            }, {
                "title": "글12",
                "category": categories[0],
                "id": 13,
                "account_id": 1
            }

        ],
        "routine_results": [
            {
                "routine_id": 6,
                "date": date,
                "result": "DONE"
            }, {
                "routine_id": 7,
                "date": date,
                "result": "DONE"
            }, {
                "routine_id": 8,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 9,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 10,
                "date": date,
                "result": "NOT"
            }, {
                "routine_id": 11,
                "date": str(convert_str2datetime(date) + timedelta(days=2)),
                "result": "DONE"
            }, {
                "routine_id": 12,
                "date": str(convert_str2datetime(date) + timedelta(days=2)),
                "result": "DONE"
            }, {
                "routine_id": 13,
                "date": str(convert_str2datetime(date) + timedelta(days=5)),
                "result": "DONE"
            }
        ]
    }

    return data
