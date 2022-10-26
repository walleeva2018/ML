from tmdbv3api import TMDb
tmdb = TMDb()
tmdb.api_key = 'f658ac98b3201a511d101895c2e23b7b'
tmdb.language = 'en'
tmdb.debug = True
from tmdbv3api import Movie
from tmdbv3api import Discover
  
 
import nltk
from nltk.stem.porter import PorterStemmer
ps= PorterStemmer()

def stem(text):
  y=[]
  for i in text.split():
    y.append(ps.stem(i))
  return " ".join(y)


import re
from collections import Counter
import math

WORD = re.compile(r"\w+")

def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator



def doit(movieName,movieCategory):
    myMap={}
    movie= Movie()
    discover= Discover()
    myMap={}
    movieCategory=int(movieCategory)
    for k in range(5):
        show = discover.discover_movies({
            'with_genres': movieCategory,
            'page': k+1
        })
        for i in show:
            myMap[i['title']]=0
        get1=movie.search(movieName)
        get2=get1[0]['overview']
        for j in show:
            put=j['overview']
            get3=stem(get2)
            put1=stem(put)
            get_vector=text_to_vector(get3)
            put_vector=text_to_vector(put1)
            score=get_cosine(get_vector,put_vector)
            if(myMap[j['title']]+score>myMap[i['title']]):
                myMap[i['title']]=myMap[j['title']]+score
                if myMap[j['title']]==get1[0]['title']:
                    myMap[j['title']]=0
    return myMap

def sim(moviername):
    movie=Movie()
    return movie.search(moviername)


def justcheck():
    return "HEllo World"

def getit(myMap):
    sorted_values = sorted(myMap.values()) # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in myMap.keys():
            if myMap[k] == i:
                sorted_dict[k] = myMap[k]
                break

    #print(sorted_dict)

    from collections import OrderedDict

    # initializing dictionary
    res = OrderedDict(reversed(list(sorted_dict.items())))
    return res
def getPoster(genre):
  myMap={}
  movie= Movie()
  discover= Discover()
  genre=int(genre)
  for k in range(5):
    show = discover.discover_movies({
        'with_genres': genre,
        'page': k+1
        })
    for j in show:
      put=j['poster_path']
      myMap[j['title']]=put
  return myMap
def wPoster(name):
    movie=Movie()
    d=movie.search(name)
    if len(d)==0:
        return ""
    return d[0]

def lib_get(name):
    movie=Movie()
    search = movie.search(name)
    recommendations = movie.recommendations(search[0].id)
    return recommendations[0]

def check_sim(current,other):
    cnt=0
    for i in current:
        for j in  other:
            if i == j:
                cnt=cnt+1
    return cnt

def get_poster(movielist):
    movie=Movie()
    lula=[]
    for i in movielist:
        be=movie.search(i)
        be=be[0]
        lula.append({'name':be.title,
                      'poster': be.poster_path})
    return lula

