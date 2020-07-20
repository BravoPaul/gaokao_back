from django.db import models


# Create your models here.


# Create your models here.

class School(models.Model):
    sch_id = models.CharField(max_length=200, primary_key=True, default='-1', unique=True)
    diploma_desc = models.CharField(max_length=200, null=True, blank=True)
    grad_desc = models.CharField(max_length=200, null=True, blank=True)
    independent_desc = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    sch_competent_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_create_time = models.CharField(max_length=200, null=True, blank=True)
    sch_english_name = models.CharField(max_length=200, null=True, blank=True)
    sch_logo = models.ImageField(null=True, blank=True)
    sch_name = models.CharField(max_length=200, null=True, blank=True)
    sch_run_type = models.CharField(max_length=200, null=True, blank=True)
    sch_run_type_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_tags = models.CharField(max_length=200, null=True, blank=True)
    sch_type_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_type_tag_desc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.sch_id


class SchoolList(models.Model):
    condition = models.CharField(max_length=200, default='')
    school = models.ForeignKey(School, on_delete=models.CASCADE)


class SchoolDetail(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    canteen_desc = models.TextField(null=True, blank=True)
    sch_address = models.TextField(max_length=200, null=True, blank=True)
    sch_fellowship = models.TextField(max_length=200, null=True, blank=True)
    sch_intro = models.TextField(max_length=200, null=True, blank=True)
    sch_scholarship = models.TextField(max_length=200, null=True, blank=True)
    sch_tel_num = models.CharField(max_length=200, null=True, blank=True)
    sch_web_url = models.CharField(max_length=200, null=True, blank=True)
    stu_dorm_desc = models.CharField(max_length=200, null=True, blank=True)
    sch_master_ratio = models.FloatField(null=True, blank=True)
    sch_abroad_ratio = models.FloatField(null=True, blank=True)


class SchoolRank(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    rank_type_desc = models.CharField(max_length=200, null=True, blank=True)
    rank_year = models.IntegerField(null=True, blank=True)
    rank_idx = models.IntegerField(null=True, blank=True)
    rank_score = models.FloatField(null=True, blank=True)
    rank_type = models.CharField(max_length=200, null=True, blank=True)
    world_rank_idx = models.IntegerField(null=True, blank=True)


class SchoolFamous(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    celebrity_name = models.CharField(max_length=200, null=True, blank=True)
    celebrity_desc = models.CharField(max_length=200, null=True, blank=True)


# todo 数据表重新插入
class SchoolScore(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # 条件
    province_id = models.CharField(max_length=200, default='')
    academic_year = models.CharField(max_length=200, default='')
    wenli = models.CharField(max_length=200, default='')
    batch = models.CharField(max_length=200, default='')
    batch_name = models.CharField(max_length=200, default='')
    diploma_id = models.CharField(max_length=200, default='')
    # 信息
    admission_count = models.CharField(max_length=200, null=True, blank=True)
    enroll_plan_count = models.CharField(max_length=200, null=True, blank=True)
    max_score = models.CharField(max_length=200, null=True, blank=True)
    max_score_diff = models.CharField(max_length=200, null=True, blank=True)
    max_score_equal = models.CharField(max_length=200, null=True, blank=True)
    max_score_rank = models.CharField(max_length=200, null=True, blank=True)
    min_score = models.CharField(max_length=200, null=True, blank=True)
    min_score_diff = models.CharField(max_length=200, null=True, blank=True)
    min_score_equal = models.CharField(max_length=200, null=True, blank=True)
    min_score_rank = models.CharField(max_length=200, null=True, blank=True)
    avg_score = models.CharField(max_length=200, null=True, blank=True)
    avg_score_diff = models.CharField(max_length=200, null=True, blank=True)
    avg_score_equal = models.CharField(max_length=200, null=True, blank=True)
    avg_score_rank = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.academic_year + '_' + self.min_score


class SchoolMajor(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    # 条件
    province_id = models.CharField(max_length=200, default='')
    wenli = models.CharField(max_length=200, default='')
    academic_year = models.CharField(max_length=200, default='')
    batch = models.CharField(max_length=200, default='')
    batch_name = models.CharField(max_length=200, default='')
    diploma_id = models.CharField(max_length=200, default='')
    # 信息
    academic_rule = models.CharField(max_length=200, null=True, blank=True)
    admission_count = models.CharField(max_length=200, null=True, blank=True)
    avg_score = models.CharField(max_length=200, null=True, blank=True)
    avg_score_diff = models.CharField(max_length=200, null=True, blank=True)
    avg_score_rank = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_code = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_id = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_name = models.CharField(max_length=200, null=True, blank=True)
    enroll_plan_count = models.CharField(max_length=200, null=True, blank=True)
    max_score = models.CharField(max_length=200, null=True, blank=True)
    max_score_diff = models.CharField(max_length=200, null=True, blank=True)
    max_score_rank = models.CharField(max_length=200, null=True, blank=True)
    min_score = models.CharField(max_length=200, null=True, blank=True)
    min_score_diff = models.CharField(max_length=200, null=True, blank=True)
    min_score_rank = models.CharField(max_length=200, null=True, blank=True)
    tuition = models.CharField(max_length=200, null=True, blank=True)


class GaokaoMetaRank(models.Model):
    province_id = models.CharField(max_length=200, default='')
    province = models.CharField(max_length=200, default='河北')
    academic_year = models.CharField(max_length=200, default='2019')
    wenli = models.CharField(max_length=200, default='1')
    score = models.IntegerField(default=300)
    rank = models.IntegerField(default=200)
    rank_cum = models.IntegerField(default=200)


class GaokaoMetaScoreLine(models.Model):
    province_id = models.CharField(max_length=200, default='')
    province = models.CharField(max_length=200, default='河北')
    wenli = models.CharField(max_length=200, default='1')
    batch_name = models.CharField(max_length=200, default='本科第一批')
    academic_year = models.CharField(max_length=200, default='2019')
    school_line = models.IntegerField(default=0)


class GaokaoRecallScore(models.Model):
    province_id = models.CharField(max_length=200, default='')
    province = models.CharField(max_length=200, default='河北')
    wenli = models.CharField(max_length=200, default='1')
    batch_name = models.CharField(max_length=200, default='本科第一批')
    score = models.IntegerField(default=0)
    school_win = models.TextField(null=True, blank=True)
    school_lose = models.TextField(null=True, blank=True)
    school_predict = models.TextField(null=True, blank=True)


class GaokaoRecallRank(models.Model):
    province_id = models.CharField(max_length=200, default='')
    province = models.CharField(max_length=200, default='河北')
    wenli = models.CharField(max_length=200, default='1')
    batch_name = models.CharField(max_length=200, default='本科第一批')
    rank = models.IntegerField(default=0)
    school_win = models.TextField(null=True, blank=True)
    school_lose = models.TextField(null=True, blank=True)
    school_predict = models.TextField(null=True, blank=True)


class Major(models.Model):
    mid = models.CharField(max_length=200, null=True, blank=True)
    mname = models.CharField(max_length=200, null=True, blank=True)
    cid = models.CharField(max_length=200, null=True, blank=True)
    cname = models.CharField(max_length=200, null=True, blank=True)
    sid = models.CharField(max_length=200, null=True, blank=True)
    sname = models.CharField(max_length=200, null=True, blank=True)
    academic_rule = models.CharField(max_length=200, null=True, blank=True)
    careers = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    diploma_id = models.CharField(max_length=200, null=True, blank=True)
    logo_url = models.CharField(max_length=200, null=True, blank=True)
    major_tags = models.CharField(max_length=200, null=True, blank=True)
    major_type = models.CharField(max_length=200, null=True, blank=True)
    employment_info = models.TextField(null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    knowledge_requirement = models.TextField(null=True, blank=True)
    main_course = models.TextField(null=True, blank=True)
    teaching_practice = models.TextField(null=True, blank=True)
    training_objective = models.TextField(null=True, blank=True)
    training_requirement = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.mname


class Career(models.Model):
    cid = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)


class MajorSplit(models.Model):
    major_id = models.CharField(max_length=200, null=True, blank=True)
    major_name = models.CharField(max_length=200, null=True, blank=True)
    mid = models.CharField(max_length=200, null=True, blank=True)
    mname = models.CharField(max_length=200, null=True, blank=True)
    cid = models.CharField(max_length=200, null=True, blank=True)
    cname = models.CharField(max_length=200, null=True, blank=True)
    sid = models.CharField(max_length=200, null=True, blank=True)
    sname = models.CharField(max_length=200, null=True, blank=True)
    match_type = models.IntegerField(default=0)


class SchoolMajorSplit(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    mid = models.CharField(max_length=200, null=True, blank=True)
    mname = models.CharField(max_length=200, null=True, blank=True)
    province_id = models.CharField(max_length=200,default='13')
    wenli = models.CharField(max_length=200,default='1')
    batch_name = models.CharField(max_length=200,default='本科第一批')

    avg_score_diff_mean = models.IntegerField(default=100)
    avg_score_rank_mean = models.IntegerField(default=100)
    min_score_diff_mean = models.IntegerField(default=100)
    min_score_rank_mean = models.IntegerField(default=100)
    max_score_diff_mean = models.IntegerField(default=100)
    max_score_rank_mean = models.IntegerField(default=100)

    avg_score_diff_std = models.IntegerField(default=100)
    avg_score_rank_std = models.IntegerField(default=100)
    min_score_diff_std = models.IntegerField(default=100)
    min_score_rank_std = models.IntegerField(default=100)
    max_score_diff_std = models.IntegerField(default=100)
    max_score_rank_std = models.IntegerField(default=100)

    avg_score_diff_trend = models.IntegerField(default=100)
    avg_score_rank_trend = models.IntegerField(default=100)
    min_score_diff_trend = models.IntegerField(default=100)
    min_score_rank_trend = models.IntegerField(default=100)
    max_score_diff_trend = models.IntegerField(default=100)
    max_score_rank_trend = models.IntegerField(default=100)
    m_level = models.IntegerField(default=-1)



class SchoolMajorSplit_2018(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    mid = models.CharField(max_length=200, null=True, blank=True)
    mname = models.CharField(max_length=200, null=True, blank=True)
    province_id = models.CharField(max_length=200,default='13')
    wenli = models.CharField(max_length=200,default='1')
    batch_name = models.CharField(max_length=200,default='本科第一批')

    avg_score_diff_mean = models.IntegerField(default=100)
    avg_score_rank_mean = models.IntegerField(default=100)
    min_score_diff_mean = models.IntegerField(default=100)
    min_score_rank_mean = models.IntegerField(default=100)
    max_score_diff_mean = models.IntegerField(default=100)
    max_score_rank_mean = models.IntegerField(default=100)

    avg_score_diff_std = models.IntegerField(default=100)
    avg_score_rank_std = models.IntegerField(default=100)
    min_score_diff_std = models.IntegerField(default=100)
    min_score_rank_std = models.IntegerField(default=100)
    max_score_diff_std = models.IntegerField(default=100)
    max_score_rank_std = models.IntegerField(default=100)

    avg_score_diff_trend = models.IntegerField(default=100)
    avg_score_rank_trend = models.IntegerField(default=100)
    min_score_diff_trend = models.IntegerField(default=100)
    min_score_rank_trend = models.IntegerField(default=100)
    max_score_diff_trend = models.IntegerField(default=100)
    max_score_rank_trend = models.IntegerField(default=100)
    m_level = models.IntegerField(default=-1)

# #
# #
class ModelRuleResult(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    enroll_major_id = models.CharField(max_length=200, null=True, blank=True)
    enroll_major_name = models.CharField(max_length=200, null=True, blank=True)
    batch_name = models.CharField(max_length=200, null=True, blank=True)
    wenli = models.CharField(max_length=200, null=True, blank=True)
    province_id = models.CharField(max_length=200, null=True, blank=True)
    min_score_diff_mean = models.IntegerField(default=-1)
    min_score_diff_std = models.IntegerField(default=-1)
    min_score_rank_mean = models.IntegerField(default=-1)
    min_score_rank_std = models.IntegerField(default=-1)
    avg_score_diff_mean = models.IntegerField(default=-1)
    avg_score_diff_std = models.IntegerField(default=-1)
    avg_score_rank_mean = models.IntegerField(default=-1)
    avg_score_rank_std = models.IntegerField(default=-1)
    # 哪种算法做的处理
    type = models.IntegerField(default=1)
