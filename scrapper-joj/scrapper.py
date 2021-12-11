from pip._vendor import requests
from bs4 import BeautifulSoup
import os
import re 
import shutil

media_dir='\\\\nas.lan\\wd4\\Serialy\\'

#open from web
#url = 'https://videoportal.joj.sk/mafstory?seasonId=22'
#r = requests.get(url)
#soup = BeautifulSoup(r.content, 'html.parser')

#open from local file
html_file = 'Mafstory _ Relácie A-Z _ Videoportál - najlepšie seriály a relácie TV JOJ.html' #'https://videoportal.joj.sk/mafstory?seasonId=274'
soup = BeautifulSoup(open(html_file, encoding="utf8"), 'html.parser')

#get season info and create season directory
show = soup.find_all("h2", class_="title")[0].text.strip()
show_dir = media_dir + show + "\\"
season = re.findall('[0-9]+', soup.find_all("div", class_="e-select")[0].find_all("select")[0].find_all("option", selected=True)[0].text)[0]
season_dir=show_dir + "Season " + season + "\\"
if not os.path.isdir(season_dir): 
    print("Create season directory")
    os.mkdir(season_dir)

if not os.path.isdir(season_dir + "\\yt_files"): 
    os.mkdir(season_dir + "\\yt_files")

if os.path.isfile(html_file):
    original = html_file
    target = season_dir + "\\yt_files\\" + html_file
    if not os.path.isfile(target):
        print("Copy " + original + "to season directory")
        shutil.copy(original, target)
    if not os.path.isdir(target.replace(".html", "") + "_files"):
        print("Copy " + original.replace(".html", "") + "_files" + " to season directory")
        shutil.copytree(original.replace(".html", "") + "_files", target.replace(".html", "") + "_files")

file=open(season_dir + "\\yt_files\\download.ps1", "w", encoding="utf8")

videos = soup.find_all("div", class_="col-12 col-sm-6 col-lg-3")
for video in videos:
    link = video.find_all('a', href=True)
    air_date = link[0].find_all("span", class_="date")[0].text
    episode = re.findall('[0-9]+', link[0].find_all("span", class_="date")[1].text)[0]
    print("& C:/Users/empee4/AppData/Local/Microsoft/WindowsApps/python3.9.exe c:/Users/empee4/Devel/youtube-dl-1/youtube_dl/__main__.py -f best " + link[0].attrs["href"] + ' -o \"' + season_dir + 'S' + season.rjust(2,"0") + 'E' + episode.rjust(2,"0") + ' - ' + link[0].attrs["title"] + " (" + air_date + ").mp4\"")
    file.write("& C:/Users/empee4/AppData/Local/Microsoft/WindowsApps/python3.9.exe c:/Users/empee4/Devel/youtube-dl-1/youtube_dl/__main__.py -f best " + link[0].attrs["href"] + ' -o \"' + season_dir + 'S' + season.rjust(2,"0") + 'E' + episode.rjust(2,"0") + ' - ' + link[0].attrs["title"] + " (" + air_date + ").mp4\"\n")

file.flush()
file.close()
