import csv
from operator import itemgetter
from itertools import islice
from statistics import median, mean
from random import shuffle


def calculateUserSimilarityAverageItemEccentricityMatrix(percentageOfUsersToLookAt=1.0):
    """
    Calculate User Similarity and output to file
    :param percentageOfUsersToLookAt: only look at subset of users, by percentage
    """
    with open('userMlAboveAvg.dat', 'r') as u:
        with open('userEccentricity.dat', 'r') as UE:
            with open('itemEccentricity.dat', 'r') as IE:
                with open('movies.csv', 'r', encoding='utf-8') as item_names:
                    reader = csv.reader(u, delimiter=" ")
                    user_positives = list(reader)

                    reader = csv.reader(IE, delimiter=" ")
                    item_eccentricity = list(reader)

                    reader = csv.reader(UE, delimiter=" ")
                    user_eccentricity = list(reader)

                    reader = csv.reader(item_names, delimiter=",")
                    item_names = list(reader)
    with open('userSimilarityAverageItemEccentricityMatrix.dat', 'w+') as w:
        with open('userSimilarityAverageItemEccentricitFileResult.dat', 'w+') as wOut:
            with open('userSimilarityEccentricityAndSet.dat','w+') as w_small:
                item_dict_names=dict()
                user_dict_ecc=dict()
                for item in item_names[1:]:
                    try:
                        item_dict_names[int(item[0])]=item[1]
                    except:
                        print(item)
                        item_dict_names[int(item[0])]='THISnameHadError'

                for user in user_eccentricity:
                    user_dict_ecc[int(user[0])]=float(user[1])
                # Create and array or enough size for max(user_id) around 950
                item_ecc_dict=dict()
                for item in item_eccentricity:
                    item_ecc_dict[int(item[0])]=float(item[1])
                user_item_dict=dict()
                for id,item in enumerate(user_positives):
                    #id+1 is the uderid
                    user_item_dict[int(id+1)]=set(map(int, item[1:]))

                high_eccentric_user_similiarity_pair=[]
                # If we dont wnt to go through entire alogirthm specific how man we want ot iter
                user_amount_to_process=int(len(user_item_dict)*percentageOfUsersToLookAt)

                min_ecc,max_ecc=get_eccentricicty_min_max(item_ecc_dict)
                print(min_ecc,max_ecc)
                print("Mean eccentricity:",mean(item_ecc_dict.values()))
                print("Median eccentricity:",median(item_ecc_dict.values()))
                median_ecc=median(item_ecc_dict.values())
                count_percentage_of_movies_bigger_zero(item_ecc_dict,item_dict_names,min_ecc, max_ecc, median_ecc)
                for user_1 in take(user_amount_to_process,user_item_dict):
                    #only if the user is an eccentric user calculate
                    if user_dict_ecc[user_1]>=0:
                        for user_2 in take(user_amount_to_process,user_item_dict):
                            if user_dict_ecc[user_2] >= 0:
                                item_intersection=user_item_dict[user_1]&user_item_dict[user_2]
                                if user_1!=user_2 and len(item_intersection)>0:
                                    # if the interscetion is not empty
                                    item_eccentricity_sum=0
                                    for item in item_intersection:
                                        to_sum=calulate_to_sum_equation(item_ecc_dict[item],min_ecc, max_ecc, median_ecc)

                                        # this calculates the sum of the eccentricities which have been rescaled to one
                                        item_eccentricity_sum+=to_sum
                                    item_eccentricity_avg=item_eccentricity_sum/len(user_item_dict[user_1])
                                    if item_eccentricity_sum!=0:
                                        high_eccentric_user_similiarity_pair.append([item_eccentricity_avg,"u1:"+str(user_1),"u1_len_likes:"+str(len(user_item_dict[user_1])), "u2:"+str(user_2),"u2_len_likes:"+str(len(user_item_dict[user_2])),len(item_intersection),item_intersection ])
                print("Loop Is over:")
                high_eccentric_user_similiarity_pair=sorted(high_eccentric_user_similiarity_pair,key=itemgetter(0))
                #for item in high_eccentric_user_similiarity_pair:
                    #print item[0]
                    #item_names_print(item_dict_names, item[7])
                for item in high_eccentric_user_similiarity_pair:
                    wOut.write("%s\n" % " ".join(str(x) for x in item))
                for item in high_eccentric_user_similiarity_pair:
                    print(item[0])
                    w_small.write(str(float(item[0]))+","+str(list(item[6]))+'\n')
                for item in high_eccentric_user_similiarity_pair[-100:]:
                    if len(item[6])<10:
                        print("User1 id=" + item[1] + " Is similar to User2 id=" + item[3])
                        print("Their values is:"+str(item[0]))
                        item_names_print(item_dict_names, item_ecc_dict,item[6])


def take(n, iterable):
    "Return first n items of the iterable as a list"
    to_return=list(islice(iterable, n))
    shuffle(to_return)
    return to_return

def item_names_print(dict_names, dict_ecc,list_ids):
    print(100*'-')
    for item in list_ids:
        print(dict_names[item])
        print("Item eccentricity:"+str(dict_ecc[item]))
        print('https://www.google.ch/search?q='+dict_names[item].replace(' ','+').replace(',','%2C').replace('(','').replace(')','').replace('\'','%27'))
    print(100*'-')

def get_eccentricicty_min_max(dict_items):
    """
    Gets max and min of dict_items
    :param dict_items: 
    :return: min_val, max_val
    """
    min_val = min(i for i in dict_items.values())
    max_val=max(i for i in dict_items.values())
    print(dict_items.items())
    return min_val,max_val

def count_percentage_of_movies_bigger_zero(dict_ecc, dict_name,min_prev, max_prev, median_ecc):
    count=0
    dict_movie_likes=amount_likes_for_movie_id()
    for key,item in dict_ecc.items():
        if calulate_to_sum_equation(item,min_prev, max_prev, median_ecc)>0:
            count+=1
            print(50*"°")
            item_names_print(dict_name,dict_ecc,[key])
            print("AMOUNT LIKES",dict_movie_likes[key])
            print(50*"°")
    print("Percentage of movies bigger zero",count/(len(dict_ecc)))


def amount_likes_for_movie_id():
    with open('userMlAboveAvg.dat', 'r') as uP:
        movie_likes=dict()
        readerP = csv.reader(uP, delimiter=" ")
        tmpP = list(readerP)
        # count all likes for a movie
        for id, line in enumerate(tmpP):

            for rat in line[1:]:
                if int(rat) in movie_likes.keys():
                    movie_likes[int(rat)]+=1
                else:
                    movie_likes[int(rat)]=1
        return movie_likes

def calulate_to_sum_equation(x,min_prev, max_prev, median_ecc):
    """
    Forces range of eccentricity into range [-1,1]
    :param x: val to convert
    :param min_prev: minimum of previouse dict
    :param max_prev: maximum of previouse dict
    :return: val converted to in range[-1,1]
    """
    to_return=0
    if x>median_ecc-0.5:
        to_return=x+abs(median_ecc-0.5)
    return to_return


calculateUserSimilarityAverageItemEccentricityMatrix(percentageOfUsersToLookAt=0.1)