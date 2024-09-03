import datetime
import calendar
import dateutil
classes_to_schedule = 8
groups = list(range(1, 14)) # not fast, but able to handle plugging in different groups
def parse_date(date_str):
    if '-' in date_str:
        start, end = date_str.split('-')
        st_day, st_month = map(int, start.split('/'))
        en_day, en_month = map(int, end.split('/'))
        return list(map(int, start.split('/'))), list(map(int, end.split('/')))
    else:
        return tuple(map(int, date_str.split('/')))
calendar_ = calendar.Calendar()
holidays = '18/9,27/9,1/10,4/10,11/10,16/10-24/10,4/11,19/11,20/11,2/12,20/12,22/12,2/1,6/1,20/1,27/1-5/2,19/3,7/27-24/4,1/5,5/5,13/5,26/5,5/6,23/6,1/7,2/2-31/8'.split(',')
holidays = [parse_date(x) for x in holidays]
