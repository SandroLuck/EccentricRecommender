import csv
from tqdm import tqdm

def createDictUserIdToUserEccentricity():
    print("Creating Dict createDictUserIdToUserEccentricity")
    user_id_to_user_ecc=dict()
    with open('userEccentricity.dat', 'r') as uE:
        readerE = csv.reader(uE, delimiter=" ")
        tmpE = list(readerE)
        # add all user who liked a movie x to its dict
        for line in tqdm(tmpE):
            user_id_to_user_ecc[int(line[0])]=float(line[1])
    return user_id_to_user_ecc

def create_dict_ecc():
    print("Creating Dict create_dict_ecc")
    with open('itemEccentricity.dat', 'r') as IE:
        reader = csv.reader(IE, delimiter=" ")
        item_eccentricity = list(reader)
        item_ecc_dict = dict()
        for item in item_eccentricity:
            item_ecc_dict[int(item[0])] = float(item[1])
    return item_ecc_dict

def create_dict_names():
    print("Creating Dict create_dict_names")
    with open('movies.csv','r', encoding='utf-8') as item_names:
        reader = csv.reader(item_names, delimiter=",")
        item_names = list(reader)
        dict_names = dict()
        for item in item_names[1:]:
            try:
                dict_names[int(item[0])] = item[1]
            except:
                dict_names[int(item[0])] = 'THISnameHadError'
        return dict_names

def createDictMovieIdToUsersWhoLiked():
    print("Creating Dict createDictMovieIdToUsersWhoLiked")
    with open('userMlAboveAvg.dat', 'r') as uP:
        users_who_liked_movie = dict()
        readerP = csv.reader(uP, delimiter=" ")
        tmpP = list(readerP)
        # add all user who liked a movie x to its dict
        for id, line in tqdm(enumerate(tmpP)):
            for rat in line[1:]:
                if int(rat) in users_who_liked_movie:
                    #id has to be +1 since userid starts from 1 and not 0
                    users_who_liked_movie[int(rat)].append(id+1)
                else:
                    users_who_liked_movie[int(rat)]=[id+1]
        return users_who_liked_movie