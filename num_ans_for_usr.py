from scipy.stats import nbinom, chisquare
from model import NegativeBinomial
import numpy as np
import pandas as pd


# Number of answers for user, which we use Shifted NBD no spike
num_ans_for_usr = pd.read_csv('num_ans_for_user.csv')

def fit_shifted_NBD(df):
    x = np.array(df['answer_cnt'])
    N = np.array(df['usr_cnt'])
    model = NegativeBinomial(x, N, shifted=True)
    result = model.fit(start_params=np.array([0.5, 0.5]), maxiter=10000, maxfun=5000)
    return pd.Series({'r':result.params[0], 'alpha':result.params[1]})

def get_expected_shifted_NBD(df):
    total = df['usr_cnt'].sum()
    k = df['answer_cnt']
    n = df['r'].unique()
    p = df['alpha'].unique() / (df['alpha'].unique() + 1)
    loc = 1
    return pd.Series({'actual':np.array(df['usr_cnt']),'expected':total * nbinom.pmf(k,n,p,loc)})

def chi_square_goodness_of_fit_NBD(df):
    df['actual'] = np.where(np.logical_or(df['actual'] <=5, df['expected'] <= 5), df['actual'] + 5, df['actual'])
    df['expected'] = np.where(np.logical_or(df['actual'] <=5, df['expected'] <= 5), df['expected'] + 5, df['expected'])
    result = chisquare(df['actual'], df['expected'], df.count() - 1 - 2)
    return pd.Series({'chisq': result[0], 'p':result[1]})

res = num_ans_for_usr.groupby(['site', 'ym']).apply(fit_shifted_NBD).reset_index()
res.to_csv('num_ans_for_usr_model.csv', header=True, index=False)

chi_square_test_res = num_ans_for_usr.set_index(['site', 'ym']).join(res.set_index(['site', 'ym']),
                                                                     on=['site','ym'], how='inner', sort=True) \
                    .groupby(['site', 'ym']).apply(get_expected_shifted_NBD) \
                    .apply(chi_square_goodness_of_fit_NBD, axis=1)
chi_square_test_res.to_csv('num_ans_for_usr_p.csv', header=True, index=False)

network_res = num_ans_for_usr.groupby(['ym','answer_cnt'])['usr_cnt'].sum().reset_index() \
                .groupby('ym').apply(fit_shifted_NBD)
network_res.to_csv('num_ans_for_usr_network.csv', header=True, index=False)