from datetime import datetime

def diffTime(start, end):
    return (datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.%fZ')).total_seconds()
