import csv
from contextlib import contextmanager
from tqdm import tqdm
import pickle
from pathlib import Path
import os,inspect
from load_or_create import load_or_create

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

def create_dict_user_id_to_recommends():
    #import only for this function
    from CreateMatrix import create_matrix_item_similarity, create_matrix_user_likes

    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    item_similarity = load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)
    print("Creating Dict create_dict_user_id_to_recommends")
    mat = u_to_likes * item_similarity
    dict_userid_to_recommends = dict()
    for i in range(mat.shape[1]):
        row = mat.getrow(i)
        #we dont need to look at zero recommends
        if len(row.nonzero()[0]) != 0:
            # print(u_to_likes.getrow(i).nonzero()[1])
            if len(u_to_likes.getrow(i).nonzero()[1]) <= 5:
                dict_userid_to_recommends[i + 1] = [(index + 1, val) for index, val in enumerate(row)]
    return dict_userid_to_recommends


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
        to_return = dict()
        readerP = csv.reader(uP, delimiter=" ")
        tmpP = list(readerP)
        # add all user who liked a movie x to its dict
        for id, line in tqdm(enumerate(tmpP)):
            for rat in line[1:]:
                if int(rat) in to_return:
                    #id has to be +1 since userid starts from 1 and not 0
                    to_return[int(rat)].append(id+1)
                else:
                    to_return[int(rat)]=[id+1]
    return to_return