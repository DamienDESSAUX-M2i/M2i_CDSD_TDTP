from datetime import datetime

def quelle_heure(heure: str="12h00") -> None:
    print(heure)

quelle_heure()
my_time: datetime = datetime.now()
quelle_heure(f"{my_time.hour}H{my_time.minute}")