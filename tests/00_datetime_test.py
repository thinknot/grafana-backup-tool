import datetime as dt
import time

def test_helloworld():
    print('Hello jello')

def floor_dt(dt_exact):
    dt_minute = dt_exact - dt.timedelta(seconds=dt_exact.second,
                                        microseconds=dt_exact.microsecond)
    return dt_minute

def test_datetime_random_failing():
    dt_now_local1 = dt.datetime.now()
    dt_now_utc1 = dt.datetime.utcnow()
    unix_now = time.time()
    dt_now_utc2 = dt.datetime.now(dt.timezone.utc)

    ts_now1 = dt_now_utc2.timestamp()
    ts_now2 = dt_now_utc2.timestamp()
    print('timestamp1 now: {}'.format(ts_now1))
    print('timestamp2 now: {}'.format(ts_now2))
    print('time now: {}'.format(unix_now))
    assert ts_now2 == ts_now1
    assert int(ts_now1) == int(unix_now)

    dt_check = dt.datetime.fromtimestamp(unix_now, dt.timezone.utc)
    print('datetime now check: {}'.format(dt_check))

    ts_then = ts_now1 - 180  # 180 seconds ago
    dt_then = dt.datetime.fromtimestamp(ts_then, dt.timezone.utc)
    then_floor = floor_dt(dt_then)
    now_floor = floor_dt(dt_now_utc2)
    print('now floor: {}'.format(now_floor))
    print('timestamp 3 minutes ago: {}'.format(ts_then))
    print('datetime 3 minutes ago: {}'.format(dt_then))
    print('3 minutes ago floor: {}'.format(then_floor))
    dt_check = dt_check.replace(microsecond=0)
    dt_now_utc2 = dt_now_utc2.replace(microsecond=0)
    assert dt_check == dt_now_utc2
