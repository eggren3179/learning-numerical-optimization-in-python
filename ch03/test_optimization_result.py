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
    print("")
    actual = classlp.result_df.shape
    assert actual == expected