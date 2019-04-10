import pandas as pd
import filesutils as fu

COL_INDIVIDUAL_NAME = 'individual'
COL_ABSTRACT_NAME = 'abstract'
COL_TYPE_NAME = 'type'
COL_NE_TYPE_NAME = 'ne_types'
COL_PREDICTIONS_NAME = 'predictions'
COL_LABELS_NAME = 'labels'
COL_UNSEEN_NAME = 'unseen'


path = "../../../data/results/FULL_merged_types_abstract.csv"


df = fu.csv_to_df(path)


stats = df[COL_TYPE_NAME].value_counts()

print(stats)


max_type = "non"
max_count = -1

for index, row in stats.iterrows():
    print("%s -- %s" % (row[0], row[1]))




#fu.df_to_csv(path+".stats", stats)

# aplicar transformacion de '\n' a ' ' solo a la columna del abstract


#abs_index = df.columns.get_loc(COL_ABSTRACT_NAME) + 1
#ind_index = df.columns.get_loc(COL_INDIVIDUAL_NAME) + 1


#df = df.replace(r'[^\x00-\x7F]+',' ', regex=True)

#df[COL_ABSTRACT_NAME] = df[COL_ABSTRACT_NAME].str.replace('\n','XXXXX', regex=False)

    #("\n|\r",'XXXXXX', regex=True)

    #replace('\r', '').replace('\n', '')

#replace('\n','XXXXXX', regex=False)



#fu.df_to_csv(path+".aplanado_2", df)

#print(df.groupby(COL_TYPE_NAME).count())
