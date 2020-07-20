import sqlite3
import pandas as pd
import numpy as np


# Create your connection.
cnx = sqlite3.connect('db.sqlite3')

df_sch_major = pd.read_sql_query("SELECT * FROM gaokao_modelruleresult",cnx)

r1 = df_sch_major.groupby(['province_id', 'batch_name', 'wenli'])[
    ['min_score_diff_std', 'min_score_rank_std', 'avg_score_diff_std', 'avg_score_rank_std','type']].median()


r2 = df_sch_major[df_sch_major['min_score_diff_std']!=0].groupby(['province_id', 'batch_name', 'wenli'])[
    ['min_score_diff_std', 'min_score_rank_std', 'avg_score_diff_std', 'avg_score_rank_std','type']].agg(pd.Series.mode)


r3 = df_sch_major.groupby(['province_id', 'batch_name', 'wenli'])[
    ['min_score_diff_std', 'min_score_rank_std', 'avg_score_diff_std', 'avg_score_rank_std','type']].mean()


print(r1)
print(r2)
print(r3)