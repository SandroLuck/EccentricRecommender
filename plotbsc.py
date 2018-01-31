from CreateDicts import create_dict_ecc, createDictUserIdToUserEccentricity, createDictMovieIdToUsersWhoLiked
from load_or_create import load_or_create
import matplotlib.pyplot as plt
import numpy as np

def plotUserEcc(dicts):
    to_plot=[]

    for k in dicts:
        to_plot.append(len(dicts[k]))


    to_plot=np.array(to_plot)

    plt.hist(to_plot, 50)
    plt.ylabel('Amount of books with this many likes')
    plt.xlabel("Amount of likes for books")
    plt.show()

    print("done")

def plotMovieConcentration(dicts):
    to_plot=[]

    for k in dicts:
        to_plot.append(len(dicts[k]))

    print(to_plot)
    to_plot=np.array(to_plot)
    to_plot.sort()
    print(to_plot)
    x=[]
    y=[]
    for xth,yth in enumerate(to_plot):
        x.append(xth)
        y.append(yth)
    plt.bar(x,y)
    plt.ylabel('Amount of likes for this movie')
    plt.xlabel("Position of5movie in ordering sorted by interactions")
    plt.show()
    sum=0
    perc=10
    amounts=0
    sum_total=0
    for i in y:
        sum_total+=i
    print(sum_total)
    sum=0
    total_perc=0
    for i in range(1,11):
        for j in y[int(0.1*(i-1)*len(y)):int(0.1*i*len(y))]:
            sum+=j
        total_perc+=float(sum)/float(3300252)
        print(float(sum)/float(3300252),i)
        sum=0
    print(total_perc)

    print("done")


dict_likes = load_or_create('/DICT/MovieIdToUsersWhoLiked.dict', createDictMovieIdToUsersWhoLiked)

#dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
#user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
#plotMovieConcentration(dict_likes)
plotUserEcc(dict_likes)
#user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)