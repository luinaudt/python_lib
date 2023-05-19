import feedparser
import time
from urllib.request import urlretrieve as wget
from pathlib import Path

# utility script to download podcast from france inter c'est à vous
# should work for other podacsts

url = "https://radiofrance-podcast.net/podcast09/rss_18153.xml"
feed = feedparser.parse("rss_18153.xml")

def extract_mp3_link(links):
    for i in links:
        if "rel" in i and i["rel"] == 'enclosure':
            if "href" in i:
                return i["href"]

def extract_url(links):
    for i in links:
        if "rel" in i and i["rel"] == 'alternate':
            if "href" in i:
                return i["href"]

def create_summary(info):
    summary = f'{info["title"]}\n{info["link"]}\n'
    summary += f'{info["summary"]}\n'
    return summary

def download_link(info, base_folder: Path):
    date : time.struct_time = info['published_parsed']
    links = info['links']
    print(f"duree: {info['itunes_duration']}")
    print(f"resume: {create_summary(info)}")
    podcast_name = extract_url(links).split('/')[-2]
    folder=Path(base_folder, podcast_name)
    if not folder.exists():
        folder.mkdir()
    filename=f"{date.tm_year}-{date.tm_mon}-{date.tm_mday}_{info['id']}"
    file = Path(folder, f"{filename}.mp3")
    if not file.exists():
        wget(extract_mp3_link(links), str(Path(folder, filename)))
        with open(Path(folder, "summary.txt"), "a") as f:
            f.write("-"*30 + "\n")
            f.write("fichier :" + filename + ":\n")
            f.write(f"date : {date.tm_year}-{date.tm_mon}-{date.tm_mday}\n")
            f.write(create_summary(info))

base_folder=Path(Path.home(), "Musique/podcast/franceinter")
if not base_folder.exists():
    base_folder.mkdir(parents=True)
for i in feed["entries"][:-1]:
    if "links" in i:
        download_link(i, base_folder)
    