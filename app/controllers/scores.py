import datetime
import requests
import urllib


class SVC_Scores:
    def cmd_scores(phrase):
        try:
            sport_code = str(phrase)
            sport_code = sport_code.lower()
            url = "http://www.espn.com/" + sport_code + "/bottomline/scores"
            r = requests.get(url)
            espn_data = r.text
            espn_data_d = urllib.parse.unquote(espn_data)
            game_list = espn_data_d.split("left")
            body_text = "Scores for: " + sport_code.upper() + "[EOL]"
            body_text += (
                "Date: "
                + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                + "[EOL]"
            )
            for x in game_list:
                game_row = str(x)
                pos1 = game_row.find("=") + 1
                pos2 = game_row.find("&")
                game_row = game_row[pos1:pos2]
                body_text += game_row + "[EOL]"
        except:
            body_text = (
                "Apologies. We failed to retrieve the scores for "
                + sport_code
                + " . Please check the Sport Code and try again.[EOL]"
            )
            body_text += "At this time, valid Sport Codes are: NFL, NBA, MLB, NHL, NCF, RPM, WNBA"
        return body_text
