from iblrig_tasks._iblrig_tasks_neuroModulatorChoiceWorld.task import Session

my_session = Session(interactive=False)


import numpy as np
nt = 900
t = np.zeros(nt)
for i in np.arange(nt):
    my_session.next_trial()



my_session.trials_table = my_session.trials_table[:my_session.trial_num]
np.testing.assert_array_equal(my_session.trials_table['trial_num'].values, np.arange(task.trial_num))

import pandas as pd

# Test the blocks task logic
df_blocks = my_session.trials_table.groupby('block_num').agg(
    count=pd.NamedAgg(column="stim_angle", aggfunc="count"),
    n_stim_probability_left=pd.NamedAgg(column="stim_probability_left", aggfunc="nunique"),
    stim_probability_left=pd.NamedAgg(column="stim_probability_left", aggfunc="first"),
    position=pd.NamedAgg(column="position", aggfunc=lambda x: 1 - (np.mean(np.sign(x)) + 1) / 2),
    first_trial=pd.NamedAgg(column="block_trial_num", aggfunc='first'),
)

# test that the first block is 90 trials
assert df_blocks['count'].values[0] == 90
# make all first block trials were reset to 0
assert np.all(df_blocks['first_trial'] == 0)
# test that the first block has 50/50 probability
assert df_blocks['stim_probability_left'].values[0] == 0.5
# make sure that all subsequent blocks alternate between 0.2 and 0.8 left probability
assert np.all(np.isclose(np.abs(np.diff(df_blocks['stim_probability_left'].values[1:])), 0.6))
# assert the the trial outcomes are within 0.3 of the generating probability
assert np.all(np.abs(df_blocks['position'] - df_blocks['stim_probability_left']) < 0.3)
