# Estazione e raccolta dei dati relativi ai generi contenuti in urls.
# Vengono raccolti tutti gli attributi delle canzoni per ogni genere e successivamente salvati in data.txt


from bs4 import BeautifulSoup
import requests
import time
import json

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en_EN; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}

#Lista dei generi di partenza di AllMusic
urls = ["https://www.allmusic.com/genre/avant-garde-ma0000012170/songs",
        "https://www.allmusic.com/genre/blues-ma0000002467/songs",
        "https://www.allmusic.com/genre/childrens-ma0000002944/songs",
        "https://www.allmusic.com/genre/classical-ma0000002521/songs",
        "https://www.allmusic.com/genre/comedy-spoken-ma0000004433/songs",
        "https://www.allmusic.com/genre/country-ma0000002532/songs",
        "https://www.allmusic.com/genre/easy-listening-ma0000002567/songs",
        "https://www.allmusic.com/genre/electronic-ma0000002572/songs",
        "https://www.allmusic.com/genre/folk-ma0000002592/songs",
        "https://www.allmusic.com/genre/holiday-ma0000012075/songs",
        "https://www.allmusic.com/genre/international-ma0000002660/songs",
        "https://www.allmusic.com/genre/jazz-ma0000002674/songs",
        "https://www.allmusic.com/genre/latin-ma0000002692/songs",
        "https://www.allmusic.com/genre/new-age-ma0000002745/songs",
        "https://www.allmusic.com/genre/pop-rock-ma0000002613/songs",
        "https://www.allmusic.com/genre/r-b-ma0000002809/songs",
        "https://www.allmusic.com/genre/rap-ma0000002816/songs",
        "https://www.allmusic.com/genre/reggae-ma0000002820/songs",
        "https://www.allmusic.com/genre/religious-ma0000004431/songs",
        "https://www.allmusic.com/genre/stage-screen-ma0000004432/songs",
        "https://www.allmusic.com/genre/vocal-ma0000011877/songs"]

data = {}
data["songs"] = []
for url in urls:
    print(url)
    req = requests.get(url, headers=user_agent, verify=True, allow_redirects=True, timeout=10)

    soup = BeautifulSoup(req.text, "html.parser")

    section = soup.find("section", {'class': 'song-highlights'})

    titles = section.find_all("td", {'class': 'title'})
    performers = section.find_all("td", {'class': 'performer'})
    genre = url.split("/")[4]

    # print(titles)
    # print(performers)

    for i in range(len(titles)):

        time.sleep(1)
        title = titles[i]
        performer = performers[i]

        url2 = title.find("a").get("href") + "/attributes"
        req = requests.get(url2, headers=user_agent, verify=True, allow_redirects=True, timeout=10)
        soup = BeautifulSoup(req.text, "html.parser")

        section2 = soup.find("section", {'class': 'attributes'})
        attributes = []

        try:
            attributes_tab_styles = section2.find("div", {'class': 'attribute-tab-styles'})
            attributes_tab_styles_list = attributes_tab_styles.find_all("a")
            for i in range(len(attributes_tab_styles_list)):
                if attributes_tab_styles_list[i].text != "Would you like to contribute?":
                    attributes.append(attributes_tab_styles_list[i].text)
        except:
            pass

        try:
            attributes_tab_moods = section2.find("div", {'class': 'attribute-tab-moods'})
            attributes_tab_moods_list = attributes_tab_moods.find_all("a")
            for i in range(len(attributes_tab_moods_list)):
                if attributes_tab_moods_list[i].text != "Would you like to contribute?":
                    if 'Playful' in str(attributes_tab_moods_list[i].text):
                        attributes.append('Playful_mood (' + str(attributes_tab_moods_list[i].text).split('(')[1])
                    else:
                        attributes.append(attributes_tab_moods_list[i].text)
        except:
            pass

        try:
            attributes_tab_themes = section2.find("div", {'class': 'attribute-tab-themes'})
            attributes_tab_themes_list = attributes_tab_themes.find_all("a")
            for i in range(len(attributes_tab_themes_list)):
                if attributes_tab_themes_list[i].text != "Would you like to contribute?":
                    attributes.append(attributes_tab_themes_list[i].text)
        except:
            pass

        if len(attributes) > 0:
            data["songs"].append({
                "title": str(title.find("a").text).strip(),
                "performer": str(performer.text).strip(),
                "genre": genre,
                "attributes": attributes
            })

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)

    # s = Song(str(title.find("a").text), str(performer.text).strip(), genres, styles, moods, themes)
    # print(s.__str__())
    # s.toPercent()
