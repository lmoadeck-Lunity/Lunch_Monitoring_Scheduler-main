import datetime
import calendar
from dateutil.rrule import *

from dateutil.parser import *
import csv

from datetime import *
import itertools
parserinfo_ = parserinfo(dayfirst=True)

def parse_date(date_str):
    if '-' in date_str:
        start, end = date_str.split('-')
        st_day, st_month = map(int, start.split('/'))
        en_day, en_month = map(int, end.split('/'))
        print(st_day, st_month, en_day, en_month)
        datetime_start = date(2024, st_month, st_day)
        datetime_end = date(2024, en_month, en_day)
        return list(rrule(freq=DAILY, until=datetime_end, dtstart=datetime_start))
    else:
        return parse(date_str,parserinfo=parserinfo_)
calendar_ = calendar.Calendar()
holidays = '18/9,27/9,1/10,4/10,11/10,16/10-24/10,4/11,19/11,20/11,2/12,20/12,22/12,2/1,6/1,20/1,27/1-5/2,19/3,4/4-24/4,1/5,5/5,13/5,26/5,5/6,23/6,1/7,2/7-31/8'.split(',')
holidays = [parse_date(x) for x in holidays]
holidays = list(itertools.chain([a for x in holidays if isinstance(x, list) for a in x], [x for x in holidays if not isinstance(x, list)]))
print(holidays)
# rule1 = rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TU, dtstart=datetime(2024, 9, 1))
# rule2_A = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 6))
# rule2_B = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 13))
# rule2_C = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 20))
# rule2_D = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 27))
ruleset_5A = rruleset(cache=True)
ruleset_5A.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=MO, dtstart=datetime(2024, 9, 1)))
ruleset_5A.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 6)))
[ruleset_5A.exdate(i) for i in holidays]
ruleset_5B = rruleset(True)
ruleset_5B.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TU, dtstart=datetime(2024, 9, 1)))
ruleset_5B.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 13)))
[ruleset_5B.exdate(i) for i in holidays]
ruleset_5C = rruleset(True)
ruleset_5C.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=WE, dtstart=datetime(2024, 9, 1)))
ruleset_5C.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 20)))
[ruleset_5C.exdate(i) for i in holidays]
ruleset_5D = rruleset(True)
ruleset_5D.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TH, dtstart=datetime(2024, 9, 1)))
ruleset_5D.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 27)))
[ruleset_5D.exdate(i) for i in holidays]
print(len(list(ruleset_5A)), len(list(ruleset_5B)), len(list(ruleset_5C)), len(list(ruleset_5D)))
for i in range(4):
    csv_file = open(f'5{chr(65+i)}.csv', 'w',newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Date'])
    for date in list(ruleset_5A) if i == 0 else list(ruleset_5B) if i == 1 else list(ruleset_5C) if i == 2 else list(ruleset_5D):
        csv_writer.writerow([date.strftime('%d/%m/%Y')])
    csv_file.close()
