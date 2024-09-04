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
        # print(st_day, st_month, en_day, en_month)
        datetime_start = date(2024, st_month, st_day) if st_month > 6 else date(2025, st_month, st_day)
        datetime_end = date(2024, en_month, en_day) if en_month > 6 else date(2025, en_month, en_day)
        return list(rrule(freq=DAILY, until=datetime_end, dtstart=datetime_start))
    else:
        return parse(date_str,parserinfo=parserinfo_)
calendar_ = calendar.Calendar()
holidays = '18/9,27/9,1/10,4/10,11/10,16/10-24/10,4/11,19/11,20/11,2/12,20/12,22/12-2/1,6/1,20/1,27/1-5/2,19/3,4/4-24/4,1/5,5/5,13/5,26/5,5/6,23/6'.split(',')
holidays = [parse_date(x) for x in holidays]
holidays = list(itertools.chain([a for x in holidays if isinstance(x, list) for a in x], [x for x in holidays if not isinstance(x, list)]))
# print(holidays)
A = []
B = []
C = []
D = []
count = 0
dates_range = list(rrule(freq=DAILY, until=datetime(2025, 6, 30), dtstart=datetime(2024, 9, 4)))
dates_range = [x for x in dates_range if x.weekday() < 5 and x not in holidays]
for date in dates_range:
    if date.weekday() == 0:
        A.append(date)
    elif date.weekday() == 1:
        B.append(date)
    elif date.weekday() == 2:
        C.append(date)
    elif date.weekday() == 3:
        D.append(date)
    elif date.weekday() == 4:
        if count % 4 == 0:
            A.append(date)
        elif count % 4 == 1:
            B.append(date)
        elif count % 4 == 2:
            C.append(date)
        elif count % 4 == 3:
            D.append(date)
        count += 1
print(A, B, C, D)
# rule1 = rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TU, dtstart=datetime(2024, 9, 1))
# rule2_A = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 6))
# rule2_B = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 13))
# rule2_C = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 20))
# rule2_D = rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 27))
# ruleset_5A = rruleset(cache=True)
# ruleset_5A.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=MO, dtstart=datetime(2024, 9, 4)))
# ruleset_5A.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 6)))
# [ruleset_5A.exdate(i) for i in holidays]
# ruleset_5B = rruleset(cache=True)
# ruleset_5B.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TU, dtstart=datetime(2024, 9, 4)))
# ruleset_5B.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 13)))
# [ruleset_5B.exdate(i) for i in holidays]
# ruleset_5C = rruleset(cache=True)
# ruleset_5C.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=WE, dtstart=datetime(2024, 9, 4)))
# ruleset_5C.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 20)))
# [ruleset_5C.exdate(i) for i in holidays]
# ruleset_5D = rruleset(cache=True)
# ruleset_5D.rrule(rrule(freq=WEEKLY, until=datetime(2025, 6, 30), byweekday=TH, dtstart=datetime(2024, 9, 4)))
# ruleset_5D.rrule(rrule(freq=WEEKLY,interval=3, until=datetime(2025, 6, 30), byweekday=FR, dtstart=datetime(2024, 9, 27)))
# [ruleset_5D.exdate(i) for i in holidays]
# print(len(list(ruleset_5A)), len(list(ruleset_5B)), len(list(ruleset_5C)), len(list(ruleset_5D)))
temparray = []
count = 0
for i in range(4):
    csv_file = open(f'5{chr(65+i)}.csv', 'w',newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Date','Groups'])

    for date in list(A) if i == 0 else list(B) if i == 1 else list(C) if i == 2 else list(D):
        while len(temparray) < 8:
            temparray.append((count%15+1) if i == 0 else (count%14+1) if i == 1 else (count%14+1) if i == 2 else (count%11+1))
            count +=1
        csv_writer.writerow([date.strftime('%d/%m/%Y'), temparray])
        temparray = []
    csv_file.close()

# csv_file = open('output.csv', 'w',newline='')
# csv_writer = csv.writer(csv_file)
# csv_writer.writerow(['5A', '5B', '5C', '5D'])
# csv_writer.writerows([[date.strftime('%d/%m/%Y') for date in list(A)], [date.strftime('%d/%m/%Y') for date in list(B)], [date.strftime('%d/%m/%Y') for date in list(C)], [date.strftime('%d/%m/%Y') for date in list(D)]])