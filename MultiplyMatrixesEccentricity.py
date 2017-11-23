from logMovieStats import item_names_print

from CreateMatrix import create_matrix_user_likes,create_matrix_item_similarity
from CreateDicts import create_dict_ecc,create_dict_names, create_dict_user_id_to_recommends, create_dict_user_id_to_liked_items, createDictUserIdToUserEccentricity
from load_or_create import load_or_create
from operator import itemgetter
from statistics import mean,median
import matplotlib.pyplot as plt
from tqdm import tqdm
from CreateMatrix import get_recommendation_matrix

from loadAndSaveLilMatrix import create_or_load_sparse_matrix

def generate_statistics_for_recommends(k=20):
    dict_userid_to_recommends = load_or_create('/DICT/UserIdToRecommends.dict', create_dict_user_id_to_recommends)
    dict_userid_to_moviesliked = load_or_create('/DICT/UserIdToLikedMovies.dict', create_dict_user_id_to_liked_items)
    dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
    user_to_ecc = load_or_create('/Dict/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)

    top_items_ecc_all=[]
    user_ecc=[]
    user_avg_rec_ecc=[]
    to_iter=[i for i in dict_userid_to_recommends]
    for user in tqdm(to_iter[-1000:]):

        #delete vals which user alreay liked
        list_recommends_not_liked_yet=[[i,j]for i,j in dict_userid_to_recommends[user] if i not in dict_userid_to_moviesliked[user]]
        list_recommends_not_liked_yet=sorted(list_recommends_not_liked_yet, key=itemgetter(1))
        #only take top k
        top_items=list_recommends_not_liked_yet[-20:]
        top_items_ecc=[dict_ecc[item] for item,val in top_items]
        #append ecc vals to plot list
        if len(top_items_ecc) > 0:
            user_ecc.append(user_to_ecc[user])
            user_avg_rec_ecc.append(mean(top_items_ecc))
        for i in top_items_ecc:
            top_items_ecc_all.append(i)
        if len(top_items_ecc)>0 and False:
            max_ecc=max(i for i in top_items_ecc)
            min_ecc=min(i for i in top_items_ecc)
            median_ecc=median(top_items_ecc)
            avg_ecc=mean(top_items_ecc)
            print(100*'-')
            print('USER '+str(user))
            print('USER ecc:',user_to_ecc[user])
            print('Max ecc:',max_ecc)
            print('Min ecc:',min_ecc)
            print('Median ecc:',median_ecc)
            print('Mean ecc:',avg_ecc)

        if user==0:
            print(50*"THIS SHOULD NOT HAPPEN\n")
    print('Starting to plot:')
    #Now plot box plot of all ecc
    plt.scatter(x=user_ecc,y=user_avg_rec_ecc)
    plt.show()
    print('Overall avg ecc of users in box:',mean(user_ecc))
    plt.boxplot(top_items_ecc_all)
    plt.show()


#generate_statistics_for_recommends()

#old functions not needs currently
def print_maxes():
    u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
    dict_names = load_or_create('/DICT/MovieIdToName.dict', create_dict_names)
    dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
    mat = get_recommendation_matrix()

    dict_userid_to_recommends = dict()

    recommends = []
    for i in tqdm(range(int(mat.shape[1]*0.2))):
        row = mat.getrow(i)
        if len(row.nonzero()[0]) != 0:
            # print(u_to_likes.getrow(i).nonzero()[1])
            if len(u_to_likes.getrow(i).nonzero()[1]) <= 10:
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

def print_max_similar():
    dict_names = load_or_create('/DICT/MovieIdToName.dict', create_dict_names)
    dict_ecc = load_or_create('/DICT/MovieIdToItemEccentricity.dict', create_dict_ecc)
    mat = load_or_create("/Matrix/ItemSimilarityEccentricity.matrix", create_matrix_item_similarity)
    maxes=[]
    for i in tqdm(range(int(mat.shape[1]*0.1))):
        row = mat.getrow(i)
        if len(row)>0:
            max_curr=max(i for i in row)
            maxes.append([i+1,row.index(max_curr) + 1,max_curr])
    maxes = sorted(maxes, key=itemgetter(2))
    for i,j,val in maxes:
        print("Val is:",val)
        item_names_print([i,j], dict_names, dict_ecc)

print_max_similar()
