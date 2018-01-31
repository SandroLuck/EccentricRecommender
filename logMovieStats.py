def item_names_print(list_ids, dict_names, ecc_dict):
    """
    Print the item names and google links given a item id list,
    might give strange results if dict is not correct the dataset
    :param list_ids:
    :param dict_names:
    :param ecc_dict:
    """
    print(100*'-')
    for item in list_ids:
        print(dict_names[item])
        print("Eccentricicty val:",ecc_dict[item])
        print('https://www.google.ch/search?q='+dict_names[item].replace(' ','+').replace(',','%2C').replace('(','').replace(')','').replace('\'','%27'))
    print(100*'-')