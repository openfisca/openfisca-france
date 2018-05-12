#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Use weekalendar to generate holidays."""


from collections import OrderedDict
from workalendar.europe import France


holidays = []
for year in range(1990, 2020):
    holidays += France().get_calendar_holidays(year)


header = """#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


holidays = ["""

footer = """
    ]
"""

with open("../assets/holidays.py", "w") as text_file:
    text_file.write(header)
    for holiday_date, holiday_name in OrderedDict(holidays).items():
        text_file.write("""
    datetime.strptime("{}", "%Y-%m-%d").date(), # {}""".format(holiday_date, holiday_name))

    text_file.write(footer)
