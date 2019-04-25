from statsmodels.base.model import GenericLikelihoodModel
from scipy.stats import nbinom
import numpy as np


class NegativeBinomial(GenericLikelihoodModel):
    def __init__(self, endog, N, **kwds):
        # Endogenous is x
        super(NegativeBinomial, self).__init__(endog, **kwds)
        self.N = N

    def log_likelihood_negative_binomial(self, x, r, alpha, shifted=False):
        # time period unit is one month
        k = x
        n = r
        p = alpha / (alpha + 1)
        loc = int(shifted)
        # pi = abs(1 / (1+pi))
        # if not spike_zero:
        return nbinom.logpmf(k, n, p, loc)
        # else:
        #     return np.log((1 - pi)*nbinom.pmf(k, n, p, loc) + int(not bool(x)) * pi)
        # return np.log((1 - pi)*nbinom.pmf(k, n, p, loc) \
        #         + np.array(np.logical_not(np.array(x, dtype=bool)), dtype=int) * pi)

    def loglike(self, params): # This is actually the log likelihood sum
        r = params[0]
        alpha = params[1]
        try:
            shifted = self.__dict__['shifted']
        except KeyError:
            shifted = False
        # try:
        #     spike_zero = self.__dict__['spike_zero']
        #     if spike_zero:
        #         pi = params[2]
        #     else:
        #         pi = 0
        #     # spike_zero = True
        # except KeyError:
        #     spike_zero = False
        #     pi = 0

        llsum = np.dot(self.N, self.log_likelihood_negative_binomial(self.endog, r, alpha, shifted))
        return llsum
