import pytest
import class_allocation_problem_in_school as classlp

# # ipynbファイルをimportする方法
# from importnb import imports
# with imports("ipynb"):
#     import class_allocation_problem_in_school as classlp


"""
最適化要件1:318人の生徒全員をそれぞれ1つのクラスに割り当てる
"""
@pytest.mark.parametrize(
    "case,expected", [
        ("生徒の総数が318人であることの確認",318),
    ]
)
def test_total_students_number(case, expected):
    student_class_mapping_dict = classlp.student_class_mapping_dict
    students_total_num = 0
    for c, s in student_class_mapping_dict.items():
        print(f"Class:{c}")
        print(f"Num:{len(s)}")
        print(f"Students:{s}")
        print("")
        students_total_num += len(s)
    actual = students_total_num
    assert actual == expected

@pytest.mark.parametrize(
    "case,expected", [
        ("2つ以上のクラスに割り当てられている生徒がいないことの確認(student_idに対してclassを割り当てたdfの形状が想定と一致すれば良い)",(318,1)),
    ]
)
def test_allocated_number(case, expected):
    actual = classlp.result_df.shape
    assert actual == expected

@pytest.mark.parametrize(
    "case,expected", [
        ("割り当てられていない生徒がいないことの確認",0),
    ]
)
def test_non_allocated_students(case, expected):
    actual = classlp.result_df.isnull().any().sum()
    assert actual == expected

"""
最適化要件2:各クラスの生徒数は39人以上、40人以下とする
"""
@pytest.mark.parametrize(
    "case,min_expected, max_expected", [
        ("どのクラスも生徒数の最小値と最大値の範囲内であることの確認",39,40),
    ]
)
def test_allocated_number_in_each_class(case, min_expected, max_expected):
    student_class_mapping_dict = classlp.student_class_mapping_dict
    for c, s in student_class_mapping_dict.items():
        print(f"Class:{c}")
        print(f"Num:{len(s)}")
        actual = len(s)
        assert actual >= min_expected
        assert actual <= max_expected

"""
最適化要件3:各クラスの男子、女子生徒の人数はそれぞれ20人以下とする
"""
@pytest.mark.parametrize(
    "case,gender,max_expected", [
        ("どのクラスも男子が閾値以下であることの確認","male",20),
        ("どのクラスも女子が閾値以下であることの確認","female",20),
    ]
)
def test_allocated_number_in_each_class(case, gender, max_expected):
    num_of_class = classlp.num_of_class
    students_result_df = classlp.students_result_df
    for i in range(num_of_class):
        students_result_class_i_df = students_result_df[students_result_df["class"] == i]
        if gender == "male":
            male_students_result_class_i_df = students_result_class_i_df[students_result_class_i_df["gender"] == 1]
            actual = len(male_students_result_class_i_df)
        elif gender == "female":
            female_students_result_class_i_df = students_result_class_i_df[students_result_class_i_df["gender"] == 0]
            actual = len(female_students_result_class_i_df)
        
        assert actual <= max_expected

"""
最適化要件4:各クラスの学力試験の平均点は学年平均点±10点とする
"""
@pytest.mark.parametrize(
    "case,min_expected, max_expected", [
        ("どのクラスも平均点が想定範囲内であることの確認",classlp.p_mean-10, classlp.p_mean+10),
    ]
)
def test_mean_score_in_each_class(case, min_expected, max_expected):
    print("")
    num_of_class = classlp.num_of_class
    students_result_df = classlp.students_result_df
    for i in range(num_of_class):
        students_result_class_i_df = students_result_df[students_result_df["class"] == i]
        actual = students_result_class_i_df["score"].mean()
        assert actual >= min_expected
        assert actual <= max_expected

"""
最適化要件5:各クラスにリーダー気質の生徒を2人以上割り当てる
"""
@pytest.mark.parametrize(
    "case,min_expected", [
        ("どのクラスも最低数以上のリーダー候補の生徒がいることの確認",2),
    ]
)
def test_num_of_leader_candidates_in_each_class(case, min_expected):
    num_of_class = classlp.num_of_class
    students_result_df = classlp.students_result_df
    for i in range(num_of_class):
        students_result_class_i_df = students_result_df[students_result_df["class"] == i]
        actual = students_result_class_i_df["leader_flag"].sum()
        assert actual >= min_expected

"""
最適化要件6:特別な支援が必要な生徒は各クラスに1人以下とする
"""
@pytest.mark.parametrize(
    "case,max_expected", [
        ("どのクラスも特別な支援が必要な生徒が閾値以下であることの確認",1),
    ]
)
def test_num_of_need_supports_in_each_class(case, max_expected):
    num_of_class = classlp.num_of_class
    students_result_df = classlp.students_result_df
    for i in range(num_of_class):
        students_result_class_i_df = students_result_df[students_result_df["class"] == i]
        actual = students_result_class_i_df["support_flag"].sum()
        assert actual <= max_expected

"""
最適化要件7:特定ペアの生徒は同一クラスに割り当てないように配慮する
"""
@pytest.mark.parametrize(
    "case", [
        ("特定ペアの生徒が割り当てられたクラスは異なることの確認"),
    ]
)
def test_special_students_pair_allocated_in_other_class(case):
    students_pair_df = classlp.students_pair_df
    students_result_df = classlp.students_result_df
    for row in students_pair_df.itertuples():
        id1 = row.student_id1
        id2 = row.student_id2
        class_id1 = students_result_df.query(f"student_id=={id1}")["class"].values[0]
        class_id2 = students_result_df.query(f"student_id=={id2}")["class"].values[0]

        assert class_id1 != class_id2