import csv
import pickle
from pathlib import Path

from tqdm import tqdm
from scipy.sparse import lil_matrix,save_npz
import numpy as np
import os,inspect
from CreateDicts import createDictUserIdToUserEccentricity,createDictMovieIdToUsersWhoLiked
from load_or_create import load_or_create
from statistics import mean

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
    users1=set(item1_users)
    users2=set(item2_users)
    intersection=users1&users2
    if len(intersection)>=5:
        res=mean([pos_or_zero(user_to_ecc[user]) for user in intersection])
        if res>=0:
            return res
        else:
            return 0
    else:
        return 0

def get_recommendation_matrix():
    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    item_similarity = load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)
    print("Multiplying MAtrix")
    mat=u_to_likes * item_similarity
    print("Multiplication has been done")
    return mat



def create_matrix_user_likes():
    """
    return the matrix shape[max_user,max_movie_id]
    each entry i,j means user i liked item j
    note: user_id-1 and item_id-1 are i and j, since movielense numerates ids from 1 but matrix numerates from 0
    :return: lil_matrix(shape=(max_user,max_movie_id))
    """
    print("Creating Matrix UserLikes")
    with open("userMlAboveAvg.dat", "r") as f:
        reader = csv.reader(f, delimiter=" ")
        items_liked = list(reader)
        max_item_id = max(int(item_id) for items in items_liked for item_id in items[1:])
        max_user_id = len(items_liked)
        print("Amount Users:", max_user_id)
        print("Amount Items:", max_item_id)
        # User bool matrix since we only care about if liked or not
        to_return = lil_matrix((max_user_id, max_item_id), dtype=np.bool)
        # the first elem in userAboveAverage is not important
        for id, item_ids in tqdm(enumerate(items_liked)):
            for item in item_ids[1:]:
                to_return[id, int(item) - 1] = True
    return to_return

def create_matrix_item_similarity(threshold_min_movie_likes=50,threshold_max_movies=1000):
    user_to_ecc = load_or_create('/Dict/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    item_to_users = load_or_create('/Dict/MovieIdToUsersWhoLiked.dict',createDictMovieIdToUsersWhoLiked)
    max_id = max(int(item_id) for item_id in item_to_users)
    item_similarity_matrix = lil_matrix((max_id , max_id ), dtype=np.float)
    print("CREATING MATRIX ITEM SIMILARITY, might take long")
    for index1, item1 in tqdm(enumerate(item_to_users)):
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
    return item_similarity_matrix