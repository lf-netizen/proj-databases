import numpy as np
import pandas as pd
from typing import List
import re

class FBT:
    df: pd.DataFrame
    threshold: float

    def __init__(self,df,threshold=0.4) -> None:
        self.df = df
        self.threshold = threshold
        pass

    def get_reccomendation(self,already_in:List):
        dicts = []
        for id in already_in:
            dicts.append(self.__top_keys(self.__count_occurrences(id,already_in),top_num=6))
        return self.__top_n(dicts,top_num=6)

    def __count_occurrences(self,input_value, already_in = []):
        ex = self.df[self.df.apply(lambda row: input_value in row.values[1], axis=1)]
        counts = {}
        for index, _ in enumerate(ex.iterrows()):
            for item in [re.sub( r"['\[\]]",'',item) for item in ex.iloc[index].values[1].split(", ")]:
                if item != input_value and item not in already_in and type(item) != int and type(item) != np.nan:
                    if item in counts:
                        counts[item] += 1
                    else:
                        counts[item] = 1
                        
        for key, value in counts.items():
            counts[key] = value / len(ex)
        return counts

    def __top_keys(self,dictionary, top_num=6):
        sorted_items = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_items[:top_num])

    def __top_n(self,dict_list, top_num=6):
        summed_dict = {}
        for dictionary in dict_list:
            for key, value in dictionary.items():
                if key in summed_dict:
                    summed_dict[key] += value
                else:
                    summed_dict[key] = value
        sorted_items = sorted(summed_dict.items(), key=lambda item: item[1], reverse=True)
        top_n_items = dict(sorted_items[:top_num]) 
        final_dict = top_n_items.copy()
        for key,val in top_n_items.items():
            if val < self.threshold:
                del(final_dict[key])
        return final_dict