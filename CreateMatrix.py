import csv
from scipy.sparse import lil_matrix
import numpy as np
from CreateDicts import createDictUserIdToUserEccentricity,createDictMovieIdToUsersWhoLiked,create_dict_ecc
from load_or_create import load_or_create

def sigmoid(x, sigmoid_strength=0.3, strength=0.15):
    """
    Calculates the sigmoid for the combination
    :param x: user eccentricity
    :param sigmoid_strength:
    :param strength:
    :return:
    """
    return (1 / (1 + np.exp(-x*sigmoid_strength)))*strength

def pos_or_zero(x):
    if x>=0:
        return x
    return 0

def limit_gen(iterable,stop):
    for index,value in enumerate(iterable):
        if index>=stop:
            return
        yield value
def CalculateItemSimilarity(item1_users, item2_users, user_to_ecc):
    """
    Calculates the user, user similarity
    :param item1_users: u1
    :param item2_users: u2
    :param user_to_ecc:
    :return:
    """
    users1=set(item1_users)
    users2=set(item2_users)
    intersection=users1&users2
    if len(intersection)>=5:
        #res=mean([pos_or_zero(user_to_ecc[user]) for user in intersection])
        sum=0
        items=0
        for i in intersection:
            i_val=user_to_ecc[i]
            if i_val>0:
                sum+=pos_or_zero(user_to_ecc[i])
                items+=1
        if sum>0:
            res = sum / float(items)
            return res
        else:
            return 0
    else:
        return 0

def get_recommendation_matrix():
    """
    returns the recommendations matrix
    :return:
    """
    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    item_similarity = load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)
    print("Multiplying MAtrix")
    mat=u_to_likes * item_similarity
    print("Multiplication has been done")
    return mat

def mix_matrix_for_ecc_and_none_ecc(mat_ecc, mat_none_ecc):
    """
    mixes to matrixes, approach mix them mat_ecc for eccentric users
    and mat_none_ecc for below 0 eccentric users, not used anymore
    :param mat_ecc:
    :param mat_none_ecc:
    :return:
    """
    print("mixing mat for ecc and none ecc")
    print(mat_ecc.shape,mat_none_ecc.shape)
    assert mat_ecc.shape==mat_none_ecc.shape
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    mat=lil_matrix((mat_ecc.shape), dtype=np.float)
    for i in range(int(mat.shape[0])):
        try:
            ecc=user_to_ecc[i+1]
            if ecc>=0:
                row=mat_ecc.getrow(i)
            else:
                row=mat_none_ecc.getrow(i)
            mat[i, :] = row
        except KeyError:
            print(50*'-')
            #this means we had  a key error in dict
            pass
    return mat

def mix_matrix_for_ecc_and_none_ecc_with_alpha(mat_ecc, mat_none_ecc):
    """
    Sigmoid weigthed matrix combination
    :param mat_ecc:
    :param mat_none_ecc:
    :return: the mixed matrix
    """
    print("mixing mat for ecc and none ecc")
    print(mat_ecc.shape,mat_none_ecc.shape)
    assert mat_ecc.shape==mat_none_ecc.shape
    #user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    mat=lil_matrix((mat_ecc.shape), dtype=np.float)
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    for i in range(int(mat.shape[0])):
        try:
            #ecc=user_to_ecc[i+1]
            mat[i, :] = (mat_ecc.getrow(i))*sigmoid(user_to_ecc[i+1])+mat_none_ecc.getrow(i)*(1-sigmoid(user_to_ecc[i+1]))
        except KeyError:
            print(50*'-')
            #this means we had  a key error in dict
            pass
    return mat


def create_matrix_user_likes():
    """
    return the matrix shape[max_user,max_movie_id]
    each entry i,j means user i liked item j, multiplied with user_eccentricity
    note: user_id-1 and item_id-1 are i and j, since movielense numerates ids from 1 but matrix numerates from 0
    :return: lil_matrix(shape=(max_user,max_movie_id))
    """
    print("Creating Matrix UserLikes")
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    with open("mlm1uabove.dat", "r") as f:
        reader = csv.reader(f, delimiter=" ")
        items_liked = list(reader)
        max_item_id = max(int(item_id) for items in items_liked for item_id in items[1:])
        max_user_id = len(items_liked)

        print("Amount Users:", max_user_id)
        print("ssrAmount Items:", max_item_id)
        # User bool matrix since we only care about if liked or not
        to_return = lil_matrix((max_user_id, max_item_id), dtype=np.bool)
        # the first elem in userAboveAverage is not important
        for id, item_ids in enumerate(items_liked):

            for item in item_ids[1:]:
                # Currently only calculate positve eccentric people
                if True:
                    to_return[id, int(item) - 1] = True
    return to_return

def create_matrix_item_similarity(threshold_min_movie_likes=5,threshold_max_movies=2000000):
    """
    Create item similarity
    :param threshold_min_movie_likes:
    :param threshold_max_movies:
    :return:
    """
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    item_to_users = load_or_create('/DICT/MovieIdToUsersWhoLiked.dict',createDictMovieIdToUsersWhoLiked)
    item_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)

    max_id = max(int(item_id) for item_id in item_to_users)
    item_similarity_matrix = lil_matrix((max_id , max_id ), dtype=np.float)
    print("CREATING MATRIX ITEM SIMILARITY, might take long")
    for index1, item1 in enumerate(item_to_users):
        # if enough users liked the movie
        # careful with id in dataset starts from 0 in matrix start from 0, thus -1
        if threshold_min_movie_likes <= len(item_to_users[item1]) <= threshold_max_movies:
            for index2, item2 in limit_gen(enumerate(item_to_users), index1):
                if threshold_min_movie_likes <= len(item_to_users[item2]) <= threshold_max_movies:
                    item_similarity_matrix[item1-1, item2-1] = CalculateItemSimilarity(item_to_users[item1],
                                                                                   item_to_users[item2], user_to_ecc)
                    # for now make matrix symetric
                    item_similarity_matrix[item2-1, item1-1] = item_similarity_matrix[item1-1, item2-1]
                    #diagonal stays zero for now
    print('shape ecc_recs:')
    return item_similarity_matrix