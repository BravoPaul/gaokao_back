import pandas as pd
import sqlite3
import os
import sys
import matplotlib as mpl

mpl.use('TkAgg')
mpl.rcParams['font.sans-serif'] = ['FangSong']
import matplotlib.pyplot as plt

os.chdir('/Users/kunyue/project_personal/my_project/gaokao_back/gaokao/processor')
cnx = sqlite3.connect('../../db.sqlite3')
cnx_2 = sqlite3.connect('db.sqlite3')
df_sch_major = pd.read_sql_query("SELECT * FROM gaokao_schoolmajor", cnx)
school = pd.read_sql_query("SELECT * FROM gaokao_school", cnx)[['sch_id', 'sch_tags', 'sch_name']]
schoolRank = pd.read_sql_query("SELECT * FROM gaokao_gaokaometarank", cnx)
df_sch_score = pd.read_sql_query("SELECT * FROM gaokao_schoolscore", cnx)

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)


def get_lucky_sch(wenli, batch_name):
    df_trait = df_sch_major[df_sch_major['wenli'] == wenli]
    df_trait = df_trait[df_trait['batch_name'] == batch_name]
    df_trait['min_score_diff'] = df_trait['min_score_diff'].map(int)
    df_trait['min_score_rank'] = df_trait['min_score_rank'].map(int)
    df_trait = df_trait[(df_trait['min_score_diff'] > 0) & (df_trait['min_score_diff'] < 700)]
    df_trait = df_trait[(df_trait['min_score_rank'] > 0) & (df_trait['min_score_rank'] < 1000000)]
    df_detail = df_trait[['school_id', 'academic_year', 'enroll_major_name', 'min_score_diff', 'min_score_rank']]
    df_grp_min = df_trait.groupby(['school_id', 'academic_year']).agg(min_score_diff=('min_score_diff', min),
                                                                      min_score_rank=(
                                                                          'min_score_rank', max)).reset_index()
    df_grp_min = pd.merge(df_grp_min, df_detail, on=['school_id', 'academic_year', 'min_score_diff', 'min_score_rank'])
    df_min_last_year = df_grp_min[df_grp_min['academic_year'] < '2019'].groupby(
        ['school_id', 'academic_year', 'min_score_diff', 'min_score_rank']).head(1)
    df_min_last_year.rename(columns={'min_score_diff': 'last_min_score', 'min_score_rank': 'last_min_rank'},
                            inplace=True)
    df_min_last_year['academic_year'] = df_min_last_year['academic_year'].map(lambda x: str(int(x) + 1))
    df_min_next_year = df_grp_min[df_grp_min['academic_year'] >= '2017']
    df_min_next_year.rename(columns={'min_score_diff': 'next_min_score', 'min_score_rank': 'next_min_rank'},
                            inplace=True)
    df_result = pd.merge(df_min_last_year, df_min_next_year, on=['school_id', 'academic_year'])

    df_major = df_grp_min[df_grp_min['academic_year'] < '2019'][
        ['school_id', 'academic_year', 'enroll_major_name']].drop_duplicates()
    df_major['academic_year'] = df_major['academic_year'].map(lambda x: str(int(x) + 1))
    df_major['major_exist'] = 1

    df_result = pd.merge(df_result, df_major,
                         left_on=['school_id', 'academic_year', 'enroll_major_name_y'],
                         right_on=['school_id', 'academic_year', 'enroll_major_name'], how='left')
    df_result = df_result.fillna(-1)

    df_result['diff_score'] = df_result.apply(
        lambda x: (int(x['last_min_score']) - int(x['next_min_score'])) / int(x['last_min_score']), axis=1)
    df_result['diff_rank'] = df_result.apply(
        lambda x: (int(x['last_min_rank']) - int(x['next_min_rank'])) / int(x['last_min_rank']), axis=1)
    return df_result


def show_result(df):
    school['211'] = school['sch_tags'].map(lambda x: '211' if str(x).find('211') >= 0 else '')
    school['985'] = school['sch_tags'].map(lambda x: '985' if str(x).find('985') >= 0 else '')
    result = pd.merge(school, df, left_on='sch_id', right_on='school_id')
    result = result.drop(['sch_tags', 'sch_id'], axis=1)
    result = result.sort_values(by=['academic_year', 'diff_score'], ascending=False)
    return result


def get_school_rule(wenli, batch_name):
    '''
    录取人数变多，对低分排名近3年逐年升高，即录取分数越来越高
    :return:
    '''
    # 三年上涨幅度每年超过5%
    df_trait = df_sch_major[df_sch_major['wenli'] == wenli]
    df_trait = df_trait[df_trait['batch_name'] == batch_name]
    df_trait['min_score_diff'] = df_trait['min_score_diff'].map(int)
    df_trait['min_score_rank'] = df_trait['min_score_rank'].map(int)
    df_grp_min = df_trait.groupby(['school_id', 'academic_year']).agg(
        min_score_rank=('min_score_rank', max)).reset_index()
    df_grp_min['diff'] = df_grp_min.sort_values(by=['school_id', 'academic_year']).groupby(['school_id'])[
        'min_score_rank'].diff()
    df_grp_min_2019_lt = df_grp_min[df_grp_min['academic_year'] < '2019']
    df_grp_min_2019_lt = df_grp_min_2019_lt.dropna(subset=['diff'])
    df_grp_min_2019_lt['diff_percent'] = df_grp_min_2019_lt['diff'] / df_grp_min_2019_lt['min_score_rank']
    df_grp_min_2019_lt_count = df_grp_min_2019_lt[df_grp_min_2019_lt['diff_percent'] < -0.05].groupby(['school_id'])[
        'diff_percent'].count().reset_index()
    df_grp_min_2019_lt_count_2 = df_grp_min_2019_lt_count[df_grp_min_2019_lt_count['diff_percent'] >= 2]
    return df_grp_min_2019_lt_count_2


def school_enroll_ana(wenli, batch_name):
    df_trait = df_sch_score[df_sch_score['wenli'] == wenli]
    df_trait['min_score_rank'] = df_trait['min_score_rank'].map(int)
    df_trait['min_score_diff'] = df_trait['min_score_diff'].map(int)
    df_trait['min_score'] = df_trait['min_score'].map(int)
    df_trait = df_trait[df_trait['batch_name'] == batch_name]
    df_trait['enroll_plan_count'] = df_trait['enroll_plan_count'].map(int)
    df_trait = df_trait[(df_trait['enroll_plan_count'] >= 0) & df_trait['enroll_plan_count'] <= 1000000]
    df_trait = df_trait.sort_values(by=['school_id', 'academic_year'])
    df_trait['enroll_last'] = df_trait.groupby(['school_id'])['enroll_plan_count'].shift()
    df_trait['min_rank_last'] = df_trait.groupby(['school_id'])['min_score_rank'].shift()
    df_trait = df_trait.dropna(subset=['enroll_last', 'min_rank_last'])
    df_trait['enroll_diff_percent'] = df_trait.apply(
        lambda x: (int(x['enroll_plan_count']) - int(x['enroll_last'])) / int(x['enroll_last']), axis=1)
    df_trait['min_rank_percent'] = df_trait.apply(
        lambda x: (int(x['min_score_rank']) - int(x['min_rank_last'])) / int(x['min_rank_last']), axis=1)
    return df_trait


def plot_rank(wenli, academic_year):
    schoolT = schoolRank[schoolRank['academic_year'] == academic_year]
    schoolT = schoolT[schoolT['wenli'] == wenli]
    schoolT = schoolT.sort_values(by=['score'])
    schoolT = schoolT[schoolT['score'] >= 200]
    schoolT['range'] = pd.cut(schoolT['score'], 100)
    school_grp = schoolT.groupby(['range'])['rank'].sum().reset_index()
    array_x = [i for i in range(len(school_grp['range']))]
    print(school_grp['range'])
    array_y = school_grp['rank'].values
    plot_bar(array_x, array_y)


def plot_min_score(wenli, academic_year):
    df_sch_t = df_sch_major[df_sch_major['academic_year'] == academic_year]
    df_sch_t = df_sch_t[df_sch_t['wenli'] == wenli]
    df_sch_t['min_score'] = df_sch_t['min_score'].map(int)
    df_sch_t = df_sch_t[(df_sch_t['min_score'] > 0) & (df_sch_t['min_score'] < 800)]
    df_sch_t = df_sch_t.groupby(['school_id'])['min_score'].min().reset_index()
    df_sch_grp = df_sch_t.sort_values(by=['min_score'])
    df_sch_grp = df_sch_grp[df_sch_grp['min_score'] >= 200]
    df_sch_grp['range'] = pd.cut(df_sch_grp['min_score'], 100)
    school_grp = df_sch_grp.groupby(['range'])['min_score'].count().reset_index()
    array_x = [i for i in range(len(school_grp['range']))]
    print(school_grp)
    array_y = school_grp['min_score'].values
    plot_bar(array_x[1:], array_y[1:])


def plot_bar(array_x, array_y):
    plt.figure(figsize=(8, 6), dpi=80)
    # 生成第一个子图在1行2列第一列位置
    plt.subplot(1, 1, 1)
    # 生成第二子图在1行2列第二列位置
    # ax2 = fig.add_subplot(122)
    # 绘图并设置柱子宽度0.5
    plt.bar(array_x, array_y, width=0.1)
    # 绘图默认柱子宽度0.8
    plt.show()


def main_plot_rank():
    plot_rank('2', '2019')


def main_plot_min_score():
    plot_min_score('2', '2019')


def main_get_sch_rule():
    result_rule = get_school_rule('2', '本科第一批')
    result_lucky = get_lucky_sch('2', '本科第一批')
    result_lucky = show_result(result_lucky)
    result_analyse = pd.merge(result_lucky, result_rule, on=['school_id'], how='left')
    result_analyse.to_sql('tmp_analyse', con=cnx_2, if_exists='append')


def main_sch_lucky():
    result_lucky = get_lucky_sch('2', '本科第一批')
    result_lucky = show_result(result_lucky)


def main_school_enroll_ana():
    result = school_enroll_ana('2', '本科第一批')
    result = pd.merge(school[['sch_id', 'sch_name']], result, left_on='sch_id', right_on='school_id')
    result.to_sql('main_school_enroll_ana', con=cnx_2, if_exists='replace')


if __name__ == '__main__':
    main_school_enroll_ana()
