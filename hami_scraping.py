import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from funct import getTitle,getSubtitle,getmainID,processpara,contains_substr,getSeason
from googletrans import Translator
import imdb 
from googletrans import Translator
from tqdm import tqdm

top_url = ["https://hamivideo.hinet.net/%E5%BD%B1%E5%8A%87%E9%A4%A8/%E6%9C%80%E6%96%B0.do","https://hamivideo.hinet.net/%E5%BD%B1%E5%8A%87%E9%A4%A8/%E9%9B%BB%E5%BD%B1/%E6%8E%A8%E8%96%A6.do","https://hamivideo.hinet.net/%E5%BD%B1%E5%8A%87%E9%A4%A8/%E6%88%B2%E5%8A%87/%E6%8E%A8%E8%96%A6.do","https://hamivideo.hinet.net/%E5%BD%B1%E5%8A%87%E9%A4%A8/%E5%8B%95%E6%BC%AB/%E6%8E%A8%E8%96%A6.do","https://hamivideo.hinet.net/%E5%BD%B1%E5%8A%87%E9%A4%A8/%E5%85%92%E7%AB%A5/%E6%8E%A8%E8%96%A6.do","https://hamivideo.hinet.net/%E5%96%AE%E9%BB%9E%E9%9B%BB%E5%BD%B1/%E6%9C%80%E6%96%B0.do"]

prefix_url = "https://hamivideo.hinet.net"

episode_url_prefix = "https://hamivideo.hinet.net/play/"

imdb_prefix = "https://www.imdb.com/title/tt"

imdb_obj = imdb.IMDb()

section_type = ["Point Movie","Movie Theatre"]
jumble = []

for url in (top_url):
    get_data = requests.get(url = url)
    soup = BeautifulSoup(get_data.text, 'html.parser')

    data = soup.find_all("div", attrs={'class':"swiper-wrapper"})
    for i in data:
        for j in i.find_all("a", attrs={'class':"alink"},href=True):
            postfix = str(j["href"])
            if contains_substr(postfix) == False:
                jumble.append(prefix_url + postfix)
            else:
                continue
# print(len(jumble))
# jumble = jumble[0:220]
translator = Translator()


# ID's already read
movie_ID = {}
movie_title = []
# movie_title_translated = []
sub_title = []
movie_rating=[]
# movie_rating_translated = []
magnitude = []
year = []
origin = []
# origin_translated = []
level = []
# level_translated = []
genre = []
# genre_translated = []
language =[]
# language_translated = []
actors = []
directors = []
dateAdded = []
removalDate = []
# removalDate_translated = []
quality = []
# quality_translated = []
episodes = []
# episodes_translated = []
category = []
main_titleID =[]
defaultval = []
current_episode_link = []
episode_url = []
episode_title_id = []
imdb_id = []
vod = []
month_access = []
section = []
valid_links = []

for link in tqdm(jumble):
    if getmainID(link) in movie_ID.keys():
        # print("Present")
        continue
    try:
        get_url = requests.get(url = link)
        new_soup = BeautifulSoup(get_url.text, 'html.parser')
        # Now from here we can get info about the movie, populate arrays and finally convert to dataframe followed by writing to csv file
        defaultval.append("NA")
        movie_ID[getmainID(link)] = 1
        mdata = new_soup.find("div", attrs={'class':"title"})
        title = getTitle(mdata)
        movie_title.append(title)
        # print(translator.translate('My name is John',dest='fr').text)
        # print(translator.translate(str(title),dest='en').text)
        # movie_title_translated.append(translator.translate(title,dest='en').text)
        subtitle = getSubtitle(mdata)
        sub_title.append(subtitle)
        title_para = mdata.find("p")
        main_titleID.append(getmainID(link))
        title_para = processpara(title_para)
        section.append(section_type[int(link[-1])-1])
        details = ""

        if len(title_para.split()) == 5:
            category.append("Show")
            episodes.append((title_para.split())[1])
            # episodes_translated.append(translator.translate(str((title_para.split())[1]),dest='en').text)
            epidata = new_soup.find("ul", attrs={'class':"program_class_in"})
            curr_episode = epidata.find("li", attrs={'class':"active"})
            current_episode_link.append(curr_episode["data-sn"])
            gen_link = episode_url_prefix + str(getmainID(link)) + "/" + str(curr_episode["data-id"]) + ".do"
            episode_url.append(gen_link)
            episode_title_id.append(str(curr_episode["data-id"]))
            vod.append(str(curr_episode["data-id"]))
            # get season from title:
            # season_no = getSeason(translator.translate(title,dest='en').text)
            # print(season_no)    
        else:
            category.append("Movie")
            episodes.append("NA")
            # episodes_translated.append("NA")
            current_episode_link.append("NA")
            vod.append("Hami Video")
            episode_url.append("NA")
            episode_title_id.append("NA")
        for i in title_para:
            if i!="\r":
                details = details + i
            else:
                break
        details = list(details)
        information = []
        datacapt=""
        for i in details:
            if i!='．':
                datacapt = datacapt + str(i)
            else:
                information.append(datacapt)
                datacapt = ""
        information.append(datacapt)
        try:
            year.append(information[0])
        except:
            year.append("NA")
        try:
            origin.append(information[1])
            # origin_translated.append(translator.translate(str(information[1]),dest = 'en').text)
        except:
            origin.append("NA")
            # origin_translated.append("NA")
        try:
            level.append(information[2])
            # level_translated.append(translator.translate(str(information[2]),dest='en').text)
        except:
            level.append("NA")
            # level_translated.append("NA")
        try:
            search_mov = imdb_obj.search_movie(subtitle)
            imdb_id.append(search_mov[0].movieID)
        except:
            # print("Not found")
            imdb_id.append("NA")
        quality.append(title_para[-8:])
        # quality_translated.append(translator.translate(str(title_para[-8:]),dest='en').text)
        try:
            Rating = mdata.find("span",attrs={'class':"meataImdbRating"}).string
        except:
            Rating = "NA"
        movie_rating.append(Rating)
        # movie_rating_translated.append(translator.translate(str(Rating),dest='en').text)
        addData = new_soup.find("ul", attrs={'class':"list_detail"})
        try:
            Rating = addData.find("p",attrs={'class':"starRating"}).string
        except:
            Rating = "NA"
        magnitude.append(Rating)
        details = []
        for detail in addData.find_all("p"):
            details.append(detail.string)
        try:
            genre.append(details[0])
            # genre_translated.append(translator.translate(str(details[0]),dest = 'en').text)
        except:
            genre.append("NA")
            # genre_translated.append("NA")
        try:
            language.append(details[1])
            # language_translated.append(translator.translate(str(details[1]),dest = 'en').text)
        except:
            language.append("NA")
            # language_translated.append("NA")
        details = []
        for detail in addData.find_all("h3"):
            details.append(detail.string)
        removalDate.append(details[3])
        # removalDate_translated.append(translator.translate(str(details[3]),dest='en').text)
        dateAdded.append(datetime.datetime.today().strftime('%Y-%m-%d'))
        month_access.append(datetime.datetime.now().strftime('%B'))
        valid_links.append(link)
        if len(dateAdded)%20 == 0:
            # print("Milestone "+ str(len(dateAdded)/20)+" of "+ str(int(len(jumble)/20)))
            pass
        # details = []
        # actdir = []
        # addData = new_soup.find_all("ul", attrs={'class':"list_detail"})
        # for detail in addData:
        #     list_data = detail.find_all("li")
        #     details = []
        #     for linkref in list_data:
        #         cast_data = linkref.find_all("a")
        #         for s in cast_data:
        #             details.append(str(s.string))
        #     actdir.append(details)
        # actors.append(actdir[1])
        # directors.append(actdir[2])
    except:
        # print("Passed")
        pass
# IMDB Queries
imdb_url_full = []
imdb_info =[]
for post in imdb_id:
    try:
        imlink = imdb_prefix + str(post) + "/"
        im_url = requests.get(url = imlink)
        imdb_soup = BeautifulSoup(im_url.text, 'html.parser')
        title_bar = imdb_soup.find("div", attrs={'class':"title_bar_wrapper"})
        information = []
        for inf in title_bar.find_all("a", href=True):
            information.append(inf.string)
        imdb_info.append(information)
        imdb_url_full.append(imlink)
    except :
        print("Nope")
        imdb_url_full.append("NA")
# Movie_List = [movie_title,sub_title,category,defaultval,defaultval,current_episode_link,year,defaultval,defaultval,genre,language,origin,level,defaultval,defaultval,jumble,main_titleID,episode_url,episode_title_id,section,month_access,vod,defaultval,defaultval,dateAdded,removalDate,movie_rating,magnitude,episodes,quality,imdb_id,imdb_url_full,movie_title_translated,genre_translated,language_translated,origin_translated,level_translated,removalDate_translated,movie_rating_translated,episodes_translated,quality_translated]
Movie_List = [movie_title,sub_title,category,defaultval,defaultval,current_episode_link,year,defaultval,defaultval,genre,language,origin,level,defaultval,defaultval,valid_links,main_titleID,episode_url,episode_title_id,section,month_access,vod,defaultval,defaultval,dateAdded,removalDate,movie_rating,magnitude,episodes,quality,imdb_id,imdb_url_full]
df = pd.DataFrame(Movie_List).transpose()
# df.columns = ['Title','Sub-Title','Category','Max Season','Season No','Episode No','Release Year','Sub-Genre','Master Genre','Type','Original Language (Pronounce)','Country Origin','Runtime','Production Company','Network','Link','Main Title ID','Episode Title URL','Episode Title ID','Section','Month','VOD','Original','Country','Date Added','Removal Date','IMDb Rating','Magnitude','Episodes','Quality','IMDb ID','IMDb URL','Title Translated','Type Translated','Original Language Translated','Country Origin Translated','Runtime Translated','Removal Date Translated','IMDb Rating Translated','Episodes Translated','Quality Translated']
df.columns = ['Title','Sub-Title','Category','Max Season','Season No','Episode No','Release Year','Sub-Genre','Master Genre','Type','Original Language (Pronounce)','Country Origin','Runtime','Production Company','Network','Link','Main Title ID','Episode Title URL','Episode Title ID','Section','Month','VOD','Original','Country','Date Added','Removal Date','IMDb Rating','Magnitude','Episodes','Quality','IMDb ID','IMDb URL']

df = df.astype(str)
df.drop_duplicates(subset=['Title'],keep = 'last')
print(df.head())
df.to_csv("output.csv")