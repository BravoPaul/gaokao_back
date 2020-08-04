import sqlite3
import pandas as pd
import numpy as np

# Create your connection.
cnx = sqlite3.connect('../../db.sqlite3')
df_sch_major = pd.read_sql_query("SELECT * FROM gaokao_schoolmajor", cnx)
school = pd.read_sql_query("SELECT * FROM gaokao_school", cnx)[['sch_id', 'sch_tags', 'sch_name']]
df_sch_major['min_score_rank'] = df_sch_major['min_score_rank'].map(int)
df_sch_major = df_sch_major[df_sch_major['academic_year'] == '2019']
df_sch_major = df_sch_major[df_sch_major['wenli'] == '2']


def get_recall_result(rank):
    min_rank = int(int(rank) - int(rank) * 0.2)
    max_rank = int(int(rank) + int(rank) * 0.2)
    print('召回介于{}名到{}名的大学'.format(min_rank, max_rank))
    sch_down = df_sch_major[df_sch_major['min_score_rank'] >= min_rank]
    sch_up = sch_down[sch_down['min_score_rank'] <= max_rank]
    sch_ids = sch_up[['school_id']].drop_duplicates()
    sch_result = pd.merge(sch_ids, df_sch_major, on=['school_id'])
    sch_min_score = sch_result.groupby(['school_id'])['min_score_rank'].mean().reset_index().rename(
        columns={'min_score_rank': '往年学校平均排名'})
    sch_min_score['往年学校平均排名'] = sch_min_score['往年学校平均排名'].map(int)
    sch_min_score = sch_min_score[sch_min_score['往年学校平均排名'] < int(rank) * 2]
    sch_result = pd.merge(sch_result, sch_min_score, on=['school_id'])[
        ['school_id', 'enroll_major_id', 'enroll_major_name', 'min_score', 'min_score_rank', 'min_score_diff',
         'avg_score', 'avg_score_rank', 'avg_score_diff', '往年学校平均排名']]
    sch_result = sch_result.rename(
        columns={'enroll_major_name': '专业名', 'min_score_rank': '往年专业最低分排名', 'avg_score_rank': '往年专业平均分排名'})
    sch_result['您的排名'] = int(rank)
    return sch_result


def show_schools(df_recall):
    school['211'] = school['sch_tags'].map(lambda x: '211' if str(x).find('211') >= 0 else '')
    school['985'] = school['sch_tags'].map(lambda x: '985' if str(x).find('985') >= 0 else '')

    def recommend(x):
        if (x['您的排名'] - x['往年学校平均排名']) / x['往年学校平均排名'] < -0.1:
            return '保底'
        elif (x['您的排名'] - x['往年学校平均排名']) / x['往年学校平均排名'] > 0.1:
            return '冲刺'
        else:
            return '稳妥'

    result = pd.merge(school, df_recall, left_on='sch_id', right_on='school_id').rename(columns={'sch_name': '学校名'})
    result['报考建议'] = result.apply(recommend, axis=1)
    result = result.sort_values(by=['往年学校平均排名', 'sch_id', '往年专业平均分排名'])
    return result[['学校名', '211', '985', '专业名', '您的排名', '往年学校平均排名', '往年专业最低分排名', '往年专业平均分排名', '报考建议']]


def main():
    while True:
        print('请输入名次:\n')
        rank = input()
        if rank == 'q':
            break
        print('名次为{}名，召回的大学如下：'.format(rank))
        df_recall = get_recall_result(rank)
        result = show_schools(df_recall)
        result.to_excel('../../data/data_result/result_recall' + rank + '.xlsx')


if __name__ == '__main__':
    main()
