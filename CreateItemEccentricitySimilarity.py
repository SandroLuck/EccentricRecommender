import csv
import numpy as np
from scipy.sparse import lil_matrix
from tqdm import tqdm
from operator import itemgetter


def CreatItemEccentricitySimilarity(threshold_EUS=0.1):
    with open('userSimilarityEccentricityAndSet.dat','r') as f:

        print('STARTING')
        reader = csv.reader(f, delimiter=",")
        in_data = list(reader)
        ecc_and_list=list()
        #find max movie id first
        # i is USE and j is movies in set
        print("CONVERTING DATA")
        for i in tqdm(in_data):
            tmp_list=list()
            for j in i[1:]:
                tmp=int(j.replace('[','').replace(']',''))
                tmp_list.append(tmp)
            ecc_and_list.append([float(i[0]),tmp_list])
        print("Finding Max")
        max_id=max(int(item_id) for user_pair in ecc_and_list for item_id in user_pair[1])
        print(max_id)
        item_similarity_matrix=lil_matrix((max_id+1,max_id+1),dtype=np.float)
        print("DOING MATRIX")
        skipped_count=0
        for user_pair in tqdm(ecc_and_list):
            #care about threshold such that only somewhat eccentric users are considered
            if user_pair[0]>=threshold_EUS:
                for index,m1_id in enumerate(user_pair[1]):
                    for m2_id in user_pair[1][index:]:
                        item_similarity_matrix[m1_id,m2_id]+=user_pair[0]
            else:
                skipped_count+=1
        print("MATRIX DONE")
        print("WE skipped:",skipped_count)
        print("OF:",len(ecc_and_list))
        print("Means we considered in percentage :",1-skipped_count/len(ecc_and_list))
        print("Means we considered exactly:",len(ecc_and_list)-skipped_count)
        toc_format =item_similarity_matrix.tocoo()

        max_val_index = toc_format.data.argmax()
        maxrow = toc_format.row[max_val_index]
        maxcol = toc_format.col[max_val_index]

        # These are the non-zero entries of the matrix
        ecc_item_sim=item_similarity_matrix.nonzero()
        i,j=ecc_item_sim
        #iterate over lil_matrix entries, which are nonzero
        list_item_similarities=list()
        print("STARTING TO SORT")
        for index_list,index_matrix in tqdm(enumerate(i)):
            # if the index is not on the diagonal we calculate
            val_i_i_diag = (item_similarity_matrix[i[index_list], i[index_list]])
            val_j_j_diag = (item_similarity_matrix[j[index_list], j[index_list]])
            # if also the movies are not exactly equally often viewed since this mostly means they are only in one data set
            if i[index_list]!=j[index_list] and val_j_j_diag!=val_i_i_diag:
                val_to_sort=item_similarity_matrix[i[index_list],j[index_list]]

                diff_abs=abs(val_i_i_diag-val_j_j_diag)
                list_item_similarities.append([i[index_list],j[index_list],(val_i_i_diag+val_j_j_diag)/val_to_sort, val_to_sort, val_i_i_diag, val_j_j_diag])
        list_item_similarities=sorted(list_item_similarities, key=itemgetter(3))
        #list_item_similarities=[i for i in list_item_similarities if i[2]!=2]
        #Now print the top movies
        dict_names=create_dict_names()
        ecc_dict=create_dict_ecc()
        print("WE'll out put this many movie pairs:",len(list_item_similarities))
        with open('testFile.txt','w+') as test_out:
            for item in list_item_similarities:
                item_names_print([item[0],item[1]],dict_names,ecc_dict)
                #print("AND THEIR VALUE IS:",item[2])
                #print("intersection of them is:",item[3])
                #print("i i diag is:",item[4])
                #print("j j diag is:",item[5])
                test_out.write(str(item[3])+","+str(item[4])+","+str(item[5])+"\n")

def create_dict_names():
    with open('movies.csv','r', encoding='utf-8') as item_names:
        reader = csv.reader(item_names, delimiter=",")
        item_names = list(reader)
        dict_names = dict()
        for item in item_names[1:]:
            try:
                dict_names[int(item[0])] = item[1]
            except:
                print(item)
                dict_names[int(item[0])] = 'THISnameHadError'
        return dict_names

def create_dict_ecc():
    with open('itemEccentricity.dat', 'r') as IE:
        reader = csv.reader(IE, delimiter=" ")
        item_eccentricity = list(reader)
        item_ecc_dict = dict()
        for item in item_eccentricity:
            item_ecc_dict[int(item[0])] = float(item[1])
    return item_ecc_dict

def item_names_print(list_ids, dict_names, ecc_dict):
    print(100*'-')
    for item in list_ids:
        print(dict_names[item])
        print("Eccentricicty val:",ecc_dict[item])
        print('https://www.google.ch/search?q='+dict_names[item].replace(' ','+').replace(',','%2C').replace('(','').replace(')','').replace('\'','%27'))
    print(100*'-')

CreatItemEccentricitySimilarity()