from scipy.sparse import lil_matrix,save_npz
import numpy as np
from CreateDicts import createDictUserIdToUserEccentricity, createDictMovieIdToUsersWhoLiked,create_dict_names,create_dict_ecc

def CreateUserRatingLilMatrix():

