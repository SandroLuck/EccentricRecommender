import csv
from operator import itemgetter
import numpy as np
from scipy.stats import zscore

def calculateMovieEccentricityIndex():
    """
    Convert files to movieControversialIndex like/dislike foreach movie
    out a file movieControversialIndex.dat which is format,
    movieid likes/dislikes amountoflikesanddislikes
    also outputs movieRarity.dat with format
    movieid, zscore(-log(amountOfLikesMovie))
    also outputs userEccentricity.dat with format
    user_id, zscore(sum(positive_iteraction_rarity)/amount_positive_interaction)
    also outputs itemEccentricity.dat with format
    movieid, zscore(sum(user_who_liked_eccentricity)/amount_positive_interaction_for_movie)
    :type ratingForLike: specifiy above which rating is considered a like
    """
    with open('userMlAboveAvg.dat', 'r') as uP:
        with open('userMlBelowAvg.dat', 'r') as uN:
            with open('movieRarity.dat', 'w+') as rarity:
                with open('userEccentricity.dat', 'w+') as user_eccentricity_out:
                    with open('itemEccentricity.dat', 'w+') as item_eccentricity_out:
                            # read file into a csv reader
                            readerP = csv.reader(uP, delimiter=" ")
                            tmpP = list(readerP)
                            readerN = csv.reader(uN, delimiter=" ")
                            tmpN = list(readerN)

                            #out_tmp has format id, amountlikes, amountdislikes, amountInteraction
                            out_tmp = [[j,0,0,0] for j in range(131264)]
                            # count all likes for a movie
                            for id,line in enumerate(tmpP):

                                for rat in line[1:]:
                                    out_tmp[int(rat)][0]=int(rat)
                                    out_tmp[int(rat)][1]+=1
                                    out_tmp[int(rat)][3]+=1
                            # count all dislikes
                            for id,line in enumerate(tmpN):
                                for rat in line[1:]:
                                    assert out_tmp[int(rat)][0]==int(rat)
                                    out_tmp[int(rat)][2]+=1
                                    out_tmp[int(rat)][3]+=1

                            problem_count=0
                            # Now also calculate Item Rarity
                            # Item rarity is -log(AmountOfInteractionsOnItem)
                            item_rarity=[[j,0] for j in range(131264)]
                            for item in item_rarity:
                                if out_tmp[item[0]][3]!=0:
                                    item[1]=-np.log(out_tmp[item[0]][3])
                                else:
                                    problem_count+=1
                            #delete all 0 values, 0 interactionsmeans movie should nto exist
                            item_rarity=list(filter(lambda item: item[1] != 0, item_rarity))
                            item_rarity_array=np.asarray(item_rarity)
                            item_rarity_array_fzscore=zscore(item_rarity_array[:,1])
                            item_rarity_array[:,1]=item_rarity_array_fzscore

                            #make item_rarity_dict
                            item_rarity_dict=dict()
                            for item in item_rarity_array:
                                item_rarity_dict[int(item[0])]=item[1]
                            #also add dict values for items which have only one ineraction
                            #problem is log(1)=0 but we discard all 0 values since they only mean not existing
                            for item in out_tmp:
                                if item[3]==1:
                                    item_rarity_dict[int(item[0])]=0
                            #Now calculate user Eccentricity
                            user_eccentricity=[[j,0] for j in range(138495)]
                            for id,line in enumerate(tmpP):
                                assert user_eccentricity[id+1][0]==id+1
                                count_pos_item=0
                                for rat in line[1:]:
                                    user_eccentricity[id+1][1]+=item_rarity_dict[int(rat)]
                                    count_pos_item+=1
                                user_eccentricity[id+1][1] /= count_pos_item
                            #delete all 0 values, 0 interactionsmeans user should nto exist
                            user_eccentricity=list(filter(lambda item: item[1] != 0, user_eccentricity))


                            user_eccentricity_array=np.asarray(user_eccentricity)
                            user_eccentricity_array_fzscore=zscore(user_eccentricity_array[:,1])
                            user_eccentricity_array[:,1]=user_eccentricity_array_fzscore

                            #make user eccentricity dict
                            user_ecc_dict=dict()
                            for item in user_eccentricity_array:
                                user_ecc_dict[int(item[0])]=item[1]

                            #Now finally calculate item_eccentricity
                            #first calculate sum of eccentric users who liked
                            item_eccentricity=[[j,0] for j in range(131264)]
                            for id,line in enumerate(tmpP):
                                for rat in line[1:]:
                                    item_eccentricity[int(rat)][1]+=user_ecc_dict[id+1]
                            # divide by user amount who liked
                            for item in item_eccentricity:
                                assert item[0]==out_tmp[int(item[0])][0]
                                if out_tmp[int(item[0])][1]!=0:
                                    item[1]/=out_tmp[int(item[0])][1]
                                else:
                                    item[1]=0
                            # delete all 0 values, 0 interactionsmeans user should nto exist
                            item_eccentricity = list(filter(lambda item: item[1] != 0, item_eccentricity))

                            item_eccentricity_array=np.asarray(item_eccentricity)
                            item_eccentricity_array_fzscore=zscore(item_eccentricity_array[:,1])
                            item_eccentricity_array[:,1]=item_eccentricity_array_fzscore

                            for item in item_eccentricity_array:
                                item_eccentricity_out.write(str(int(item[0]))+" "+str(item[1])+"\n")

                            for item in user_eccentricity_array:
                                user_eccentricity_out.write(str(int(item[0]))+" "+str(item[1])+"\n")
                            #output rarity
                            for item in item_rarity_array:
                                rarity.write(str(int(item[0]))+" "+str(item[1])+"\n")
calculateMovieEccentricityIndex()