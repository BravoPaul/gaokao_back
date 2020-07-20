import pandas as pd


#
# 用户特征
# score_user
# rank_user
# wenli
# province_id

# 学校特征
# sch_id
# batch_id
# major_id
# sch_score_min
# sch_score_max
# sch_score_avg
# score_min_mean
# score_min_std
# score_min_trend
# score_avg_mean
# score_avg_std
# score_avg_trend
# score_max_mean
# score_max_std
# score_max_trend
# sch_enroll_plan
# major_enroll_plan
# rank_min_mean
# rank_min_std
# rank_min_trend
# rank_avg_mean
# rank_avg_std
# rank_avg_trend
# rank_max_mean
# rank_max_std
# rank_max_trend

# sch_major_1_id
# sch_major_1_min_mean
# sch_major_1_min_std
# sch_major_1_min_trend
# sch_major_2_id
# sch_major_2_min_mean
# sch_major_2_min_std
# sch_major_2_min_trend
# sch_major_3_id
# sch_major_3_min_mean
# sch_major_3_min_std
# sch_major_3_min_trend

# major_1_id
# major_1_min_mean
# major_1_min_std
# major_1_min_trend
# major_2_id
# major_2_min_mean
# major_2_min_std
# major_2_min_trend
# major_3_id
# major_3_min_mean
# major_3_min_std
# major_3_min_trend


# python manage.py shell < /Users/kunyue/project_personal/my_project/mysite/gaokao/processor/model.py

class Model(object):

    # 这个模型是为了得到每个大学在当年录取的时候，每个专业的预测分
    def rule_model(self, academic_year='2019'):
        from gaokao.models import School, ModelRuleResult
        import sqlite3
        import pandas as pd
        import numpy
        # Create your connection.
        cnx = sqlite3.connect('db.sqlite3')

        df_sch_major = pd.read_sql_query("SELECT * FROM gaokao_schoolmajor where academic_year=" + academic_year + "",
                                         cnx)

        print('2019学校专业数为：', len(df_sch_major[['school_id', 'enroll_major_id', 'enroll_major_name']].drop_duplicates()))

        df_major_split = pd.read_sql_query("SELECT * FROM gaokao_majorsplit", cnx)
        df_sch_major_score = pd.read_sql_query("SELECT * FROM gaokao_schoolmajorsplit", cnx)

        df_sch_major_score = df_sch_major_score[
            (df_sch_major_score['min_score_diff_mean'] >= 0) &
            (df_sch_major_score['min_score_rank_mean'] >= 0) &
            (df_sch_major_score['min_score_diff_std'] >= 0) &
            (df_sch_major_score['min_score_rank_std'] >= 0) &
            (df_sch_major_score['avg_score_diff_mean'] >= 0) &
            (df_sch_major_score['avg_score_rank_mean'] >= 0) &
            (df_sch_major_score['avg_score_diff_std'] >= 0) &
            (df_sch_major_score['avg_score_rank_std'] >= 0)
            ]

        df_sch_major_split = pd.merge(df_sch_major, df_major_split, left_on='enroll_major_name', right_on='major_name')

        df_sch_major_split_3 = df_sch_major_split[
            ['school_id', 'wenli', 'batch_name', 'province_id', 'enroll_major_name', 'mname', 'enroll_major_id']]
        df_sch_major_split_3 = df_sch_major_split_3[df_sch_major_split_3['mname'].map(lambda x: len(str(x)) >= 1)]
        df_sch_major_split_3['m_level'] = 3

        df_sch_major_split_2 = df_sch_major_split[
            ['school_id', 'wenli', 'batch_name', 'province_id', 'enroll_major_name', 'cname',
             'enroll_major_id']].rename(
            columns={
                'cname': 'mname'
            }
        )
        df_sch_major_split_2 = df_sch_major_split_2[df_sch_major_split_2['mname'].map(lambda x: len(str(x)) >= 1)]
        df_sch_major_split_2['m_level'] = 2

        df_sch_major_split_1 = df_sch_major_split[
            ['school_id', 'wenli', 'batch_name', 'province_id', 'enroll_major_name', 'sname',
             'enroll_major_id']].rename(
            columns={
                'sname': 'mname'
            }
        )
        df_sch_major_split_1 = df_sch_major_split_1[df_sch_major_split_1['mname'].map(lambda x: len(str(x)) >= 1)]
        df_sch_major_split_1['m_level'] = 1

        df_sch_major_split_merge = pd.concat([df_sch_major_split_3, df_sch_major_split_2, df_sch_major_split_1])
        df_sch_major_score = df_sch_major_score[
            ['school_id', 'wenli', 'batch_name', 'province_id', 'mname', 'm_level',
             'min_score_diff_mean',
             'min_score_rank_mean',
             'min_score_diff_std',
             'min_score_rank_std',
             'avg_score_diff_mean',
             'avg_score_rank_mean',
             'avg_score_diff_std',
             'avg_score_rank_std',
             ]]

        # 经过专业分解后，可以处理的数目为： 23522，说明有2000的专业无法分解，之前从来没见过

        df_sch_major_score_merge = pd.merge(df_sch_major_split_merge, df_sch_major_score,
                                            on=['school_id', 'wenli', 'batch_name', 'province_id', 'mname', 'm_level'],
                                            how='left')

        def my_agg_1(x):
            names = {
                'min_score_diff_mean': (x['min_score_diff_mean'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_diff_std': (x['min_score_diff_std'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_rank_mean': (x['min_score_rank_mean'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_rank_std': (x['min_score_rank_std'] * x['weight']).sum() / x['weight'].sum(),
                'avg_score_diff_mean': (x['avg_score_diff_mean'] * x['weight']).sum() / x['weight'].sum(),
                'avg_score_diff_std': (x['avg_score_diff_std'] * x['weight']).sum() / x['weight'].sum(),
                'avg_score_rank_mean': (x['avg_score_rank_mean'] * x['weight']).sum() / x['weight'].sum(),
                'avg_score_rank_std': (x['avg_score_rank_std'] * x['weight']).sum() / x['weight'].sum()
            }
            return pd.Series(names, [
                'min_score_diff_mean',
                'min_score_diff_std',
                'min_score_rank_mean',
                'min_score_rank_std',
                'avg_score_diff_mean',
                'avg_score_diff_std',
                'avg_score_rank_mean',
                'avg_score_rank_std'
            ])

        def my_agg_2(x):
            names = {
                'min_score_diff_mean': (x['min_score_diff_mean'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_diff_std': (x['min_score_diff_std'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_rank_mean': (x['min_score_rank_mean'] * x['weight']).sum() / x['weight'].sum(),
                'min_score_rank_std': (x['min_score_rank_std'] * x['weight']).sum() / x['weight'].sum(),
            }
            return pd.Series(names, [
                'min_score_diff_mean',
                'min_score_diff_std',
                'min_score_rank_mean',
                'min_score_rank_std',
            ])

        def weight_cal(x):
            if x == 3:
                return 0.6
            elif x == 2:
                return 0.3
            else:
                return 0.1

        df_sch_major_score_merge = df_sch_major_score_merge.fillna(-99999)
        print('总数为：',
              len(df_sch_major_score_merge[['school_id', 'enroll_major_id', 'enroll_major_name']].drop_duplicates()))

        # ####### 算法一：有学校有专业

        #

        df_sch_major_score_merge_done = df_sch_major_score_merge[
            df_sch_major_score_merge['min_score_diff_mean'] != -99999]
        print('学校专业拼接为：', len(
            df_sch_major_score_merge_done[['school_id', 'enroll_major_id', 'enroll_major_name']].drop_duplicates()))
        df_sch_major_score_merge_done['weight'] = df_sch_major_score_merge_done['m_level'].map(weight_cal)
        result_merge_grp = df_sch_major_score_merge_done.groupby(
            ['school_id', 'wenli', 'batch_name', 'province_id', 'enroll_major_name', 'enroll_major_id']).apply(
            my_agg_1).reset_index()
        # 写入数据
        list_result = []
        for index, row in result_merge_grp.iterrows():
            kargs = {}
            kargs['enroll_major_id'] = row['enroll_major_id']
            kargs['enroll_major_name'] = row['enroll_major_name']
            kargs['batch_name'] = row['batch_name']
            kargs['wenli'] = row['wenli']
            kargs['province_id'] = row['province_id']
            kargs['min_score_diff_mean'] = row['min_score_diff_mean']
            kargs['min_score_diff_std'] = row['min_score_diff_std']
            kargs['min_score_rank_mean'] = row['min_score_rank_mean']
            kargs['min_score_rank_std'] = row['min_score_rank_std']
            kargs['avg_score_diff_mean'] = row['avg_score_diff_mean']
            kargs['avg_score_diff_std'] = row['avg_score_diff_std']
            kargs['avg_score_rank_mean'] = row['avg_score_rank_mean']
            kargs['avg_score_rank_std'] = row['avg_score_rank_std']
            kargs['type'] = 1
            school = School.objects.get(sch_id=row['school_id'])
            list_result.append(ModelRuleResult(**kargs, school=school))
        ModelRuleResult.objects.bulk_create(list_result)


        # 算法二
        # 有学校有专业处理后的数目为： 16455，剩下的10000不能用学校去join，原因是这些学校之前没有专业平均成绩或者最低成绩，或者专业没见过
        # 这部分的处理方法是拿到他的历年录取最低成绩，然后相关批次大学各专业和最低成绩的分差，把这些分差加到这些学校的最低成绩上。
        df_sch_major_score_merge_undone = df_sch_major_score_merge[
            df_sch_major_score_merge['min_score_diff_mean'] == -99999]

        print('剩余第二算法处理为：', len(
            df_sch_major_score_merge_undone[['school_id', 'enroll_major_id', 'enroll_major_name']].drop_duplicates()))

        # 学校历年录取分数处理
        df_school_score = pd.read_sql_query(
            "SELECT * FROM gaokao_schoolscore where academic_year<" + academic_year + "",
            cnx)
        df_school_score['min_score_diff'] = df_school_score['min_score_diff'].map(int)
        df_school_score['min_score_rank'] = df_school_score['min_score_rank'].map(int)

        # 求专业的平均成绩和标准差
        df_major_score_f1 = df_sch_major_score.groupby([
            'wenli', 'batch_name', 'province_id', 'mname', 'm_level']).agg(['mean', 'std']).reset_index()
        columns_my = []
        for one_col_name in df_major_score_f1.columns:
            if len(one_col_name[1]) > 1:
                columns_my.append(one_col_name[0] + '_' + one_col_name[1] + '_f1')
            else:
                columns_my.append(one_col_name[0])
        df_major_score_f1.columns = columns_my
        # 求学校的平均成绩和标准差
        result_school_score_mean_f3 = df_school_score.groupby(['wenli', 'batch_name', 'province_id'])[
            ['min_score_diff', 'min_score_rank']].agg(['mean', 'std']).reset_index()

        columns_my = []
        for one_col_name in result_school_score_mean_f3.columns:
            if len(one_col_name[1]) > 1:
                columns_my.append(one_col_name[0] + '_' + one_col_name[1] + '_f3')
            else:
                columns_my.append(one_col_name[0])
        result_school_score_mean_f3.columns = columns_my

        result_school_major_score_2 = pd.merge(result_school_score_mean_f3, df_major_score_f1,
                                               on=['wenli', 'batch_name', 'province_id'])
        # 求专业和学校的比例关系，这个是按照文理、批次、省份聚合的，目的是求一个统计的平均值
        result_school_major_score_2['percent_score_diff_mean'] = result_school_major_score_2[
                                                                     'min_score_diff_mean_mean_f1'] / \
                                                                 result_school_major_score_2['min_score_diff_mean_f3']
        result_school_major_score_2['percent_rank_diff_mean'] = result_school_major_score_2[
                                                                    'min_score_rank_mean_mean_f1'] / \
                                                                result_school_major_score_2['min_score_rank_mean_f3']
        result_school_major_score_2['percent_score_diff_std'] = result_school_major_score_2[
                                                                    'min_score_diff_std_std_f1'] / \
                                                                result_school_major_score_2['min_score_diff_std_f3']
        result_school_major_score_2['percent_rank_diff_std'] = result_school_major_score_2[
                                                                   'min_score_rank_std_std_f1'] / \
                                                               result_school_major_score_2['min_score_rank_std_f3']

        # 每个学校平均每年的录取分数
        result_school_score_f2 = df_school_score.groupby(['school_id', 'wenli', 'batch_name', 'province_id'])[
            ['min_score_diff', 'min_score_rank']].agg(['mean', 'std']).reset_index()
        columns_my = []
        for one_col_name in result_school_score_f2.columns:
            if len(one_col_name[1]) > 1:
                columns_my.append(one_col_name[0] + '_' + one_col_name[1])
            else:
                columns_my.append(one_col_name[0])
        result_school_score_f2.columns = columns_my
        tmp_final_1 = pd.merge(df_sch_major_split_merge, result_school_score_f2,
                               on=['school_id', 'wenli', 'batch_name', 'province_id'])

        df_final = pd.merge(tmp_final_1, result_school_major_score_2,
                            on=['wenli', 'batch_name', 'province_id', 'mname', 'm_level'])

        df_final = df_final[
            ['school_id', 'enroll_major_id', 'enroll_major_name', 'wenli', 'batch_name', 'province_id', 'mname',
             'm_level', 'percent_score_diff_mean',
             'percent_rank_diff_mean', 'percent_score_diff_std', 'percent_rank_diff_std',
             'min_score_diff_mean', 'min_score_diff_std', 'min_score_rank_mean',
             'min_score_rank_std']].fillna(-999999)

        df_final['min_score_diff_mean'] = df_final['min_score_diff_mean'] * df_final['percent_score_diff_mean']
        df_final['min_score_diff_std'] = df_final['min_score_diff_std'] * df_final['percent_score_diff_std']
        df_final['min_score_rank_mean'] = df_final['min_score_rank_mean'] * df_final['percent_rank_diff_mean']
        df_final['min_score_rank_std'] = df_final['min_score_rank_std'] * df_final['percent_rank_diff_std']

        df_final['weight'] = df_final['m_level'].map(weight_cal)
        result_final = df_final.groupby(
            ['school_id', 'enroll_major_id', 'enroll_major_name', 'wenli', 'batch_name', 'province_id']).apply(
            my_agg_2).reset_index()
        print('通过算法二处理的数量为：',
              len(result_final[['school_id', 'enroll_major_id', 'enroll_major_name']].drop_duplicates()))

        list_result = []
        # @todo 专业之间的差别是不是太大了
        for index, row in result_final.iterrows():
            kargs = {}
            kargs['enroll_major_id'] = row['enroll_major_id']
            kargs['enroll_major_name'] = row['enroll_major_name']
            kargs['batch_name'] = row['batch_name']
            kargs['wenli'] = row['wenli']
            kargs['province_id'] = row['province_id']
            kargs['min_score_diff_mean'] = row['min_score_diff_mean']
            kargs['min_score_diff_std'] = row['min_score_diff_std']
            kargs['min_score_rank_mean'] = row['min_score_rank_mean']
            kargs['min_score_rank_std'] = row['min_score_rank_std']
            kargs['type'] = 2
            school = School.objects.get(sch_id=row['school_id'])
            list_result.append(ModelRuleResult(**kargs, school=school))
        ModelRuleResult.objects.bulk_create(list_result)


    def fea_generate(self):
        pass

    def evaluate(self):
        # @todo 大学最低分排序和录取概率排序
        # @todo 大学专业录取概率排序和各专业最低分排序
        pass


md = Model()
md.rule_model('2019')
