from bs4 import BeautifulSoup
import requests
import sys
import re

listurl = 'https://letterboxd.com/ivan0716/list/2021-ranked/'

get_rating = True

if len(sys.argv) == 2:
    listurl = ''+sys.argv[1]+''

list_page = 1
rank = 1

# iterate through list pages
while list_page < 100:
    webpage = requests.get(listurl + 'detail/page/' + str(list_page) + '/')
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # find all films in list
    films = soup.find_all(attrs={"data-target-link":True})

    if get_rating:
        ratings = soup.find_all(class_=re.compile("rating rated.*"))

    rating_idx = 0

    # break if no films found on current page
    if not films:
        break

    # generate url
    for film in (films):
        # get lb url
        lb_url = 'https://letterboxd.com' + film['data-target-link']
        webpage = requests.get(lb_url)
        soup = BeautifulSoup(webpage.content, 'html.parser')

        film_info = soup.find(class_="film-header-lockup -default")

        #print(film_info)

        title = list(film_info.children)[1].get_text()
        year = film_info.find('a').get_text()
        aka = film_info.find('em')
        dir = film_info.find('span').get_text()

        if get_rating:
            if aka is not None:
                print(str(rank)+'. '+title+' ['+aka.get_text().replace('’', '').replace('‘', '')+'] ('+year+', '+dir+')  '+str(ratings[rating_idx].get_text()))
            else:
                print(str(rank)+'. '+title+' ('+year+', '+dir+')  '+str(ratings[rating_idx].get_text()))
        else:
            if aka is not None:
                print(str(rank)+'. '+title+' ['+aka.get_text().replace('’', '').replace('‘', '')+'] ('+year+', '+dir+')  ')
            else:
                print(str(rank)+'. '+title+' ('+year+', '+dir+')  ')



        rank += 1
        rating_idx += 1

    list_page += 1
