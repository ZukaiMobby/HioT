from datetime import datetime

x = datetime.timestamp(datetime.now())



print(datetime.fromtimestamp(x))
print(datetime.fromtimestamp(x+10-datetime.now()))