import requests
import datetime
import json
import time
import os

URL=f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=266&date={"-".join(str(datetime.date.today()).split("-")[::-1])}'
ALERT_URL = os.environ.get("WEB_HOOK_URL")


header={
    "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

def loop():
    resp=requests.get(URL, headers=header)
    if resp.status_code==200:
        centers=json.loads(resp.text)["centers"]
        centers=list(filter(lambda x: x["block_name"]=="Mysore", centers))
        for center in centers:
            center["sessions"]=list(filter(lambda x: x["min_age_limit"]<=45 and x["available_capacity"]>0,center["sessions"]))
        centers=list(filter(lambda x: x["sessions"],centers))

        if centers:
            print("\n\n\n===========Slots==========\n\n\n")
            print(centers)
            centers=list(map(lambda x: x["name"],centers))
            data=f"Vaccination slots available in {', '.join(centers)}."
            print("\n\n\n===========Centers==========\n\n\n")
            print(data)
            print("\n========================\n")
            return data

    return None

if __name__=="__main__":
    print("\nMonitoring slots every 15 seconds\n")
    while(True):
        data=loop()
        if data:
            requests.post(ALERT_URL, data={"value1":data})
            time.sleep(60)
        else:
            print("No Slots available")
            time.sleep(15)