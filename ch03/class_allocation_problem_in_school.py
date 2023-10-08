#!/usr/bin/env python
# coding: utf-8

# # 学校のクラス編成問題

# ## 1. 問題設定
# とある学校のある学年のクラス編成を考える問題を考える。
# #### 1-1. 前提条件
#  - 学年の人数：318人（男子：158人、女子：160人）
#  - クラス数：8
#  - 学力試験は500点満点で、学年平均点は303.6点
#  - 学年にリーダー気質の生徒が17人いる
#  - 学年に特別な支援が必要な生徒が4人いる
# #### 1-2. 解くべき最適化問題の要件
#  - 318人の生徒全員をそれぞれ1つのクラスに割り当てる
#  - 8つのクラスに割り当てるので、各クラスの生徒数は39人以上、40人以下とする
#  - クラスの男女の割合をほぼ一定にするため、各クラスの男子、女子生徒の人数はそれぞれ20人以下とする
#  - クラス間の学力差をなくすため、各クラスの学力試験の平均点は学年平均点$\pm10$点とする
#  - 各クラスにリーダー気質の生徒を2人以上割り当てる
#  - 特別な支援が必要な生徒は各クラスに1人以下とする
#  - 同姓同名や双子の兄弟など、特定ペアの生徒は同一クラスに割り当てないように配慮する

# ## 2. 必要ライブラリのインポートとデータ確認

# In[1]:


import numpy as np
import pandas as pd


# ##### 生徒情報の確認

# In[2]:


students_df = pd.read_csv("./data/students.csv")
students_df


# student_idがユニークな値で、欠損値なくすべての値が使われているかどうかの確認

# In[3]:


studnet_id_list = students_df["student_id"].unique()
is_student_id_unique = len(studnet_id_list) == 318
is_student_id_not_loss = set(range(1,319)) == set(studnet_id_list)
print(f"Num of student_id:{len(studnet_id_list)}")
print(f"Is student_id unique?:{is_student_id_unique}")
print(f"Is there number-loss in student_id?:{is_student_id_not_loss}")


# In[4]:


students_df["score"].describe()


# In[5]:


students_df["score"].hist()


# In[6]:


students_df["gender"].value_counts()


# In[7]:


students_df["leader_flag"].value_counts()


# In[8]:


students_df["support_flag"].value_counts()


# ##### 生徒内で考慮が必要な特定ペア情報の確認

# In[9]:


students_pair_df = pd.read_csv("./data/student_pairs.csv")
students_pair_df


# ## 3. 最適化問題の定義

# In[10]:


import pulp


# In[11]:


problem = pulp.LpProblem("ClassAssignmentProblem", pulp.LpMaximize)


# #### 3-1. 最適化要件１：318人の生徒全員をそれぞれ1つのクラスに割り当てる
#  - 生徒のリスト$S$, クラスのリスト$C$とする。
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#    $$
#    x_{s,c} = \left\{
#    \begin{array}{ll}
#    1 & (\text{allocated}) \\ 
#    0 & (\text{not allocated})
#    \end{array}
#    \right.
#    $$
#  - 各クラスへ割り当てられる
#    $$ \sum_{c\in C} x_{s,c} = 1$$
# 

# In[12]:


num_of_class = 8
class_list = [c for c in range(num_of_class)]
class_list


# In[13]:


students_list = students_df["student_id"].to_list()
# students_list


# In[14]:


# 生徒とクラスの全ペアのリスト
all_class_students_pair = [(s,c) for s in students_list for c in class_list]
# all_class_students_pair

# 生徒をどのクラスに割り当てるかを表す変数を定義
x = pulp.LpVariable.dicts("x",all_class_students_pair, cat="Binary")
# x
# {(1, 0): x_(1,_0),
#  (1, 1): x_(1,_1),
#  (1, 2): x_(1,_2),
#  (1, 3): x_(1,_3),
#  (1, 4): x_(1,_4),...}


# In[15]:


# 最適化要件１の実装
for s in students_list:
    problem += pulp.lpSum([x[s,c] for c in class_list]) == 1


# #### 3-2. 最適化要件２：各クラスの生徒数は39人以上、40人以下とする
#  - 生徒のリスト$S$, クラスのリスト$C$とする
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#  - 満たすべき条件式：
#     $$ \sum_{s \in S} x_{s,c} >= 39$$
#     $$ \sum_{s \in S} x_{s,c} <= 40$$

# In[16]:


#最適化要件２の実装
for c in class_list:
    problem += pulp.lpSum([x[s,c] for s in students_list]) >= 39
    problem += pulp.lpSum([x[s,c] for s in students_list]) <= 40


# #### 3-3. 最適化要件３：各クラスの男子、女子生徒の人数はそれぞれ20人以下とする
#  - 生徒のリスト$S$, クラスのリスト$C$とする
#  - 男子生徒のリスト$S_{\text{male}}$, 女子生徒のリスト$S_{\text{female}}$とする。
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$が満たすべき条件式
#    $$ \sum_{s \in S_{\text{male}}} x_{s,c} <= 20$$
#    $$ \sum_{s \in S_{\text{female}}} x_{s,c} <= 20$$

# In[17]:


male_df = students_df[students_df["gender"] == 1]
male_list = male_df["student_id"].to_list()
print(f"num of male:{len(male_list)}")


# In[18]:


female_df = students_df[students_df["gender"] == 0]
female_list = female_df["student_id"].to_list()
print(f"num of female:{len(female_list)}")


# In[19]:


#最適化要件３の実装
for c in class_list:
    problem += pulp.lpSum([x[ms,c] for ms in male_list]) <= 20
    problem += pulp.lpSum([x[fs,c] for fs in female_list]) <= 20


# #### 3-4. 最適化要件４：各クラスの学力試験の平均点は学年平均点±10点とする
#  - 生徒のリスト$S$, クラスのリスト$C$
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#  - 生徒$s(\in S)$の学力試験の点数$p_{s}$, 学年の平均点$p_{mean}$
#  - 満たすべき条件式
#    $$ \frac{\sum_{s \in S} p_{s} x_{s, c}}{\sum_{s \in S} x_{s,c}} >= (p_{mean} - 10) $$
#    $$ \frac{\sum_{s \in S} p_{s} x_{s, c}}{\sum_{s \in S} x_{s,c}} <= (p_{mean} + 10) $$

# ただし、満たすべき条件式が非線形の式となっており、使える最適化ソルバが限定されると同時に、解くことができるサイズが限定される。そのため、条件式を次のように変形して線形最適化問題に落とし込む。
# 
#  - 満たすべき条件式
#    $$ \sum_{s \in S} p_{s} x_{s, c} >= (p_{mean} - 10) * \sum_{s \in S} x_{s,c}$$
#    $$ \sum_{s \in S} p_{s} x_{s, c} <= (p_{mean} + 10) * \sum_{s \in S} x_{s,c}$$
#  

# In[20]:


# 最適化要件４の実装
p_mean = students_df["score"].mean()
print(f"Mean scoer of students:{p_mean}")
score_dict = {row.student_id:row.score for row in students_df.itertuples()}
# print(score_list)
for c in class_list:
    problem += pulp.lpSum([score_dict[s] * x[s,c] for s in students_list]) >= (p_mean - 10) * pulp.lpSum([x[s,c] for s in students_list])
    problem += pulp.lpSum([score_dict[s] * x[s,c] for s in students_list]) <= (p_mean + 10) * pulp.lpSum([x[s,c] for s in students_list])


# #### 3-5. 最適化要件５：各クラスにリーダー気質の生徒を2人以上割り当てる
#  - リーダー気質の生徒リスト$S_{\text{leader}}$
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#  - 満たすべき条件式
#    $$\sum_{s \in S_{\text{leader}}} x_{s,c} >= 2$$

# In[21]:


# リーダー気質の生徒のリスト作成
leader_list = [row.student_id for row in students_df.itertuples() if row.leader_flag==1 ]
print(len(leader_list))
leader_list


# In[22]:


# 最適化要件５の実装
for c in class_list:
    problem += pulp.lpSum([x[s,c] for s in leader_list]) >= 2


# #### 3-6. 最適化要件６：特別な支援が必要な生徒は各クラスに1人以下とする
#  - 特別な支援が必要な生徒のリスト$S_{\text{support}}$
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#  - 満たすべき条件式
#    $$\sum_{s \in S_{\text{support}}} x_{s,c} <= 1$$

# In[23]:


support_list = [row.student_id for row in students_df.itertuples() if row.support_flag == 1]
print(len(support_list))
support_list


# In[24]:


# 最適化要件６の実装
for c in class_list:
    problem += pulp.lpSum([x[s,c] for s in support_list]) <= 1


# #### 3-7. 最適化要件７：特定ペアの生徒は同一クラスに割り当てないように配慮する
#  - 特定ペアの生徒リスト$S_{\text{special}}$
#  - 生徒$s(\in S)$がクラス$c(\in C)$に割り当てられるかどうかを表す変数$x_{s,c}$
#  - 満たすべき条件式
#    $$x_{s1,c} + x_{s2, c} <= 1 \ \ ((s1, s2) \in S_{\text{special}})$$

# In[25]:


# students_pair_df["student_id1"]
students_pair_tuple_list = [(row.student_id1, row.student_id2) for row in students_pair_df.itertuples()]
students_pair_tuple_list


# In[26]:


# 最適化要件７の実装
for s1, s2 in students_pair_tuple_list:
    for c in class_list:
        problem += pulp.lpSum([x[s1,c], x[s2,c]]) <= 1


# In[27]:


# print(problem)


# #### 3-8. 最適化問題の求解

# In[28]:


status = problem.solve()
print(status)
print(pulp.LpStatus[status])


# #### 3-9. 最適化問題の結果の表示

# In[29]:


student_class_mapping_dict = {}
for c in class_list:
    student_class_mapping_dict[c] = [s for s in students_list if x[s,c].value() == 1]

for c, s in student_class_mapping_dict.items():
    print(f"Class:{c}")
    print(f"Num:{len(s)}")
    print(f"Students:{s}")
    print("")


# ## 4. 最適化問題の結果の検証

# #### 4-1. 最適化要件１の検証
#  - 「318人の生徒全員をそれぞれ1つのクラスに割り当てる」ことが満たされているか検証

# In[36]:


studentid_class_mapping_dict = {s:c for s in students_list for c in class_list if x[s,c].value()==1}
# studentid_class_mapping_dict


# In[42]:


result_df = pd.DataFrame.from_dict(studentid_class_mapping_dict.values())
result_df


# In[46]:


result_df.shape


# In[62]:


result_df.isnull().any()


# In[63]:


result_df.isnull().any().sum()


# In[43]:


students_result_df = students_df.copy()
students_result_df["class"] =result_df
students_result_df


# このdfが問題なく作られており、class列のdfにNoneがないということは1人に1つのクラスが割り当てられていることの確認ができた、ということを意味している。

# #### 4-2. 最適化要件２の検証
#  - 「各クラスの生徒数は39人以上、40人以下とする」ことが満たされているか検証

# In[68]:


print("Check the number of students in each class...")
for c, s in student_class_mapping_dict.items():
    print(f"class:{c}")
    print(f"Allocated results:{len(s)}")
    if len(s) < 39 or len(s) > 40:
        print(f"Error!!:: class {c} is allocated more or less allocated number of students than expected")
    else:
        print("OK")
    print("")


# #### 4-3.最適化要件３の検証
#  - 「各クラスの男子、女子生徒の人数はそれぞれ20人以下とする」ことが満たされていることの検証

# In[77]:


print("Check the number of male and female students in each class...")
for i in range(num_of_class):
    print(f"class:{i}")
    students_result_class_i_df = students_result_df[students_result_df["class"] == i]
    male_students_result_class_i_df = students_result_class_i_df[students_result_class_i_df["gender"] == 1]
    female_students_result_class_i_df = students_result_class_i_df[students_result_class_i_df["gender"] == 0]
    male_number = len(male_students_result_class_i_df)
    female_number = len(female_students_result_class_i_df)
    print(f"number of male:{male_number}")
    print(f"number of female:{female_number}")
    
    if male_number > 20 or female_number > 20:
        print(f"Error!!:: class {i} is allocated more or less number of male or female than expected")
    else:
        print("OK")
        print("")


# #### 4-4. 最適化要件４の検証
#  - 「各クラスの学力試験の平均点は学年平均点±10点とする」ことが満たされていることの検証

# In[79]:


print("Check the mean of score in each class...")
for i in range(num_of_class):
    print(f"class:{i}")
    students_result_class_i_df = students_result_df[students_result_df["class"] == i]
    mean_i = students_result_class_i_df["score"].mean()
    print(f"men score:{mean_i}")
    if mean_i < p_mean -10 or mean_i > p_mean + 10:
        print(f"Error!!:: mean score of class {i} less or more than expected")
    else:
        print("OK")
    print("")


# #### 4-5. 最適化要件５の検証
#  - 「各クラスにリーダー気質の生徒を2人以上割り当てる」ことが満たされていることの検証

# In[88]:


print("Check the number of students of leader_flag in each class...")
for i in range(num_of_class):
    print(f"class:{i}")
    students_result_class_i_df = students_result_df[students_result_df["class"] == i]
    num_of_leader_class_i = students_result_class_i_df["leader_flag"].sum()
    print(f"num_of_leader:{num_of_leader_class_i}")
    if num_of_leader_class_i <2:
        print(f"Error!!:: number of leader candidates in class {i} less or more than expected")
    else:
        print("OK")
    print("")


# #### 4-6.最適化要件６の検証
#  - 「特別な支援が必要な生徒は各クラスに1人以下とする」が満たされていることの検証

# In[86]:


print("Check the number of students who needs support by someone...")
for i in range(num_of_class):
    print(f"class:{i}")
    students_result_class_i_df = students_result_df[students_result_df["class"] == i]
    num_of_need_support = students_result_class_i_df["support_flag"].sum()
    print(f"num_of_need_support:{num_of_need_support}")
    if num_of_need_support > 1:
        print(f"Error!!:: number of students who needs support by someone in class {i} is more than expected")
    else:
        print("OK")
    print("")


# #### 4-7.最適化要件７の検証
#  - 「特定ペアの生徒は同一クラスに割り当てないように配慮する」が満たされていることの検証

# In[144]:


print("Check the class of students who are belong in the special pair list...")
for row in students_pair_df.itertuples():
    id1 = row.student_id1
    id2 = row.student_id2
    print(f"id1:{id1}")
    class_id1 = students_result_df.query(f"student_id=={id1}")["class"].values[0]
    # class_id1 = students_result_df.loc[students_result_df['student_id'] == f'{id1}', 'class'].values[0]
    print(f"class_id1:{class_id1}")
    print(f"id2:{id2}")
    class_id2 = students_result_df.query(f"student_id=={id2}")["class"].values[0]
    print(f"class_id2:{class_id2}")
    
    if class_id1 == class_id2:
        print(f"Error!!:: {id1} and {id2} are allocated the same class {class_id1}")
    else:
        print("OK")
    print("")

    


# In[ ]:




