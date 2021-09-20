import time
from datetime import datetime
import payload.payload_tests as payload
currentTime = datetime.utcnow().strftime("%M")

# while int(datetime.utcnow().strftime("%M")) %15 != 0:
#     print("{} Minutes : {} Seconds to go".format(14-(int(datetime.utcnow().strftime("%M"))%15),(60 - int(datetime.utcnow().strftime("%S")))))
#     time.sleep(1)main.py


def main():
    while True:
        try:
            logic = payload.Payload(pair='LTCBTC', period='15m', limit=0, quantity=0)
            logic.buy_entry_logic()
            logic.buy_exit_logic()
            logic.sell_entry_logic()
            logic.sell_exit_logic()

        except Exception as e:
            print(e)
            time.sleep(15)

        while float(datetime.utcnow().strftime("%M.%S")) % 15 != 0:
            print("{} Minutes : {} Seconds to go".format(14 - (int(datetime.utcnow().strftime("%M")) % 15),
                                                         (60 - int(datetime.utcnow().strftime("%S")))))
            time.sleep(1)

if __name__ == '__main__':
    main()
