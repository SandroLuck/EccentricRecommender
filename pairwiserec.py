from operator import itemgetter

import gc
import numpy as np
from scipy.sparse import lil_matrix
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

from CreateDicts import createDictUserIdToUserEccentricity, create_dict_ecc, create_dict_names, \
    create_dict_user_id_to_liked_items, create_dict_user_id_to_recommends_from_mat
from CreateMatrix import create_matrix_user_likes, mix_matrix_for_ecc_and_none_ecc, create_matrix_item_similarity, \
    mix_matrix_for_ecc_and_none_ecc_with_alpha
from load_or_create import load_or_create
from logMovieStats import item_names_print
import matplotlib.pyplot as plt
from statistics import mean,median

def print_maxes(mat):
    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    dict_names = load_or_create('/DICT/MovieIdToName.dict', create_dict_names)
    dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)
    dict_userid_to_moviesliked = load_or_create('/DICT/UserIdToLikedMovies.dict', create_dict_user_id_to_liked_items)

    dict_userid_to_recommends = dict()
    print("STARTING ECC CALC")
    recommends = []
    for i in range(int(mat.shape[0]*0.5)):
        row = mat.getrow(i)
        if len(row.nonzero()[0]) != 0:
            # print(u_to_likes.getrow(i).nonzero()[1])
            if len(u_to_likes.getrow(i).nonzero()[1])<10 and user_to_ecc[i+1]>0:
                # print("Amount of recommends:",len(row.nonzero()[0]))
                row = row.toarray()[0].tolist()
                max_val = max(val for val in row if str(row.index(val) + 1) not in dict_userid_to_moviesliked[i+1])
                print('SUM is:',sum(val for val in row if str(row.index(val) + 1) not in dict_userid_to_moviesliked[i+1]))
                print('SUM with all is:',sum(val for val in row))

                index_max=row.index(max_val) + 1

                recommends.append(
                    [max_val, row.index(max_val) + 1, i + 1, [i + 1 for i in u_to_likes.getrow(i).nonzero()[1]],
                     [row.index(max_val) + 1],user_to_ecc[i+1]])

    recommends = sorted(recommends, key=itemgetter(0))

    for i in recommends[-100:]:
        print("MAX id:", i[1])
        print("MAX val:", i[0])
        print("Users ECC:",i[5])
        print("for user:", i[2])
        print("MOVIES HE ALREADY LIKED", 50 * "=")
        item_names_print(i[3], dict_names, dict_ecc)
        print("Movie Well recommend:" + 50 * '*')
        item_names_print(i[4], dict_names, dict_ecc)
        print(50 * "#")

def generate_statistics_for_recommends(mat,k=20):
    dict_userid_to_recommends = create_dict_user_id_to_recommends_from_mat(mat)
    dict_userid_to_moviesliked = load_or_create('/DICT/UserIdToLikedMovies.dict', create_dict_user_id_to_liked_items)
    dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)

    top_items_ecc_all=[]
    user_ecc=[]
    user_avg_rec_ecc=[]
    to_iter=[i for i in dict_userid_to_recommends]
    print("starting to calculate plot data...")
    counter_ecc=0
    counter_none_ecc=0
    for user in tqdm(to_iter[:1000]):

        #delete vals which user alreay liked
        list_recommends_not_liked_yet=[[i,j]for i,j in dict_userid_to_recommends[user] if i not in dict_userid_to_moviesliked[user]]
        list_recommends_not_liked_yet=sorted(list_recommends_not_liked_yet, key=itemgetter(1))
        #only take top k
        top_items=list_recommends_not_liked_yet[-20:]
        top_items_ecc=[dict_ecc[item] for item,val in top_items]
        #append ecc vals to plot list
        if len(top_items_ecc) > 0:
            user_ecc.append(user_to_ecc[user])
            if user_to_ecc[user]>0:
                counter_ecc+=1
            else:
                counter_none_ecc+=1
            user_avg_rec_ecc.append(mean(top_items_ecc))
        for i in top_items_ecc:
            top_items_ecc_all.append(i)
        if user==0:
            print(50*"THIS SHOULD NOT HAPPEN\n")
    print('Starting to plot:')
    print("ecc users:",counter_ecc)
    print("none ecc users:",counter_none_ecc)
    #Now plot box plot of all ecc
    plt.scatter(x=user_ecc,y=user_avg_rec_ecc)
    plt.show()
    print('Overall avg ecc of users in box:',mean(user_ecc))
    plt.boxplot(top_items_ecc_all)
    plt.show()



amount_of_items=5000

u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)

print(type(u_to_likes))
print(u_to_likes.shape)
u_likes=u_to_likes
print(type(u_likes))
print(u_likes.shape)

pair_wise_rat=cosine_similarity(u_likes.transpose()[:amount_of_items,:])
recommends=lil_matrix(u_to_likes[:10000,:amount_of_items]*pair_wise_rat)
recommends_ecc=load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)



mat_mixed=mix_matrix_for_ecc_and_none_ecc_with_alpha(recommends_ecc[:recommends.shape[0],:recommends.shape[1]],recommends, alpha=0.35)
print(type(mat_mixed))
gc.collect()
print_maxes(mat_mixed)
#generate_statistics_for_recommends(mat_mixed)
