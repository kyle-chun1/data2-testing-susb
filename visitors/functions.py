

from datetime import datetime
import pytz
#  CONVERTS ANY DATETIME OBJCECT TO US/EASTERN TIME
def useastern(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern'))
    return any_timestamp.astimezone(pytz.timezone('US/Eastern'))

def useastern_start(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern')).replace(hour=0,minute=0,second=0,microsecond=0)
    return any_timestamp.astimezone(pytz.timezone('US/Eastern')).replace(hour=0,minute=0,second=0,microsecond=0)

def useastern_end(any_timestamp=''):
    if any_timestamp == '' :
        return datetime.now().astimezone(pytz.timezone('US/Eastern')).replace(hour=23,minute=59,second=59,microsecond=999999)
    return any_timestamp.astimezone(pytz.timezone('US/Eastern')).replace(hour=23,minute=59,second=59,microsecond=999999)
