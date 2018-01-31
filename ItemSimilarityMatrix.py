from scipy.sparse import lil_matrix,save_npz
import numpy as np
from CreateDicts import createDictUserIdToUserEccentricity, createDictMovieIdToUsersWhoLiked,create_dict_names,create_dict_ecc
from logMovieStats import item_names_print
from statistics import mean,median
from operator import itemgetter

def limit_gen(iterable,stop):
    for index,value in enumerate(iterable):
        if index>=stop:
            return
        yield value
def CalculateItemSimilarity(item1_users, item2_users, user_to_ecc):
    """
    Calculate similarity between two user, by user user Eccentric similarity
    :param item1_users:
    :param item2_users:
    :param user_to_ecc:
    :return:
    """
    users1=set(item1_users)
    users2=set(item2_users)

    intersection=users1&users2
    #sum_ecc_users=sum([user_to_ecc[user] for user in intersection])
    #return sum_ecc_users/float(len(intersection))
    if len(intersection)>=5:
        return mean([user_to_ecc[user] for user in intersection])
    else:
        return 0

def outputSparseMatrixStats(spars_matrix, dict_item_id_to_users):


    """
    Analyzing for Matrix
    :param spars_matrix:
    :param dict_item_id_to_users:
    """
    ecc_item_sim_nonzero = spars_matrix.nonzero()
    dict_names=create_dict_names()
    dict_item_ecc=create_dict_ecc()

    i_item_index = ecc_item_sim_nonzero[0]
    j_item_index = ecc_item_sim_nonzero[1]
    results_to_print=list()
    for index in range(len(i_item_index)):
        results_to_print.append([i_item_index[index], j_item_index[index], spars_matrix[i_item_index[index], j_item_index[index]]])
    results_to_print=sorted(results_to_print, key=itemgetter(2))
    for item_pair in results_to_print[-100:]:
        print(50*"#")
        item_names_print([item_pair[0],item_pair[1]],dict_names,dict_item_ecc)
        print("THEIR VALUE IS:",item_pair[2])
        a=set(dict_item_id_to_users[int(item_pair[0])])
        b=set(dict_item_id_to_users[int(item_pair[1])])
        intersection= a&b
        print("Intersection Length:",len(intersection))
        print(50*"#")

def CreateItemSimilarityMatrix(threshold_min_movie_likes=5,threshold_max_movies=2000000):
    """
    Creates matrix similarty
    :param threshold_min_movie_likes:
    :param threshold_max_movies:
    """
    user_to_ecc=createDictUserIdToUserEccentricity()
    print(100*"#")
    item_to_users=createDictMovieIdToUsersWhoLiked()
    print(100*"#")
    print("Loaded Dicts..")
    max_id = max(int(item_id) for item_id in item_to_users)

    item_similarity_matrix = lil_matrix((max_id + 1, max_id + 1), dtype=np.float)
    skipped_count=0
    print(100*"#")
    print("Calculating the matrix:")

    print("Mean length:",mean([len(list(item_to_users[item1])) for item1 in item_to_users]))
    print("Median length:",median([len(list(item_to_users[item1])) for item1 in item_to_users]))

    for index1,item1 in enumerate(item_to_users):
        # if enough users liked the movie
        if threshold_min_movie_likes<= len(item_to_users[item1]) <= threshold_max_movies:
            for index2,item2 in limit_gen(enumerate(item_to_users),index1):
                if threshold_min_movie_likes <= len(item_to_users[item2]) <= threshold_max_movies:
                    item_similarity_matrix[item1,item2]=CalculateItemSimilarity(item_to_users[item1],item_to_users[item2],user_to_ecc)
                    #for now make matrix symetric
                    item_similarity_matrix[item2,item1]=item_similarity_matrix[item1,item2]

        else:
            skipped_count += 1
    print("MATRIX DONE")
    print("WE skipped:", skipped_count)
    print("OF:", len(item_to_users))
    print("Means we considered in percentage :", 1 - skipped_count / float(len(item_to_users)))
    print("Means we considered exactly:", len(item_to_users) - skipped_count)
    outputSparseMatrixStats(item_similarity_matrix, item_to_users)
    print("The Length of the nonzeros was:",len(item_similarity_matrix.nonzero()[0]))

CreateItemSimilarityMatrix()