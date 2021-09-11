def german_data_to_csv():
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('datasets/german.data', sep=' ')
    df.info()
    print(df)

    df['checking_account'] = df['checking_account'].map(
        {'A11': '<0', 'A12': '0<=x<200', 'A13': '>=200', 'A14': 'None'}).astype(str)
    df['credit_history'] = df['credit_history'].map(
        {'A30': 'no_credits_taken', 'A31': 'all_credits_paid_bank',
         'A32': 'existing_credits_paid', 'A33': 'delay_in_past', 'A34': 'critical'}).astype(str)
    df['purpose'] = df['purpose'].map(
        {'A40': 'car_new', 'A41': 'car_used', 'A42': 'furniture/equipment', 'A43': 'radio/tv',
         'A44': 'domestic_appliances', 'A45': 'repairs', 'A46': 'education', 'A47': 'vacation', 'A48': 'retraining',
         'A49': 'business', 'A410': 'others'}).astype(str)
    df['savings_account'] = df['savings_account'].map(
        {'A61': '<100', 'A62': '100<=x<500', 'A63': '500<=x<1000', 'A64': '>=1000', 'A65': 'unknown'}).astype(str)
    df['present_employment_since'] = df['present_employment_since'].map(
        {'A71': 'unemployed', 'A72': '<1', 'A73': '1<=x<4', 'A74': '4<=x<7', 'A75': '>=7'}).astype(str)
    df['personal_status_sex'] = df['personal_status_sex'].map(
        {'A91': 'male_divorced/separated', 'A92': 'female_divorced/separated/married', 'A93': 'male_single',
         'A94': 'male_married/widowed', 'A95': 'female_single'}).astype(str)
    df['other_debtors_guarantors'] = df['other_debtors_guarantors'].map(
        {'A101': 'None', 'A102': 'co-applicant', 'A103': 'guarantor'}).astype(str)
    df['property'] = df['property'].map(
        {'A121': 'real_estate', 'A122': 'savings_insurance', 'A123': 'car_other', 'A124': 'unknown'}).astype(str)
    df['installment_plans'] = df['installment_plans'].map(
        {'A141': 'bank', 'A142': 'stores', 'A143': 'None'}).astype(str)
    df['housing'] = df['housing'].map(
        {'A151': 'rent', 'A152': 'own', 'A153': 'for_free'}).astype(str)
    df['job'] = df['job'].map(
        {'A171': 'unemployed', 'A172': 'unskilled', 'A173': 'skilled', 'A174': 'management'}).astype(str)
    df['telephone'] = df['telephone'].map(
        {'A191': 'none', 'A192': 'yes'}).astype(str)
    df['foreign'] = df['foreign'].map(
        {'A201': 'yes', 'A202': 'no'}).astype(str)
    df['risk'] = df['risk'].map(
        {1: 'good', 2: 'bad'}).astype(str)

    print(df)
    df.to_csv('datasets/german_credit_data.csv')
