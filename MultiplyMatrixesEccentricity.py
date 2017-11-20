from pathlib import Path
from logMovieStats import item_names_print
from scipy.sparse import lil_matrix,save_npz
import numpy as np
from CreateMatrix import create_matrix_user_likes,create_matrix_item_similarity
import pickle
import os,inspect
from CreateDicts import create_dict_ecc,create_dict_names, create_dict_user_id_to_recommends
from load_or_create import load_or_create
from operator import itemgetter


def generate_statistics_for_recommends():
    dict_userid_to_recommends = load_or_create('/DICT/UserIdToRecommends.dict', create_dict_user_id_to_recommends)
    for user in dict_userid_to_recommends:
        list_recommends=set(dict_userid_to_recommends[user])
        #delete vals which user alreay liked
        list_not_liked=

        if user==0:
            print(50*"THIS SHOULD NOT HAPPEN\n")


dict_userid_to_recommends=load_or_create('/DICT/UserIdToRecommends.dict',create_dict_user_id_to_recommends)
generate_statistics_for_recommends()


#old functions not needs currently
def print_maxes():
    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    item_similarity = load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)
    dict_names = load_or_create('/DICT/MovieIdToName.dict', create_dict_names)
    dict_ecc = load_or_create('/DICT/MovieIdToUserEccentricity.dict', create_dict_ecc)
    print(u_to_likes.shape, item_similarity.shape)
    mat = u_to_likes * item_similarity

    dict_userid_to_recommends = dict()

    recommends = []
    for i in range(mat.shape[1]):
        row = mat.getrow(i)
        if len(row.nonzero()[0]) != 0:
            # print(u_to_likes.getrow(i).nonzero()[1])
            if len(u_to_likes.getrow(i).nonzero()[1]) <= 5:
                # print("Amount of recommends:",len(row.nonzero()[0]))
                row = row.toarray()[0].tolist()
                max_val = max(i for i in row)
                recommends.append(
                    [max_val, row.index(max_val) + 1, i + 1, [i + 1 for i in u_to_likes.getrow(i).nonzero()[1]],
                     [row.index(max_val) + 1]])

    recommends = sorted(recommends, key=itemgetter(0))

    for i in recommends[-100:]:
        print("MAX id:", i[1])
        print("MAX val:", i[0])
        print("for user:", i[2])
        print("MOVIES HE ALREADY LIKED", 50 * "=")
        item_names_print(i[3], dict_names, dict_ecc)
        print("Movie Well recommend:" + 50 * '*')
        item_names_print(i[4], dict_names, dict_ecc)
        print(50 * "#")
