from operator import itemgetter
from scipy import stats
import random
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
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

def calculateRecallAt(mat,train,k=50):
    """
    calculates the recall
    :param mat: recommendation matrix
    :param train: trainings matrix
    :param k: recall at
    """
    dict_userid_to_recommends = create_dict_user_id_to_recommends_from_mat(mat)
    dict_userid_to_moviesliked = load_or_create('/DICT/UserIdToLikedMovies.dict', create_dict_user_id_to_liked_items)
    user_to_ecc = load_or_create('/DICT/UserIdToUserEccentricity.dict',createDictUserIdToUserEccentricity)

    recalls = []
    recalls_ecc_0_05=[]
    recalls_ecc_05_1=[]
    recalls_ecc_1_15=[]
    recalls_ecc_15_2=[]
    recalls_ecc_2_25=[]
    recalls_ecc_25=[]
    hits=0
    top_n_items=0
    counts=0
    for user in dict_userid_to_moviesliked:
        try:
            list_recommends=[[i,j]for i,j in dict_userid_to_recommends[user]]
            list_recommends=sorted(list_recommends, key=itemgetter(1),reverse=True)
            list_liked=[int(i) for i in dict_userid_to_moviesliked[user]]

            train_set=[int(i)+1 for i in train.getrow(int(user)-1).rows[0]]
            hits=0
            if len(list_liked)-len(train_set)>=2 :
                counts+=1
                top_n_items=0
                for i,j in list_recommends:
                    # ignore item in the training set
                    if i in train_set:
                        continue
                    #print("Recs:",list_recommends[:20])
                    #print("liked:",list_liked)
                    if i in list_liked:
                        hits += 1
                    top_n_items += 1
                    if top_n_items == k:
                        break
                recalls.append(hits / float(len(list_liked)-len(train_set)))
                if 0<user_to_ecc[user]<=0.5:
                    recalls_ecc_0_05.append(hits / float(len(list_liked) - len(train_set)))
                if 0.5<user_to_ecc[user]<=1:
                    recalls_ecc_05_1.append(hits / float(len(list_liked) - len(train_set)))
                if 1<user_to_ecc[user]<=1.5:
                    recalls_ecc_1_15.append(hits / float(len(list_liked) - len(train_set)))
                if 1.5<user_to_ecc[user]<=2:
                    recalls_ecc_15_2.append(hits / float(len(list_liked) - len(train_set)))
                if 2<user_to_ecc[user]<=2.5:
                    recalls_ecc_2_25.append(hits / float(len(list_liked) - len(train_set)))
                if 2.5<user_to_ecc[user]:
                    recalls_ecc_25.append(hits / float(len(list_liked) - len(train_set)))

        except KeyError as e:
            pass
    print('Recall at all:',k,mean(recalls))
    print('Recall at 0:',k,mean(recalls_ecc_0_05))
    print('Recall at 0.5:',k,mean(recalls_ecc_05_1))
    print('Recall at 1:',k,mean(recalls_ecc_1_15))
    print('Recall at 1.5:',k,mean(recalls_ecc_15_2))
    print('Recall at 2:',k,mean(recalls_ecc_2_25))
    print('Recall at 2.5 and higher:',k,mean(recalls_ecc_25))
    print('That many user:',counts)

def matrixToTrainAndTest(mat,train_split=0.8):
    """
    Splits the train-test set
    :param mat: to split
    :param train_split: percentage of split
    :return: train and test matrix
    """
    train=lil_matrix(mat.shape,dtype=np.bool)
    test=lil_matrix(mat.shape,dtype=np.bool)
    print('split')
    for i in range(mat.shape[0]):
        row=mat.getrow(i).rows[0]
        random.seed=100
        random.shuffle(row)
        til_len=int(len(row)*train_split)
        train_ind=row[:til_len]
        test_ind=row[til_len:]
        for j in train_ind:
            train[i,j]=True
        for j in test_ind:
            test[i,j]=True
    print('end split')
    return train,test

def print_maxes(mat):
    """
    prints variouse informations about the martrix
    :param mat: matrix to print
    """
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
    """
    Creates plots for the run
    :param mat: matrix to analyze
    :param k: amount of items to consider
    """
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
    print("length dict:",len(dict_userid_to_recommends))
    for user in tqdm(to_iter):

        #delete vals which user alreay liked
        list_recommends_not_liked_yet=[[i,j]for i,j in dict_userid_to_recommends[user] if i not in dict_userid_to_moviesliked[user]]
        list_recommends_not_liked_yet=sorted(list_recommends_not_liked_yet, key=itemgetter(1))
        #only take top k
        top_items=list_recommends_not_liked_yet[-20:]
        top_items_ecc=[dict_ecc[item] for item,val in top_items]
        #append ecc vals to plot list
        counter_ignored=0
        if len(top_items_ecc) > 0:
            user_ecc.append(user_to_ecc[user])
            if user_to_ecc[user]>0:
                counter_ecc+=1
            else:
                counter_none_ecc+=1
            user_avg_rec_ecc.append(mean(top_items_ecc))
        else:
            print('ignored')
            counter_ignored+=1
        for i in top_items_ecc:
            top_items_ecc_all.append(i)
        if user==0:
            print(50*"THIS SHOULD NOT HAPPEN\n")
    regr = linear_model.LinearRegression()
    a=np.array(user_ecc).reshape((len(user_ecc),1))
    b=np.array(user_avg_rec_ecc)
    print(a.shape,b.shape)
    user_ecc_np=np.array(user_ecc).reshape((len(user_ecc),1))
    user_avg_rec_ecc_np=np.array(user_avg_rec_ecc)
    print(len(user_ecc_np),len(user_avg_rec_ecc_np))
    print(user_ecc_np.shape,user_avg_rec_ecc_np.shape)
    regr.fit(user_ecc_np, user_avg_rec_ecc_np)
    y_pred = regr.predict(user_ecc_np)
    print(y_pred[:],user_avg_rec_ecc[:10])
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
          % mean_squared_error(user_ecc_np, y_pred))
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(user_avg_rec_ecc_np, y_pred))
    print("Pearson relation:",stats.pearsonr(np.array(user_ecc), np.array(user_avg_rec_ecc)))
    # Plot outputs
    print('Starting to plot:')
    print("ecc users:",counter_ecc)
    print("none ecc users:",counter_none_ecc)
    print("ignored users:",counter_ignored)
    #Now plot box plot of all ecc
    print(user_ecc_np.shape, y_pred.shape)
    plt.scatter(x=user_ecc,y=user_avg_rec_ecc,s=0.3)
    plt.text(-2.9, 1.3, "Mean squared error: %.2f"
          % mean_squared_error(user_avg_rec_ecc_np, y_pred),
            color='black', fontsize=12)
    plt.text(-2.9, 1.6, "Correlation:"+str(stats.pearsonr(np.array(user_ecc), np.array(user_avg_rec_ecc))),
            color='black', fontsize=12)
    plt.plot(user_ecc_np.tolist(), y_pred.tolist(), color='red')

    plt.ylim([-3, +3])
    plt.xlim([-3, +3])
    plt.xlabel("User Eccentricity")
    plt.ylabel("Avg. Item Eccentricity in top-20 recommendations")
    plt.show()
    print('Overall avg ecc of users in box:',mean(user_ecc))
    plt.boxplot(top_items_ecc_all)
    plt.show()

#load data
u_to_likes = load_or_create("/Matrix/UserIdToLikes.matrix", create_matrix_user_likes)
#split into train,test
u_to_likes,test=matrixToTrainAndTest(u_to_likes,0.5)
#Calculate normal similarity
pair_wise_rat=cosine_similarity(u_to_likes.transpose())
#Calculate normal recommendations
recommends=lil_matrix(u_to_likes.dot(pair_wise_rat))
#Calculate Eccentric recommendations
recommends_ecc=create_matrix_item_similarity()
recommends_ecc=u_to_likes.dot(recommends_ecc)
#Mix the matrix using sigmoid weigthed
mat_mixed=mix_matrix_for_ecc_and_none_ecc_with_alpha(recommends_ecc,recommends)
#fore python to reales memory
gc.collect()


print(50*"-")
print('Mixed Results:')
calculateRecallAt(mat_mixed,u_to_likes)
print(50*"-")
print('Normal Results:')
calculateRecallAt(recommends,u_to_likes)
print(50*"-")
print('Creating statistics for mixed:')
generate_statistics_for_recommends(mat_mixed)