from flask import Flask,jsonify
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

data =[]
@app.route('/')
def hello_world():  # put application's code here
    url = "https://www.airbnb.fr/?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&search_mode=flex_destinations_search&flexible_trip_lengths%5B%5D=one_week&location_search=MIN_MAP_BOUNDS&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&category_tag=Tag%3A8536&search_type=category_change"
    response = requests.get(url)
    clearing = ["Professionnel,  · Professionnel", 'Particulier,  · Particulier', ' Particulier']
    title = "listing-card-title"
    subtitle = "listing-card-subtitle"
    price = "price-availability-row"

    def splitter_sub(lis, tag):
        subs = []
        for i in lis:
            for index, j in enumerate(i):
                if index % 2 == 0 and index!=6:
                    at = j.get_text()
                    for el in clearing:
                        at.replace(el, '')
                    print(tag, at)
                    if at!=' · ':
                       subs.append(at)
        item[tag]=subs

    rating = 'r4a59j5 atm_h_1h6ojuz atm_9s_1txwivl atm_7l_jt7fhx atm_84_evh4rp atm_mk_h2mmj6 atm_mj_glywfm dir dir-ltr'
    soup = BeautifulSoup(response.text, 'html.parser')
    t = soup.find_all('div', {"data-testid": title})
    s = soup.find_all('div', {"data-testid": subtitle})
    s = list(zip(s[::2], s[1::2]))
    p = soup.find_all('div', {"data-testid": price})

    r = soup.find_all('span', {'class': rating})

    for i in range(0, len(t)):
        item = {}
        print("Title : ", t[i].get_text())
        item["Title"]= t[i].get_text()
        for sub in s[i]:
            splitter_sub(sub, "Subtitle : ")
        new_price = p[i].get_text().split('p')
        print("Price : ", new_price[0])
        item["Price "]= new_price[0]
        # splitter_sub(p[i],"Price : ")
        try:
            rate = r[i].get_text()
            if 'Nouvel' in rate:
                rate = 'No rating'
            elif 'sur' in rate:
                rate = rate[20:25]
            print("Rating: ", rate, " stars")
            item["Rating"]= rate
        except IndexError:
            print("Rating : No more rating it's enough")
            item["Rating"]= False
        print("")
        print("")
        data.append(item)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
