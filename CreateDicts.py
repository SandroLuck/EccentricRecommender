import csv
from contextlib import contextmanager
import pickle
from pathlib import Path
import os,inspect

from loadAndSaveLilMatrix import create_or_load_sparse_matrix
from load_or_create import load_or_create

def createDictUserIdToUserEccentricity():
    """
    Creates a dict user->User Eccentricity
    :return: dict
    """
    print("Creating Dict createDictUserIdToUserEccentricity")
    user_id_to_user_ecc=dict()
    with open('userEccentricity.dat', 'r') as uE:
        readerE = csv.reader(uE, delimiter=" ")
        tmpE = list(readerE)
        # add all user who liked a movie x to its dict
        for line in tmpE:
            user_id_to_user_ecc[int(line[0])]=float(line[1])
    return user_id_to_user_ecc

def create_dict_user_id_to_liked_items():
    """
    Creates a dict user->to list of liked items
    :return: dict
    """
    print("Creating Dict create_dict_user_id_to_liked_items")
    with open('mlm1uabove.dat', 'r') as uP:
        to_return = dict()
        readerP = csv.reader(uP, delimiter=" ")
        tmpP = list(readerP)
        # add all user who liked a movie x to its dict
        for id, line in enumerate(tmpP):
            for rat in line[1:]:
                if int(id+1) in to_return:
                    #id has to be +1 since userid starts from 1 and not 0
                    to_return[id+1].append(rat)
                else:
                    to_return[id+1]=[rat]
    return to_return

def create_dict_ecc():
    """
    Creates a dict item->Item Eccentricity
    :return: dict
    """
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
    """
    Creates a dict user->to recommendation for the user
    old approach
    :return: dict
    """
    from CreateMatrix import get_recommendation_matrix

    #
    mat = get_recommendation_matrix()[:10000,:20000]
    print("Creating Dict create_dict_user_id_to_recommends")
    print(type(mat))
    dict_userid_to_recommends = dict()
    for i in range(int(mat.shape[0])):
        row = mat.getrow(i).toarray()[0].tolist()
        #we dont need to look at zero recommends
        if True:
            # print(u_to_likes.getrow(i).nonzero()[1])
            dict_userid_to_recommends[i + 1] = [(index + 1, val) for index, val in enumerate(row) if val!=0]
    return dict_userid_to_recommends


def create_dict_user_id_to_recommends_from_mat(mat):
    """
    Creates a dict user->recommendations
    from a matrix
    :param mat: matrix to use
    :return:
    """
    mat = mat
    print("Creating Dict create_dict_user_id_to_recommends")
    print(type(mat))
    dict_userid_to_recommends = dict()
    for i in range(int(mat.shape[0])):
        row = mat.getrow(i).toarray()[0].tolist()
        #we dont need to look at zero recommends
        if True:
            # print(u_to_likes.getrow(i).nonzero()[1])
            dict_userid_to_recommends[i + 1] = [(index + 1, val) for index, val in enumerate(row) if val!=0]

    return dict_userid_to_recommends

def create_dict_names():
    """
    item->name of item
    can be used for analyzing
    :return:
    """
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
    """
    Creates a dict items->to user who liked this item
    :return:
    """
    print("Creating Dict createDictMovieIdToUsersWhoLiked")
    with open('mlm1uabove.dat', 'r') as uP:
        to_return = dict()
        readerP = csv.reader(uP, delimiter=" ")
        tmpP = list(readerP)
        # add all user who liked a movie x to its dict
        for id, line in enumerate(tmpP):
            for rat in line[1:]:
                if int(rat) in to_return:
                    #id has to be +1 since userid starts from 1 and not 0
                    to_return[int(rat)].append(id+1)
                else:
                    to_return[int(rat)]=[id+1]
    return to_return