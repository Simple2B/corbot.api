import requests
import bs4 as BeautifulSoup


class SVC_MusicMap:
    def cmd_musicmap(arg):
        query = str(arg)
        query = query.replace(" ", "+")
        query = query.replace(" ", "+")
        query = query.replace(" ", "+")
        query = query.replace("-", "-2d")
        main_url = "https://www.music-map.com/"
        combine = main_url + query + ".html"
        r = requests.get(combine)
        soup = BeautifulSoup.BeautifulSoup(r.text, "lxml")
        artist_text = "Below is a list of artist similar in popularity to the one you selected: \r\n"
        cnt = 0
        for artists in soup.find_all("a"):
            if cnt > 1:
                artist_text += artists.text + " | "
            cnt += 1
        if cnt < 4:
            artist_text = "Apologies: no similar artist have been found for the artist name you selected, please check the spelling."
        print(cnt)
        return artist_text
