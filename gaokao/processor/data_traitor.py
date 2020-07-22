# update sqlite_sequence set seq = 0 where name = 'gaokao_schooldetail';
# delete from sqlite_sequence where name = 'gaokao_schooldetail';
# delete from sqlite_sequence;

# python manage.py shell < /Users/kunyue/project_personal/my_project/mysite/gaokao/processor/data_traitor.py


class DataTraitor(object):
    def __init__(self):
        import sqlite3
        import os
        print(os.getcwd())
        self.basic_path = 'data/data_spider/'
        self.conn = sqlite3.connect("../../db.sqlite3")
        self.cur = self.conn.cursor()

    def university_save_sqlite(self):
        import pickle
        from gaokao.models import School
        data_origin = pickle.load(open(self.basic_path + 'university.pkl', "rb"))
        print('正在执行')
        for sch in data_origin:
            new_education = School(**sch)
            new_education.save()

    def university_detail_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolRank, SchoolDetail, SchoolFamous
        data_origin = pickle.load(open(self.basic_path + 'spider_all_university_detail.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            sch_id = sch_detail['sch_id']
            detail_kargs = {}
            result_detail = sch_detail['result']
            detail_kargs['canteen_desc'] = result_detail['sch_detail_info']['canteen_desc']
            detail_kargs['sch_address'] = result_detail['sch_detail_info']['sch_address']
            detail_kargs['sch_fellowship'] = result_detail['sch_detail_info']['sch_fellowship']
            detail_kargs['sch_intro'] = result_detail['sch_detail_info']['sch_intro']
            detail_kargs['sch_scholarship'] = result_detail['sch_detail_info']['sch_scholarship']
            detail_kargs['sch_tel_num'] = result_detail['sch_detail_info']['sch_tel_num']
            detail_kargs['sch_web_url'] = result_detail['sch_detail_info']['sch_web_url']
            detail_kargs['stu_dorm_desc'] = result_detail['sch_detail_info']['stu_dorm_desc']
            detail_kargs['sch_master_ratio'] = result_detail['sch_detail_info']['sch_master_ratio']
            detail_kargs['sch_abroad_ratio'] = result_detail['sch_detail_info']['sch_abroad_ratio']
            school = School.objects.get(sch_id=sch_id)
            SchoolDetail.objects.create(**detail_kargs, school=school)

            if result_detail['sch_rank_info'] is not None:
                for sch_rank in result_detail['sch_rank_info']:
                    rank_kargs = {}
                    rank_kargs['rank_type_desc'] = sch_rank['rank_type_desc']
                    rank_kargs['rank_year'] = sch_rank['rank_year']
                    rank_kargs['rank_idx'] = sch_rank['rank_idx']
                    rank_kargs['rank_score'] = sch_rank['rank_score']
                    rank_kargs['rank_type'] = sch_rank['rank_type']
                    rank_kargs['world_rank_idx'] = sch_rank['world_rank_idx']
                    school = School.objects.get(sch_id=sch_id)
                    SchoolRank.objects.create(**rank_kargs, school=school)

            if result_detail['sch_celebrity_info'] is not None:
                for sch_celebrity in result_detail['sch_celebrity_info']:
                    celebrity_kargs = {}
                    celebrity_kargs['celebrity_name'] = sch_celebrity['celebrity_name']
                    celebrity_kargs['celebrity_desc'] = sch_celebrity['celebrity_desc']
                    school = School.objects.get(sch_id=sch_id)
                    SchoolFamous.objects.create(**celebrity_kargs, school=school)

    def university_score_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolScore
        data_origin = pickle.load(open(self.basic_path + 'spider_all_school_score.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            try:
                result_detail = sch_detail['result']
                if result_detail is not None:
                    for one_result in result_detail:
                        sch_id = one_result['sch_id']
                        true_data = one_result['enroll_info_list']
                        for one_true_data in true_data:
                            data_kargs = {}
                            data_kargs['academic_year'] = one_true_data['academic_year']
                            data_kargs['wenli'] = one_true_data['wenli']
                            data_kargs['batch'] = one_true_data['batch']
                            data_kargs['batch_name'] = one_true_data['batch_name']
                            data_kargs['diploma_id'] = one_true_data['diploma_id']
                            data_kargs['province_id'] = '13'
                            data_kargs['admission_count'] = one_true_data['admission_count']
                            data_kargs['enroll_plan_count'] = one_true_data['enroll_plan_count']
                            data_kargs['max_score'] = one_true_data['max_score']
                            data_kargs['max_score_diff'] = one_true_data['max_score_diff']
                            data_kargs['max_score_equal'] = one_true_data['max_score_equal']
                            data_kargs['max_score_rank'] = one_true_data['max_score_rank']
                            data_kargs['min_score'] = one_true_data['min_score']
                            data_kargs['min_score_diff'] = one_true_data['min_score_diff']
                            data_kargs['min_score_equal'] = one_true_data['min_score_equal']
                            data_kargs['min_score_rank'] = one_true_data['min_score_rank']
                            data_kargs['avg_score'] = one_true_data['avg_score']
                            data_kargs['avg_score_diff'] = one_true_data['avg_score_diff']
                            data_kargs['avg_score_equal'] = one_true_data['avg_score_equal']
                            data_kargs['avg_score_rank'] = one_true_data['avg_score_rank']
                            school = School.objects.get(sch_id=sch_id)
                            SchoolScore.objects.create(**data_kargs, school=school)
            except KeyError:
                continue

    def university_major_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolMajor
        data_origin = pickle.load(open(self.basic_path + 'spider_all_major_score.pkl', "rb"))
        print('正在执行')
        for sch_detail in data_origin:
            try:
                data_kargs = {}
                sch_id = sch_detail['sch_id']
                data_kargs['wenli'] = sch_detail['wenli']
                data_kargs['academic_year'] = sch_detail['academic_year']
                data_kargs['batch'] = sch_detail['batch']
                data_kargs['batch_name'] = sch_detail['batch_name']
                data_kargs['diploma_id'] = sch_detail['diploma_id']
                data_kargs['province_id'] = '13'
                result_detail = sch_detail['result']
                if result_detail is not None and type(result_detail) is list:
                    for one_result in result_detail:
                        data_kargs['academic_rule'] = one_result['academic_rule']
                        data_kargs['admission_count'] = one_result['admission_count']
                        data_kargs['avg_score'] = one_result['avg_score']
                        data_kargs['avg_score_diff'] = one_result['avg_score_diff']
                        data_kargs['avg_score_rank'] = one_result['avg_score_rank']
                        data_kargs['enroll_major_code'] = one_result['enroll_major_code']
                        data_kargs['enroll_major_id'] = one_result['enroll_major_id']
                        data_kargs['enroll_major_name'] = one_result['enroll_major_name']
                        data_kargs['enroll_plan_count'] = one_result['enroll_plan_count']
                        data_kargs['max_score'] = one_result['max_score']
                        data_kargs['max_score_diff'] = one_result['max_score_diff']
                        data_kargs['max_score_rank'] = one_result['max_score_rank']
                        data_kargs['min_score'] = one_result['min_score']
                        data_kargs['min_score_diff'] = one_result['min_score_diff']
                        data_kargs['min_score_rank'] = one_result['min_score_rank']
                        data_kargs['tuition'] = one_result['tuition']
                        school = School.objects.get(sch_id=sch_id)
                        SchoolMajor.objects.create(**data_kargs, school=school)
            except KeyError:
                continue

    def university_schoollist_sqlite(self):
        import pickle
        from gaokao.models import School, SchoolList, SchoolScore
        print('正在执行')
        tags = ['985', '211', '双一流', '研究生点', '民办高校', '公立大学']
        score_tags = ['本科第一批', '本科第二批', '高职专科批']
        locates_top = ['北京', '上海', '广州', '深圳']
        locates_deux = ['成都市'
            , '杭州市'
            , '武汉市'
            , '西安市'
            , '苏州市'
            , '南京市'
            , '长沙市'
            , '郑州市'
            , '东莞市'
            , '青岛市'
            , '沈阳市'
            , '宁波市'
            , '昆明市'
            , '天津市'
            , '重庆市']
        locates = [
            '北京',
            '上海',
            '天津',
            '重庆',
            '广东',
            '河北',
            '辽宁',
            '吉林',
            '黑龙江',
            '山东',
            '江苏',
            '浙江',
            '安徽',
            '福建',
            '江西',
            '广西',
            '海南',
            '河南',
            '湖南',
            '湖北',
            '山西',
            '内蒙古',
            '宁夏',
            '青海',
            '陕西',
            '甘肃',
            '新疆',
            '四川',
            '贵州',
            '云南',
            '西藏',
            '香港',
            '澳门',
            '台湾']

        all_school = School.objects.all()
        for sch in all_school:
            for tag in tags:
                data_kargs = {}
                if sch.sch_tags.find(tag) >= 0:
                    data_kargs['condition'] = tag
                    school = School.objects.get(sch_id=sch.sch_id)
                    SchoolList.objects.create(**data_kargs, school=school)
            for loc in locates:
                data_kargs = {}
                if sch.province.find(loc) >= 0:
                    data_kargs['condition'] = loc
                    school = School.objects.get(sch_id=sch.sch_id)
                    SchoolList.objects.create(**data_kargs, school=school)

            for loc_x in locates_top:
                data_kargs = {}
                if sch.location.find(loc_x) >= 0:
                    data_kargs['condition'] = '一线城市'
                    school = School.objects.get(sch_id=sch.sch_id)
                    SchoolList.objects.create(**data_kargs, school=school)

            for loc_x2 in locates_deux:
                data_kargs = {}
                if sch.location.find(loc_x2) >= 0:
                    data_kargs['condition'] = '新一线城市'
                    school = School.objects.get(sch_id=sch.sch_id)
                    SchoolList.objects.create(**data_kargs, school=school)

        all_school = SchoolScore.objects.all()
        for score_tag in score_tags:
            tmp_schs = set()
            for sch in all_school:
                if sch.batch_name.find(score_tag) >= 0:
                    tmp_schs.add(sch.school_id)
            for sch_id in tmp_schs:
                data_kargs = {}
                data_kargs['condition'] = score_tag
                school = School.objects.get(sch_id=sch_id)
                SchoolList.objects.create(**data_kargs, school=school)

    def gaokao_meta_rank(self):
        # province
        # academic_year
        # wenli
        # score
        # rank
        # rank_cum
        from gaokao.models import GaokaoMetaRank
        import pandas as pd
        from os import walk
        import re
        import math

        dataframe_list = {}
        # walk会返回3个参数，分别是路径，目录list，文件list，你可以按需修改下
        for f, _, i in walk('data/score_rank'):
            for j in i:
                if j.find('2016') >= 0:
                    dataframe_list['2016'] = pd.read_excel(f + '/' + j)
                elif j.find('2017') >= 0:
                    dataframe_list['2017'] = pd.read_excel(f + '/' + j)
                elif j.find('2018') >= 0:
                    dataframe_list['2018'] = pd.read_excel(f + '/' + j)
                elif j.find('2019') >= 0:
                    dataframe_list['2019'] = pd.read_excel(f + '/' + j)

        for key, one_data in dataframe_list.items():
            for index, row in one_data.iterrows():
                data_args_1 = {}
                try:
                    score_tmp = int(row['score'])
                except ValueError:
                    score_tmp = int(re.findall('\d+', str(row['score']))[0])

                data_args_1['score'] = score_tmp
                data_args_1['province_id'] = '13'
                data_args_1['academic_year'] = key
                data_args_1['province'] = '河北'
                data_args_1['wenli'] = 1
                data_args_1['rank'] = 0 if math.isnan(row['rank_wk']) else row['rank_wk']
                data_args_1['rank_cum'] = 0 if math.isnan(row['rank_wk_cum']) else row['rank_wk_cum']

                new_education = GaokaoMetaRank(**data_args_1)
                new_education.save()

                data_args_1['score'] = score_tmp
                data_args_1['province_id'] = '13'
                data_args_1['academic_year'] = key
                data_args_1['province'] = '河北'
                data_args_1['wenli'] = 2
                data_args_1['rank'] = 0 if math.isnan(row['rank_lk']) else row['rank_lk']
                data_args_1['rank_cum'] = 0 if math.isnan(row['rank_lk_cum']) else row['rank_lk_cum']

                new_education = GaokaoMetaRank(**data_args_1)
                new_education.save()

    def gaokao_score_line(self):
        from gaokao.models import GaokaoMetaScoreLine, SchoolScore
        province_condition = ['河北']
        wenli_condition = ['1', '2']
        batch_condition = ['本科第一批', '本科第二批', '高职专科批']
        academic_year = ['2016', '2017', '2018', '2019']
        for one_province in province_condition:
            for one_wenli in wenli_condition:
                for one_batch in batch_condition:
                    for one_year in academic_year:
                        school_score = SchoolScore.objects.filter(academic_year=one_year,
                                                                  wenli=one_wenli,
                                                                  batch_name=one_batch)
                        data_args_1 = {}
                        data_args_1['province_id'] = '13'
                        data_args_1['province'] = one_province
                        data_args_1['wenli'] = one_wenli
                        data_args_1['batch_name'] = one_batch
                        data_args_1['academic_year'] = one_year
                        data_args_1['school_line'] = int(school_score[0].min_score) - int(
                            school_score[0].min_score_diff)
                        new_education = GaokaoMetaScoreLine(**data_args_1)
                        new_education.save()

    def gaokao_recall_score(self):
        from gaokao.models import SchoolScore, GaokaoRecallScore, GaokaoRecallRank
        import pandas as pd

        province_condition = ['河北']
        wenli_condition = ['1', '2']
        batch_condition = ['本科第一批', '本科第二批', '高职专科批']

        for one_province in province_condition:
            for one_wenli in wenli_condition:
                for one_batch in batch_condition:
                    sch_id = []
                    academic_year = []
                    max_score_diff = []
                    min_score_diff = []
                    avg_score_diff = []
                    max_score_rank = []
                    min_score_rank = []
                    avg_score_rank = []
                    school_score = SchoolScore.objects.all()
                    for one_school in school_score:
                        if one_school.wenli == one_wenli and one_school.batch_name == one_batch:
                            sch_id.append(one_school.school_id)
                            academic_year.append(one_school.academic_year)
                            max_score_diff.append(
                                -1 if (int(one_school.max_score_diff) < 0 or int(
                                    one_school.max_score_diff) > 750) else int(one_school.max_score_diff))
                            min_score_diff.append(
                                -1 if (int(one_school.min_score_diff) < 0 or int(
                                    one_school.min_score_diff) > 750) else int(one_school.min_score_diff))
                            avg_score_diff.append(
                                -1 if (int(one_school.avg_score_diff) < 0 or int(
                                    one_school.avg_score_diff) > 750) else int(one_school.avg_score_diff))
                            max_score_rank.append(
                                -1 if (int(one_school.max_score_rank) < 0 or int(
                                    one_school.max_score_rank) > 750) else int(one_school.max_score_rank))
                            min_score_rank.append(
                                -1 if (int(one_school.min_score_rank) < 0 or int(
                                    one_school.min_score_rank) > 750) else int(one_school.min_score_rank))
                            avg_score_rank.append(
                                -1 if (int(one_school.avg_score_rank) < 0 or int(
                                    one_school.avg_score_rank) > 750) else int(one_school.avg_score_rank))

                    data_o = pd.DataFrame.from_dict({
                        'sch_id': sch_id,
                        'academic_year': academic_year,
                        'max_score_diff': max_score_diff,
                        'min_score_diff': min_score_diff,
                        'avg_score_diff': avg_score_diff,
                        'max_score_rank': max_score_rank,
                        'min_score_rank': min_score_rank,
                        'avg_score_rank': avg_score_rank
                    })
                    data_t = data_o[data_o['academic_year'] != '2019']
                    data_t = data_t[data_t['max_score_diff'] != -1]
                    data_t = data_t[data_t['min_score_diff'] != -1]
                    data_t = data_t[data_t['avg_score_diff'] != -1]

                    data_grp_1 = data_t.groupby(['sch_id']).agg(
                        {'max_score_diff': ['max', 'std'], 'avg_score_diff': ['mean'], 'min_score_diff': ['min',
                                                                                                          'std']}).reset_index()
                    df_max = data_grp_1[['sch_id', 'max_score_diff', 'avg_score_diff']].droplevel(0, axis=1).rename(
                        columns={'': 'sch_id'}).sort_values(by=['mean'], ascending=False)
                    df_min = data_grp_1[['sch_id', 'min_score_diff', 'avg_score_diff']].droplevel(0, axis=1).rename(
                        columns={'': 'sch_id'}).sort_values(by=['mean'])

                    for score in range(0, 600):
                        sch_max = df_max[df_max['max'] < score]['sch_id'].values.tolist()
                        sch_min = df_min[df_min['min'] > score]['sch_id'].values.tolist()
                        all_school = set(df_max['sch_id'].values.tolist())
                        if len(sch_max) == len(all_school):
                            break
                        sch_predict_list = list(all_school - set(sch_max) - set(sch_min))
                        sch_predict = df_max[df_max['sch_id'].map(lambda x: x in sch_predict_list)][
                            'sch_id'].values.tolist()

                        data_args = {}
                        data_args['province_id'] = '13'
                        data_args['province'] = one_province
                        data_args['wenli'] = one_wenli
                        data_args['batch_name'] = one_batch
                        data_args['score'] = score
                        data_args['school_win'] = ','.join(sch_max)
                        data_args['school_lose'] = ','.join(sch_min)
                        data_args['school_predict'] = ','.join(sch_predict)

                        new_education = GaokaoRecallScore(**data_args)
                        new_education.save()

                    data_grp_1 = data_t.groupby(['sch_id']).agg(
                        {'max_score_rank': ['min', 'std'], 'avg_score_rank': ['mean'],
                         'min_score_rank': ['max', 'std']}).reset_index()
                    df_max = data_grp_1[['sch_id', 'max_score_rank', 'avg_score_rank']].droplevel(0, axis=1).rename(
                        columns={'': 'sch_id'}).sort_values(by=['mean'], ascending=False)
                    df_min = data_grp_1[['sch_id', 'min_score_rank', 'avg_score_rank']].droplevel(0, axis=1).rename(
                        columns={'': 'sch_id'}).sort_values(by=['mean'])

                    for rank in set(df_max['min'].values.tolist()):
                        sch_max = df_max[df_max['min'] >= rank]['sch_id'].values.tolist()
                        sch_min = df_min[df_min['max'] < rank]['sch_id'].values.tolist()
                        all_school = set(df_max['sch_id'].values.tolist())
                        sch_predict_list = list(all_school - set(sch_max) - set(sch_min))
                        sch_predict = df_max[df_max['sch_id'].map(lambda x: x in sch_predict_list)][
                            'sch_id'].values.tolist()

                        data_args = {}
                        data_args['province_id'] = '13'
                        data_args['province'] = one_province
                        data_args['wenli'] = one_wenli
                        data_args['batch_name'] = one_batch
                        data_args['rank'] = rank
                        data_args['school_win'] = ','.join(sch_max)
                        data_args['school_lose'] = ','.join(sch_min)
                        data_args['school_predict'] = ','.join(sch_predict)

                        new_education = GaokaoRecallRank(**data_args)
                        new_education.save()

    def major_career_detail(self):
        from gaokao.models import Major, Career
        import pickle
        data_origin = pickle.load(open(self.basic_path + 'spider_all_major_detail.pkl', "rb"))
        print('正在执行')
        for major_detail in data_origin:
            kargs = {}

            kargs['mid'] = major_detail['mid']
            kargs['mname'] = major_detail['mname']
            kargs['cid'] = major_detail['cid']
            kargs['cname'] = major_detail['cname']
            kargs['sid'] = major_detail['sid']
            kargs['sname'] = major_detail['sname']
            kargs['academic_rule'] = major_detail['academic_rule']
            kargs['degree'] = major_detail['degree']
            kargs['diploma_id'] = major_detail['diploma_id']
            kargs['logo_url'] = major_detail['logo_url']
            kargs['major_tags'] = major_detail['major_tags']
            kargs['major_type'] = major_detail['major_type']
            kargs['employment_info'] = major_detail['employment_info']
            kargs['intro'] = major_detail['intro']
            kargs['knowledge_requirement'] = major_detail['knowledge_requirement']
            kargs['main_course'] = major_detail['main_course']
            kargs['teaching_practice'] = major_detail['teaching_practice']
            kargs['training_objective'] = major_detail['training_objective']
            kargs['training_requirement'] = major_detail['training_requirement']

            career_tmp = []
            if major_detail['careers'] is not None:
                for one_career in major_detail['careers']:
                    kargs_c = {}
                    kargs_c['cid'] = one_career['id']
                    kargs_c['name'] = one_career['name']
                    kargs_c['desc'] = one_career['desc']
                    Career(**kargs_c).save()
                    career_tmp.append(one_career['id'])

            kargs['careers'] = ','.join(career_tmp)
            new_education = Major(**kargs)
            new_education.save()

    def major_split(self):
        from gaokao.models import MajorSplit, Major, SchoolMajor
        import pandas as pd

        all_sch_major = SchoolMajor.objects.all()
        l_sch_majoir_name = list()
        l_sch_majoir_id = list()
        for one_sch_major in all_sch_major:
            name_tmp = one_sch_major.enroll_major_name
            id_tmp = one_sch_major.enroll_major_id
            if name_tmp not in l_sch_majoir_name:
                l_sch_majoir_name.append(name_tmp)
                l_sch_majoir_id.append(id_tmp)
        result_sch_major = pd.DataFrame.from_dict({'major_id': l_sch_majoir_id, 'major_name': l_sch_majoir_name})

        print('需要处理的majorId  ', len(result_sch_major[['major_id', 'major_name']].drop_duplicates()))

        all_majors = Major.objects.all()
        l_mname = list()
        l_mid = list()
        l_cname = list()
        l_cid = list()
        l_sname = list()
        l_sid = list()

        for one_major in all_majors:
            l_mname.append(one_major.mname)
            l_mid.append(one_major.mid)
            l_cname.append(one_major.cname)
            l_cid.append(one_major.cid)
            l_sname.append(one_major.sname)
            l_sid.append(one_major.sid)

        result_major = pd.DataFrame.from_dict({
            'mname': l_mname,
            'mid': l_mid,
            'cname': l_cname,
            'cid': l_cid,
            'sname': l_sname,
            'sid': l_sid
        })

        data_split_3 = pd.merge(result_sch_major, result_major, left_on='major_name', right_on='mname', how='left')
        result_split_3 = data_split_3[data_split_3['mid'].map(lambda x: len(str(x)) > 5)]

        list_traited = result_split_3['major_id'].values.tolist()
        result_split_3['match_type'] = 0

        data_for_trait = \
            result_sch_major[result_sch_major['major_id'].map(lambda x: x not in list_traited)].reset_index()[
                ['major_id', 'major_name']].drop_duplicates()

        l_major_id = []
        l_major_name = []
        l_split_1_id = []
        l_split_1_name = []
        l_split_2_id = []
        l_split_2_name = []
        l_split_3_id = []
        l_split_3_name = []
        l_match_type = []
        total_len = len(data_for_trait)
        list_result_major = result_major.values
        list_data_trait = data_for_trait.values.tolist()
        for index, one_row in enumerate(list_data_trait):
            if index % 100 == 0:
                print('进度: ', float(index) / total_len)
            for one_major in list_result_major:
                if (one_row[1].find(one_major[0]) >= 0):
                    l_major_id.append(one_row[0])
                    l_major_name.append(one_row[1])
                    l_split_1_id.append(one_major[5])
                    l_split_1_name.append(one_major[4])
                    l_split_2_id.append(one_major[3])
                    l_split_2_name.append(one_major[2])
                    l_split_3_id.append(one_major[1])
                    l_split_3_name.append(one_major[0])
                    l_match_type.append(3)
                else:
                    c_name = one_major[2]
                    if c_name[-1] == '类':
                        c_name = c_name[0:-1]
                    if len(c_name) >= 3 and c_name[-1] == '学':
                        c_name = c_name[0:-1]
                    s_name = one_major[4]
                    if len(s_name) >= 3 and s_name[-1] == '学':
                        s_name = s_name[0:-1]

                    if (one_row[1].find(c_name) >= 0):
                        l_major_id.append(one_row[0])
                        l_major_name.append(one_row[1])
                        l_split_1_id.append(one_major[5])
                        l_split_1_name.append(one_major[4])
                        l_split_2_id.append(one_major[3])
                        l_split_2_name.append(one_major[2])
                        l_split_3_id.append('')
                        l_split_3_name.append('')
                        l_match_type.append(2)
                    elif (one_row[1].find(s_name) >= 0):
                        l_major_id.append(one_row[0])
                        l_major_name.append(one_row[1])
                        l_split_1_id.append(one_major[5])
                        l_split_1_name.append(one_major[4])
                        l_split_2_id.append('')
                        l_split_2_name.append('')
                        l_split_3_id.append('')
                        l_split_3_name.append('')
                        l_match_type.append(1)
                    elif s_name == '工学' and (one_row[1].find('工科') >= 0):
                        l_major_id.append(one_row[0])
                        l_major_name.append(one_row[1])
                        l_split_1_id.append(one_major[5])
                        l_split_1_name.append(one_major[4])
                        l_split_2_id.append('')
                        l_split_2_name.append('')
                        l_split_3_id.append('')
                        l_split_3_name.append('')
                        l_match_type.append(1)
                    elif s_name == '理学' and (one_row[1].find('理科') >= 0):
                        l_major_id.append(one_row[0])
                        l_major_name.append(one_row[1])
                        l_split_1_id.append(one_major[5])
                        l_split_1_name.append(one_major[4])
                        l_split_2_id.append('')
                        l_split_2_name.append('')
                        l_split_3_id.append('')
                        l_split_3_name.append('')
                        l_match_type.append(1)

        result_for_trait = pd.DataFrame.from_dict({
            'major_id': l_major_id,
            'major_name': l_major_name,
            'mid': l_split_3_id,
            'mname': l_split_3_name,
            'cid': l_split_2_id,
            'cname': l_split_2_name,
            'sid': l_split_1_id,
            'sname': l_split_1_name,
            'match_type': l_match_type,
        })

        result_for_trait = result_for_trait.drop_duplicates()
        result_final = pd.concat([result_for_trait, result_split_3], sort=True)

        print('一共处理的major  ', len(result_final['major_id'].unique()))

        for index, one_result in result_final.iterrows():
            kargs = {}
            kargs['major_id'] = one_result['major_id']
            kargs['major_name'] = one_result['major_name']
            kargs['mid'] = one_result['mid']
            kargs['mname'] = one_result['mname']
            kargs['cid'] = one_result['cid']
            kargs['cname'] = one_result['cname']
            kargs['sid'] = one_result['sid']
            kargs['sname'] = one_result['sname']
            kargs['match_type'] = one_result['match_type']
            new_education = MajorSplit(**kargs)
            new_education.save()

    def score_major_split(self):
        from gaokao.models import MajorSplit, SchoolMajorSplit, SchoolMajor, School
        import pandas as pd
        import numpy as np

        all_sch_major = SchoolMajor.objects.all()
        school_id = []
        l_sch_majoir_name = list()
        l_sch_majoir_id = list()
        academic_year = []
        province_id = []
        wenli = []
        batch_name = []
        avg_score_diff = []
        avg_score_rank = []
        max_score_diff = []
        max_score_rank = []
        min_score_diff = []
        min_score_rank = []
        for one_sch_major in all_sch_major:
            school_id.append(str(one_sch_major.school_id))
            l_sch_majoir_name.append(one_sch_major.enroll_major_name)
            l_sch_majoir_id.append(one_sch_major.enroll_major_id)
            province_id.append(one_sch_major.province_id)
            wenli.append(one_sch_major.wenli)
            batch_name.append(one_sch_major.batch_name)
            academic_year.append(one_sch_major.academic_year)
            avg_score_diff.append(one_sch_major.avg_score_diff)
            avg_score_rank.append(one_sch_major.avg_score_rank)
            max_score_diff.append(one_sch_major.max_score_diff)
            max_score_rank.append(one_sch_major.max_score_rank)
            min_score_diff.append(one_sch_major.min_score_diff)
            min_score_rank.append(one_sch_major.min_score_rank)

        data_score_rank = pd.DataFrame.from_dict({
            'sch_id': school_id,
            'major_id': l_sch_majoir_id,
            'major_name': l_sch_majoir_name,
            'academic_year': academic_year,
            'province_id': province_id,
            'wenli': wenli,
            'batch_name':batch_name,
            'avg_score_diff': avg_score_diff,
            'avg_score_rank': avg_score_rank,
            'max_score_diff': max_score_diff,
            'max_score_rank': max_score_rank,
            'min_score_diff': min_score_diff,
            'min_score_rank': min_score_rank
        })

        all_major = MajorSplit.objects.all()
        major_id = []
        major_name = []
        mid = []
        mname = []
        cid = []
        cname = []
        sid = []
        sname = []
        match_type = []

        for one_major in all_major:
            major_id.append(one_major.major_id)
            major_name.append(one_major.major_name)
            mid.append(one_major.mid)
            mname.append(one_major.mname)
            cid.append(one_major.cid)
            cname.append(one_major.cname)
            sid.append(one_major.sid)
            sname.append(one_major.sname)
            match_type.append(one_major.match_type)

        data_major = pd.DataFrame.from_dict({
            'major_id': major_id,
            'major_name': major_name,
            'mid': mid,
            'mname': mname,
            'cid': cid,
            'cname': cname,
            'sid': sid,
            'sname': sname,
            'match_type': match_type
        })

        # 制作16、17年集合
        data_score_rank = data_score_rank[data_score_rank['academic_year'] < '2019']

        data_merge = pd.merge(data_score_rank, data_major, on=['major_id', 'major_name']).sort_values(
            by=['sch_id', 'academic_year']).reset_index()
        print(data_merge)

        def custom_mean(x):
            format_x = []
            for one_x in x.values:
                if int(one_x) > 0 and int(one_x) < 1000000:
                    format_x.append(int(one_x))

            if len(format_x) == 0:
                return -1
            return np.mean(format_x)

        def custom_std(x):
            format_x = []
            for one_x in x.values:
                if int(one_x) > 0 and int(one_x) < 1000000:
                    format_x.append(int(one_x))

            if len(format_x) == 0:
                return -1
            return np.std(format_x)

        def custom_trend(x):
            format_x = []
            for one_x in x.values:
                if int(one_x) > 0 and int(one_x) < 1000000:
                    format_x.append(int(one_x))

            if len(format_x) == 0:
                return -1
            return (format_x[-1] - format_x[0]) / 3

        data_merge_3 = data_merge[[
            'sch_id',
            'mid',
            'province_id',
            'batch_name',
            'wenli',
            'mname',
            'avg_score_diff',
            'avg_score_rank',
            'max_score_diff',
            'max_score_rank',
            'min_score_diff',
            'min_score_rank'
        ]].dropna()

        data_grp_3 = data_merge_3.groupby(['sch_id', 'mid', 'province_id', 'batch_name','wenli', 'mname']).agg(
            [custom_mean, custom_std, custom_trend]).reset_index()

        columns_my = []
        for one_col_name in data_grp_3.columns:
            if len(one_col_name[1].split('_')) > 1:
                columns_my.append(one_col_name[0] + '_' + one_col_name[1].split('_')[1])
            else:
                columns_my.append(one_col_name[0])
        data_grp_3.columns = columns_my

        data_grp_3['level'] = 3

        data_merge_2 = data_merge[[
            'sch_id',
            'province_id',
            'wenli',
            'batch_name',
            'cid',
            'cname',
            'avg_score_diff',
            'avg_score_rank',
            'max_score_diff',
            'max_score_rank',
            'min_score_diff',
            'min_score_rank'
        ]].dropna()
        data_grp_2 = data_merge_2.groupby(['sch_id', 'cid', 'province_id','batch_name', 'wenli', 'cname'])[
            ['avg_score_diff', 'avg_score_rank', 'max_score_diff', 'max_score_rank', 'min_score_diff',
             'min_score_rank']].agg([custom_mean, custom_std, custom_trend]).reset_index().rename(columns={
            'cid': 'mid',
            'cname': 'mname'
        })

        data_grp_2.columns = columns_my

        data_grp_2['level'] = 2

        data_merge_1 = data_merge[[
            'sch_id',
            'province_id',
            'wenli',
            'batch_name',
            'sid',
            'sname',
            'avg_score_diff',
            'avg_score_rank',
            'max_score_diff',
            'max_score_rank',
            'min_score_diff',
            'min_score_rank'
        ]].dropna()

        data_grp_1 = data_merge_1.groupby(['sch_id', 'sid', 'province_id', 'batch_name','wenli', 'sname'])[
            ['avg_score_diff', 'avg_score_rank', 'max_score_diff', 'max_score_rank', 'min_score_diff',
             'min_score_rank']].agg([custom_mean, custom_std, custom_trend]).reset_index().rename(columns={
            'sid': 'mid',
            'sname': 'mname'
        })
        data_grp_1.columns = columns_my

        data_grp_1['level'] = 1

        data_final = pd.concat([data_grp_1, data_grp_2, data_grp_3]).fillna(-1).reset_index()
        data_final = data_final.drop_duplicates()

        leng_data = len(data_final)
        #
        #
        list_data_major = []
        for index, one_data in data_final.iterrows():
            if index % 100 == 0:
                print('进度：', float(index) / leng_data)
            kargs = {}
            kargs['mid'] = one_data['mid']
            kargs['mname'] = one_data['mname']
            kargs['province_id'] = one_data['province_id']
            kargs['wenli'] = one_data['wenli']
            kargs['batch_name'] = one_data['batch_name']
            kargs['avg_score_diff_mean'] = one_data['avg_score_diff_mean']
            kargs['avg_score_rank_mean'] = one_data['avg_score_rank_mean']
            kargs['min_score_diff_mean'] = one_data['min_score_diff_mean']
            kargs['min_score_rank_mean'] = one_data['min_score_rank_mean']
            kargs['max_score_diff_mean'] = one_data['max_score_diff_mean']
            kargs['max_score_rank_mean'] = one_data['max_score_rank_mean']

            kargs['avg_score_diff_std'] = one_data['avg_score_diff_std']
            kargs['avg_score_rank_std'] = one_data['avg_score_rank_std']
            kargs['min_score_diff_std'] = one_data['min_score_diff_std']
            kargs['min_score_rank_std'] = one_data['min_score_rank_std']
            kargs['max_score_diff_std'] = one_data['max_score_diff_std']
            kargs['max_score_rank_std'] = one_data['max_score_rank_std']

            kargs['avg_score_diff_trend'] = one_data['avg_score_diff_trend']
            kargs['avg_score_rank_trend'] = one_data['avg_score_rank_trend']
            kargs['min_score_diff_trend'] = one_data['min_score_diff_trend']
            kargs['min_score_rank_trend'] = one_data['min_score_rank_trend']
            kargs['max_score_diff_trend'] = one_data['max_score_diff_trend']
            kargs['max_score_rank_trend'] = one_data['max_score_rank_trend']
            kargs['m_level'] = one_data['level']
            school = School.objects.get(sch_id=one_data['sch_id'])
            list_data_major.append(SchoolMajorSplit(**kargs,school=school))

        SchoolMajorSplit.objects.bulk_create(list_data_major)


print('执行了么')
dt = DataTraitor()
# print('正在执行：  university')
# dt.university_save_sqlite()
# print('正在执行：  university_detail_sqlite')
# dt.university_detail_sqlite()
# print('正在执行：  niversity_score_sqlite')
# dt.university_score_sqlite()
# print('正在执行：  niversity_major_sqlite')
# dt.university_major_sqlite()
# print('正在执行：  niversity_schoollist_sqlite')
# dt.university_schoollist_sqlite()
print('正在执行：  gaokao_meta_rank')
# dt.gaokao_meta_rank()
print('正在执行：  aokao_score_line')
dt.gaokao_score_line()
# print('正在执行：  aokao_recall_score')
# dt.gaokao_recall_score()
# print('正在执行：  ajor_career_detail')
# dt.major_career_detail()
# print('正在执行：  ajor_split')
# dt.major_split()
# print('正在执行：  core_major_split')
# dt.score_major_split()
