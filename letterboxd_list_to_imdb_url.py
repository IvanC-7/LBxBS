from bs4 import BeautifulSoup
import requests
import sys

listurl = 'https://letterboxd.com/ivan0716/list/2021-ranked/'

if len(sys.argv) == 2:
    listurl = ''+sys.argv[1]+''

list_page = 1
total_films = 0
imdburl_found = 0
not_found = []

# iterate through list pages
while list_page < 100:
    webpage = requests.get(listurl + 'detail/page/' + str(list_page) + '/')
    soup = BeautifulSoup(webpage.content, 'html.parser')

    # find all films in list
    films = soup.find_all(attrs={"data-target-link":True})

    # break if no films found on current page
    if not films:
        break

    # generate url
    for film in films:
        # get lb url
        total_films += 1

        lb_url = 'https://letterboxd.com' + film['data-target-link']
        webpage = requests.get(lb_url)
        soup = BeautifulSoup(webpage.content, 'html.parser')

        # get imdb url from letterboxd film page
        imdb_url = soup.find(attrs={"data-track-action": "IMDb"})

        if imdb_url is not None:
            print(imdb_url['href'].replace("maindetails", ""))
            imdburl_found += 1
        else:
            title = soup.find(attrs={"property": "og:title"})
            not_found.append(title['content'])

    list_page += 1

print('\n\n'+str(imdburl_found)+'/'+str(total_films)+' URLs found')

if len(not_found) > 0:
    print('\nNot found:')
    for x in not_found:
        print(x)

