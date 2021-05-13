# Using a markov chain to determine average number of rolls required from rare to legendary

from numpy.random import default_rng
import pandas as pd
import seaborn as sns

results = pd.DataFrame(columns=('simul_count', 'rr', 're', 'er', 'ee', 'eu', 'ue', 'uu', 'ul'), dtype=int)
rng = default_rng()

# Rate changes according to https://orangemushroom.net/2021/04/30/ability-rank-line-rates-released/
# r denotes rare, e denotes epic, u denotes unique, l denotes legendary
rr_rate = 0.95
re_rate = 0.05
er_rate = 0.01
ee_rate = 0.98
eu_rate = 0.01
ue_rate = 0.14
uu_rate = 0.85
ul_rate = 0.01

while results.shape[0] < 50000:
    ha_rank = 0 # rare, reset
    count_rolls = 0

    # counters for promotions/demotions/same state
    rr_count = 0
    re_count = 0
    er_count = 0
    ee_count = 0
    eu_count = 0
    ue_count = 0
    uu_count = 0
    ul_count = 0
    while ha_rank < 2:
        
        while ha_rank == 0:
            roll_value = rng.random()
            if roll_value > (1 - re_rate):
                ha_rank += 1
                re_count += 1
            else:
                rr_count += 1
            count_rolls += 1
        
        while ha_rank == 1:
            roll_value = rng.random()
            if roll_value < er_rate:
                ha_rank -= 1
                er_count += 1
            elif roll_value > (1 - eu_rate):
                ha_rank += 1
                eu_count += 1
            else:
                ee_count += 1
            count_rolls += 1

        while ha_rank == 2:
            roll_value = rng.random()
            if roll_value < ue_rate:
                ha_rank -= 1
                ue_count += 1
            elif roll_value > (1 - ul_rate):
                ha_rank += 1
                ul_count += 1
            else:
                uu_count += 1
            count_rolls +=1

    results2 = pd.DataFrame([(count_rolls, rr_count, re_count, er_count, ee_count, eu_count, ue_count, uu_count, ul_count)], columns=('simul_count', 'rr', 're', 'er', 'ee', 'eu', 'ue', 'uu', 'ul'))
    results = results.append(results2, ignore_index = True)

#%% Run descriptive statistics.
results
results.describe()

#%% Plotting results
g = sns.histplot(data=results, x='simul_count')
g.set_ylabel('Number of Rolls')