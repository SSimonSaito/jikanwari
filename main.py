import streamlit as st
import pandas as pd
import random
from collections import defaultdict

# 教師の担当教科と上限コマ数（1週間）
TEACHERS = {
    '川原先生': {'教科': ['現代文', '古文', '漢文'], '上限': 15},
    '土屋先生': {'教科': ['数学Ⅰ', '数学Ⅱ', '数学Ⅲ', '数学A', '数学B', '数学C'], '上限': 15},
    '中山先生': {'教科': ['物理基礎', '物理', '化学基礎', '化学'], '上限': 15},
    '田代先生': {'教科': ['生物基礎', '生物', '地学基礎', '地学'], '上限': 15},
    '小東先生': {'教科': ['英語コミュニケーションⅠ', '英語コミュニケーションⅡ', '英語コミュニケーションⅢ',
                       '論理・表現Ⅰ', '論理・表現Ⅱ', '論理・表現Ⅲ'], '上限': 15},
    '桜木先生': {'教科': ['世界史A', '世界史B', '日本史A', '日本史B', '地理A', '地理B', '現代社会', '倫理', '政治・経済'], '上限': 15},
    '齋須先生': {'教科': ['保健', '体育'], '上限': 15},
    '佐藤先生': {'教科': ['音楽Ⅰ', '音楽Ⅱ', '美術Ⅰ', '美術Ⅱ', '書道Ⅰ', '書道Ⅱ'], '上限': 15},
    '高橋先生': {'教科': ['家庭基礎', '家庭総合'], '上限': 10},
    '山田先生': {'教科': ['情報Ⅰ', '情報Ⅱ'], '上限': 10}
}

REQUIRED_SUBJECTS = {
    '1年': {
        '現代文': 2, '言語文化': 2, '地理総合': 2, '数学Ⅰ': 4, '科学と人間生活': 3,
        '体育': 2, '保健': 1, '英語コミュニケーションⅠ': 3, '論理・表現Ⅰ': 1,
        '家庭基礎': 2, '情報Ⅰ': 2, '芸術科目': 2, '総合探究': 1, 'HR': 1
    },
    '2年': {
        '現代文': 3, '公共': 2, '数学Ⅱ': 4, '理科（選択）': 4, '体育': 2,
        '英語コミュニケーションⅡ': 3, '論理・表現Ⅱ': 1, '総合探究': 1, 'HR': 1
    },
    '3年': {
        '現代文': 3, '倫理/政経': 2, '数学Ⅲ': 3, '理科（選択）': 3, '体育': 2,
        '英語コミュニケーションⅢ': 3, '論理・表現Ⅲ': 1, '総合探究': 1, 'HR': 1
    }
}

DAYS = ['月', '火', '水', '木', '金']
PERIODS_MAP = {'月': 6, '火': 5, '水': 5, '木': 6, '金': 5}
GRADES = ['1年', '2年', '3年']
CLASSES = ['A組', 'B組', 'C組', 'D組']

st.title('進学校向け 時間割作成アプリ（全校一括・現実割当対応）')

if st.button('全学年・全クラスの時間割を作成'):
    timetable = []
    teacher_assignments = defaultdict(int)
    slot_usage = defaultdict(set)

    for grade in GRADES:
        for cls in CLASSES:
            subjects = REQUIRED_SUBJECTS[grade].copy()
            all_slots = [(day, f'{p+1}限') for day in DAYS for p in range(PERIODS_MAP[day])]
            random.shuffle(all_slots)
            for subject, count in subjects.items():
                for _ in range(count):
                    while all_slots:
                        day, period = all_slots.pop()
                        assigned_teacher = next(
                            (t for t, data in TEACHERS.items()
                             if subject in data['教科']
                             and teacher_assignments[t] < data['上限']
                             and t not in slot_usage[(day, period)]),
                            None)
                        if assigned_teacher:
                            timetable.append({
                                '学年': grade, '組': cls, '曜日': day, '時限': period,
                                '教科': subject, '教師': assigned_teacher
                            })
                            teacher_assignments[assigned_teacher] += 1
                            slot_usage[(day, period)].add(assigned_teacher)
                            break

    df = pd.DataFrame(timetable).sort_values(['曜日', '時限', '学年', '組'])
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button('CSVとしてダウンロード', data=csv, file_name='full_timetable.csv', mime='text/csv')
