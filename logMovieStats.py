def item_names_print(list_ids, dict_names, ecc_dict):
    print(100*'-')
    for item in list_ids:
        print(dict_names[item])
        print("Eccentricicty val:",ecc_dict[item])
        print('https://www.google.ch/search?q='+dict_names[item].replace(' ','+').replace(',','%2C').replace('(','').replace(')','').replace('\'','%27'))
    print(100*'-')