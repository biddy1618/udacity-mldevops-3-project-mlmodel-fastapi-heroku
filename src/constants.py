'''
Constants.

Author: Dauren Baitursyn
Date: 26.08.22
'''
from collections import defaultdict

# Field definitions
ind_fields = [
    'age', 'workclass', 'fnlgt', 'education', 'education_num',
    'marital_status', 'occupation', 'relationship', 'race', 'sex',
    'capital_gain', 'capital_loss', 'hours_per_week', 'native_country',
]

target_field = 'salary'

cat_fields = [
    'workclass', 'education', 'marital_status', 'occupation',
    'relationship', 'race', 'sex', 'native_country']
num_fields = [
    'age', 'fnlgt', 'education_num', 'capital_gain',
    'capital_loss', 'hours_per_week']

mandatory_fields = ['age', 'sex']

zero_imputed = ['fnlgt', 'education_num', 'capital_gain', 'capital_loss']
median_imputed = ['hours_per_week']


# Field values
workclass = set([
    'State-gov',
    'Self-emp-not-inc',
    'Private',
    'Federal-gov',
    'Local-gov',
    'Unknown',
    'Self-emp-inc',
    'Without-pay',
    'Never-worked'
])

education = set([
    'Bachelors',
    'HS-grad',
    '11th',
    'Masters',
    '9th',
    'Some-college',
    'Assoc-acdm',
    'Assoc-voc',
    '7th-8th',
    'Doctorate',
    'Prof-school',
    '5th-6th',
    '10th',
    '1st-4th',
    'Preschool',
    '12th'
])

marital_status = set([
    'Never-married',
    'Married-civ-spouse',
    'Divorced',
    'Married-spouse-absent',
    'Separated',
    'Married-AF-spouse',
    'Widowed'
])

occupation = set([
    'Adm-clerical',
    'Exec-managerial',
    'Handlers-cleaners',
    'Prof-specialty',
    'Other-service',
    'Sales',
    'Craft-repair',
    'Transport-moving',
    'Farming-fishing',
    'Machine-op-inspct',
    'Tech-support',
    'Unknown',
    'Protective-serv',
    'Armed-Forces',
    'Priv-house-serv'
])

relationship = set([
    'Not-in-family',
    'Husband',
    'Wife',
    'Own-child',
    'Unmarried',
    'Other-relative'
])

sex = set(['Male', 'Female'])

native_country = set([
    'United-States',
    'Cuba',
    'Jamaica',
    'India',
    'Unknown',
    'Mexico',
    'South',
    'Puerto-Rico',
    'Honduras',
    'England',
    'Canada',
    'Germany',
    'Iran',
    'Philippines',
    'Italy',
    'Poland',
    'Columbia',
    'Cambodia',
    'Thailand',
    'Ecuador',
    'Laos',
    'Taiwan',
    'Haiti',
    'Portugal',
    'Dominican-Republic',
    'El-Salvador',
    'France',
    'Guatemala',
    'China',
    'Japan',
    'Yugoslavia',
    'Peru',
    'Outlying-US(Guam-USVI-etc)',
    'Scotland',
    'Trinadad&Tobago',
    'Greece',
    'Nicaragua',
    'Vietnam',
    'Hong',
    'Ireland',
    'Hungary',
    'Holand-Netherlands'
])

salary = set(['<=50K', '>50K'])

education_map = defaultdict(int, {
        'Preschool': 1,
        '1st-4th': 2,
        '5th-6th': 3,
        '7th-8th': 4,
        '9th': 5,
        '10th': 6,
        '11th': 7,
        '12th': 8,
        'HS-grad': 9,
        'Some-college': 10,
        'Assoc-voc': 11,
        'Assoc-acdm': 12,
        'Bachelors': 13,
        'Masters': 14,
        'Prof-school': 15,
        'Doctorate': 16}
)
