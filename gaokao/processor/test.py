import sqlite3
import pandas as pd
import numpy as np


# Create your connection.
cnx = sqlite3.connect('../../db.sqlite3')
df_sch_major = pd.read_sql_query("SELECT * FROM gaokao_schoolmajor", cnx)
school = pd.read_sql_query("SELECT * FROM gaokao_school", cnx)[['sch_id', 'sch_name']]


def get_recall_result(rank):
    df_sch_major['min_score_rank'] = df_sch_major['min_score_rank'].map(int)
    min_rank = int(int(rank) - int(rank) * 0.1)
    max_rank = int(int(rank) + int(rank) * 0.1)
    print('召回介于{}名到{}名的大学'.format(min_rank, max_rank))
    sch_down = df_sch_major[df_sch_major['min_score_rank'] >= min_rank]
    sch_up = sch_down[sch_down['min_score_rank'] <= max_rank]
    return sch_up[['school_id', 'enroll_major_id', 'enroll_major_name', 'min_score', 'min_score_rank', 'min_score_diff',
                   'avg_score', 'avg_score_rank', 'avg_score_diff']]


def show_schools(df_recall):
    result = pd.merge(school, df_recall, left_on='sch_id', right_on='school_id')
    result = result.sort_values(by=['avg_score_rank'])
    return result


def main():
    while True:
        print('请输入名次:\n')
        rank = input()
        if rank=='q':
            break
        print('名次为{}名，召回的大学如下：'.format(rank))
        df_recall = get_recall_result(rank)
        result = show_schools(df_recall)
        del result['sch_id']
        del result['school_id']
        del result['enroll_major_id']
        result.to_excel('../../data/data_result/result_recall'+rank+'.xlsx')


if __name__ == '__main__':
    main()
