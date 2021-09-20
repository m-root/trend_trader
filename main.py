import time
from datetime import datetime
from payload import payload
import settings
currentTime = datetime.utcnow().strftime("%M")

# while int(datetime.utcnow().strftime("%M")) %15 != 0:
#     print("{} Minutes : {} Seconds to go".format(14-(int(datetime.utcnow().strftime("%M"))%15),(60 - int(datetime.utcnow().strftime("%S")))))
#     time.sleep(1)main.py


pairs = settings.pairs
def main():
    # for pair in pairs:
    #     payload.Payload(pair=pair[0], set_range=pair[1]).logic()
    #     time.sleep(1)
    while True:
        try:
            for pair in pairs:
                payload.Payload(pair=pair[0], set_range=pair[1]).logic()
                time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(15)

        while float(datetime.utcnow().strftime("%M.%S")) % 15 != 0:
            print("{} Minutes : {} Seconds to go".format(14 - (int(datetime.utcnow().strftime("%M")) % 15),
                                                         (60 - int(datetime.utcnow().strftime("%S")))))
            time.sleep(1)

if __name__ == '__main__':
    main()
