from scipy.stats import nbinom, chisquare
from model import NegativeBinomial
import numpy as np
import pandas as pd


# Number of answers per question, in one-month rolling time frame, where we use NBD spike
num_ans_for_q = pd.read_csv('num_ans_for_q.csv')

def fit_spike_NBD(df):
    x = np.array(df['answercount'])
    N = np.array(df['question_cnt'])
    model = NegativeBinomial(x, N, shifted=False)
    result = model.fit(start_params=np.array([0.5, 0.5]), maxiter=10000, maxfun=5000)
    return pd.Series({'r':result.params[0], 'alpha':result.params[1]})

def get_expected_spike_NBD(df):
    total = df['question_cnt'].sum()
    k = df['answercount']
    n = df['r'].unique()
    p = df['alpha'].unique() / (df['alpha'].unique() + 1)
    # pi = df['pi'].unique()
    loc = 0
    return pd.Series({'actual':np.array(df['question_cnt']), \
                        'expected': total*nbinom.pmf(k,n,p,loc)})
                #       'expected':total * (1 - pi)*nbinom.pmf(k, n, p, loc) \
                # + np.array(np.logical_not(np.array(k, dtype=bool)), dtype=int) * pi})

def chi_square_goodness_of_fit(df):
    df['actual'] = np.where(np.logical_or(df['actual'] <=5, df['expected'] <= 5), df['actual'] + 5, df['actual'])
    df['expected'] = np.where(np.logical_or(df['actual'] <=5, df['expected'] <= 5), df['expected'] + 5, df['expected'])
    result = chisquare(df['actual'], df['expected'], df.count() - 1 - 2)
    return pd.Series({'chisq': result[0], 'p':result[1]})

res = num_ans_for_q.groupby(['site', 'ym']).apply(fit_spike_NBD).reset_index()
res.to_csv('num_ans_for_q_model.csv', header=True, index=False)
# res = pd.read_csv('num_ans_for_q_model.csv')
chi_square_test_res = num_ans_for_q.set_index(['site', 'ym']).join(res.set_index(['site', 'ym']),
                                                                   on=['site', 'ym'], how='inner', sort=True) \
                    .groupby(['site', 'ym']).apply(get_expected_spike_NBD) \
                    .apply(chi_square_goodness_of_fit, axis=1)
chi_square_test_res.to_csv('num_ans_for_q_p.csv', header=True, index=False)

network_res = num_ans_for_q.groupby(['ym', 'answercount'])['question_cnt'].sum().reset_index() \
                .groupby('ym').apply(fit_spike_NBD)
network_res.to_csv('num_ans_for_q_network.csv', header=True, index=True)