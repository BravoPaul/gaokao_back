# python manage.py shell < /Users/kunyue/project_personal/my_project/mysite/gaokao/recommend.py

from gaokao.models import GaokaoMetaRank, School, GaokaoRecallScore, GaokaoRecallRank, GaokaoMetaScoreLine, SchoolMajor, \
    MajorSplit, ModelRuleResult


class Recommend(object):

    # 专业改名字了怎么办
    # 新专业怎么办

    def __init__(self):
        self.scale = {
            '本科第一批': {
                'score': 5,
                'rank': 100
            },
            '本科第二批': {
                'score': 10,
                'rank': 1000
            },
            '高职专科批': {
                'score': 50,
                'rank': 10000
            }
        }

    def get_recommend_prepare(self, province_id, wenli, year, score):
        from gaokao.models import GaokaoMetaRank, School, GaokaoRecallScore, GaokaoRecallRank, GaokaoMetaScoreLine, \
            SchoolMajor, MajorSplit
        score_1 = GaokaoMetaScoreLine.objects.filter(province_id=province_id, wenli=wenli, academic_year=year,
                                                     batch_name='本科第一批')[0].school_line
        score_2 = GaokaoMetaScoreLine.objects.filter(province_id=province_id, wenli=wenli, academic_year=year,
                                                     batch_name='本科第二批')[0].school_line
        score_3 = GaokaoMetaScoreLine.objects.filter(province_id=province_id, wenli=wenli, academic_year=year,
                                                     batch_name='高职专科批')[0].school_line

        rank_g = GaokaoMetaRank.objects.filter(province_id=province_id, wenli=wenli, academic_year=year, score=score)[0]
        score_rank = rank_g.rank_cum

        result = {'本科第一批': score - score_1, '本科第二批': score - score_2, '高职专科批': score - score_3}, score_rank

        print(result)
        return result

    def get_recommend_result(self, province_id, wenli, year, score):
        from gaokao.models import GaokaoMetaRank, School, GaokaoRecallScore, GaokaoRecallRank, GaokaoMetaScoreLine, \
            SchoolMajor, MajorSplit
        '''
        推荐接口关注的是用户对于所有学校所有专业的概率，而学校的录取概率为所有专业录取概率最低值
        :param province_id: 省份
        :param wenli: 1：文科；2：理科
        :param score: 高考分
        :return:
        '''
        score_diff, score_rank = self.get_recommend_prepare(province_id, wenli, year, score)
        recallResult = self.recallScore(province_id, wenli, score_diff, year)
        rankResult = self.rank(province_id, wenli, score_diff, score_rank, year, recallResult)
        return rankResult

    # @todo 录取概率处理问题，感觉概率都偏小
    def rank(self, province_id, wenli, score_diff, score_rank, year, recallResult):
        from gaokao.models import GaokaoMetaRank, School, GaokaoRecallScore, GaokaoRecallRank, GaokaoMetaScoreLine, \
            SchoolMajor, MajorSplit
        from scipy.stats import norm
        import math

        result_rank = {}

        school_majors_score_1 = ModelRuleResult.objects.filter(wenli=wenli,
                                                               province_id=province_id, type=1)
        school_majors_score_2 = ModelRuleResult.objects.filter(wenli=wenli,
                                                               province_id=province_id, type=2)
        dict_result_1 = {}
        for one_data in school_majors_score_1:
            if dict_result_1.get(one_data.batch_name + '_' + str(one_data.school_id)) is None:
                dict_result_1[one_data.batch_name + '_' + str(one_data.school_id)] = [one_data]
            else:
                dict_result_1[one_data.batch_name + '_' + str(one_data.school_id)].append(one_data)
        dict_result_2 = {}
        for one_data in school_majors_score_2:
            if dict_result_2.get(one_data.batch_name + '_' + str(one_data.school_id)) is None:
                dict_result_2[one_data.batch_name + '_' + str(one_data.school_id)] = [one_data]
            else:
                dict_result_2[one_data.batch_name + '_' + str(one_data.school_id)].append(one_data)


        for key, value in recallResult.items():
            result_rank_tmp = []
            for index, one_value in enumerate(value):
                sch_id = one_value['sch_id']
                one_value['major'] = []
                min_probability = 0
                if dict_result_1.get(key + '_' + sch_id) is not None:
                    for one_major_score in dict_result_1[key + '_' + sch_id]:
                        major_tmp = {}

                        scall_score_min = self.scale[key]['score'] if int(one_major_score.min_score_diff_std) < \
                                                                      self.scale[key]['score'] else int(
                            one_major_score.min_score_diff_std)
                        scall_rank_min = self.scale[key]['rank'] if int(one_major_score.min_score_rank_std) < \
                                                                    self.scale[key]['rank'] else int(
                            one_major_score.min_score_rank_std)
                        probability_score_min = norm.cdf(x=int(score_diff[key]),
                                                         loc=int(one_major_score.min_score_diff_mean),
                                                         scale=scall_score_min)
                        probability_rank_min = 1 - norm.cdf(x=int(score_rank),
                                                            loc=int(one_major_score.min_score_rank_mean),
                                                            scale=scall_rank_min)
                        probability_min = (probability_score_min + probability_rank_min) / 2

                        # avg
                        scall_score_avg = self.scale[key]['score'] if int(one_major_score.avg_score_diff_std) < \
                                                                      self.scale[key]['score'] else int(
                            one_major_score.avg_score_diff_std)
                        scall_rank_avg = self.scale[key]['rank'] if int(one_major_score.avg_score_rank_std) < \
                                                                    self.scale[key]['rank'] else int(
                            one_major_score.avg_score_rank_std)
                        probability_score_avg = norm.cdf(x=int(score_diff[key]),
                                                         loc=int(one_major_score.avg_score_diff_mean),
                                                         scale=scall_score_avg)
                        probability_rank_avg = 1 - norm.cdf(x=int(score_rank),
                                                            loc=int(one_major_score.min_score_rank_mean),
                                                            scale=scall_rank_avg)
                        probability_avg = (probability_score_avg + probability_rank_avg) / 2

                        # 融合
                        probability = (probability_min + probability_avg) / 2

                        if probability > min_probability:
                            min_probability = probability

                        major_tmp['major_id'] = str(one_major_score.enroll_major_id)
                        major_tmp['probability'] = int(round(probability, 2) * 100)

                        one_value['major'].append(major_tmp)

                elif dict_result_2.get(key + '_' + sch_id) is not None:
                    for one_major_score in dict_result_2[key + '_' + sch_id]:
                        major_tmp = {}
                        scall_score_min = self.scale[key]['score'] if int(one_major_score.min_score_diff_std) < \
                                                                      self.scale[key]['score'] else int(
                            one_major_score.min_score_diff_std)
                        scall_rank_min = self.scale[key]['rank'] if int(one_major_score.min_score_rank_std) < \
                                                                    self.scale[key]['rank'] else int(
                            one_major_score.min_score_rank_std)
                        probability_score_min = norm.cdf(x=int(score_diff[key]),
                                                         loc=int(one_major_score.min_score_diff_mean),
                                                         scale=scall_score_min)
                        probability_rank_min = 1 - norm.cdf(x=int(score_rank),
                                                            loc=int(one_major_score.min_score_rank_mean),
                                                            scale=scall_rank_min)
                        probability_min = (probability_score_min + probability_rank_min) / 2

                        if probability_min > min_probability:
                            min_probability = probability_min

                        major_tmp['major_id'] = str(one_major_score.enroll_major_id)
                        major_tmp['probability'] = int(round(probability_min, 2) * 100)

                        one_value['major'].append(major_tmp)

                else:
                    print(key + '_' + sch_id)


                one_value['probability'] = int(round(min_probability, 2) * 100)

                if one_value['probability'] > 0 and one_value['probability'] <= 100:
                    json_tmp = {
                        'sch_id': one_value['sch_id'],
                        'probability': one_value['probability'],
                        'major': one_value['major']
                    }
                    result_rank_tmp.append(json_tmp)
            result_rank[key] = result_rank_tmp

        print('打分情况如下: \n')
        print(len(result_rank['本科第一批']))
        print(len(result_rank['本科第二批']))
        print(len(result_rank['高职专科批']))

        return result_rank

    def recallScore(self, province_id, wenli, score_diffs, year):
        from gaokao.models import GaokaoMetaRank, School, GaokaoRecallScore, GaokaoRecallRank, GaokaoMetaScoreLine, \
            SchoolMajor, MajorSplit
        '''
        召回分为3种，肯定能上的，肯定不能上的和不确定的，打分的意义在于给不确定的打分
        :param province_id:
        :param wenli:
        :param score:
        :return:
        '''

        result = {
            '本科第一批': [],
            '本科第二批': [],
            '高职专科批': [],
        }
        score_line = GaokaoMetaScoreLine.objects.filter(
            province_id=province_id,
            wenli=wenli,
            academic_year=year
        )
        print(score_line)
        scores_lines = ['本科第一批', '本科第二批', '高职专科批']

        for key, value in score_diffs.items():
            if value >= 0:
                score_diff = value
                print('正在预测', key, score_diffs)
                recall_data = GaokaoRecallScore.objects.filter(
                    province_id=province_id,
                    wenli=wenli,
                    batch_name=key,
                )
                scores = []
                for one_data in recall_data:
                    scores.append(one_data.score)
                    if one_data.score == score_diff:
                        sch_wins = one_data.school_win.split(',')
                        school_loses = one_data.school_lose.split(',')
                        school_predicts = one_data.school_predict.split(',')
                        for one_sch in school_predicts:
                            result[key].append({'sch_id': one_sch, 'probability': 50})
                        for one_sch in school_loses:
                            result[key].append({'sch_id': one_sch, 'probability': 10})
                        for one_sch in sch_wins:
                            result[key].append({'sch_id': one_sch, 'probability': 90})

                if len(result[key]) == 0:
                    max_score = max(scores)
                    min_score = max(scores)
                    max_index = scores.index(max_score)
                    min_index = scores.index(min_score)
                    if score_diff > max_score:
                        print('这里max')
                        sch_wins = recall_data[max_index].school_win.split(',')
                        school_predicts = recall_data[max_index].school_predict.split(',')
                        for one_sch in school_predicts:
                            if one_sch != '':
                                result[key].append({'sch_id': one_sch, 'probability': 90})
                        for one_sch in sch_wins:
                            if one_sch != '':
                                result[key].append({'sch_id': one_sch, 'probability': 90})

                    elif score_diff < min_score:
                        print('这里min')
                        school_loses = recall_data[min_index].school_lose.split(',')
                        school_predicts = recall_data[min_index].school_predict.split(',')
                        for one_sch in school_predicts:
                            if one_sch != '':
                                result[key].append({'sch_id': one_sch, 'probability': 10})
                        for one_sch in school_loses:
                            if one_sch != '':
                                result[key].append({'sch_id': one_sch, 'probability': 10})

                    else:
                        raise ValueError

            result[key] = result[key][0:100]

        print('召回情况如下: \n')
        print(len(result['本科第一批']))
        print(len(result['本科第二批']))
        print(len(result['高职专科批']))

        # print(result)

        return result

    def recallRank(self, province_id, wenli, score):
        '''
        召回分为3种，肯定能上的，肯定不能上的和不确定的，打分的意义在于给不确定的打分
        :param province_id:
        :param wenli:
        :param score:
        :return:
        '''
        return 1
