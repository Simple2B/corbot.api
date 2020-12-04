import lyricwikia


class SVC_Lyrics:
    def cmd_lyrics(arg):
        search_phrase = str(arg)
        try:
            full_input = search_phrase.lower()
            full_input = full_input.split(",")
            artist_input = full_input[0]
            song_input = full_input[1]
            lyrics = lyricwikia.get_lyrics(artist_input, song_input)
            text_data = lyrics
        except Exception as E:
            text_data = (
                "Lyric search failed, please check the spelling of the artist and song title. Please note, "
                "there are millions of songs and artist in the database, your query has to be exactly right to "
                "retrieve the lyrics."
            )
            text_data += "Your body of the message should look like one of the following examples: \r"
            text_data += "Ariana Grande, Imagine \r"
            text_data += "Lady Gaga, Shallow \r"
            text_data += "Mariah Carey, All I want for Christmas is Your \r"
            text_data += "Chainsmokers, Hope \r"
            text_data += "Error: " + str(E)
        return text_data
