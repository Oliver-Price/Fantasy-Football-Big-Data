#%%
#Loading various things

import pickle
import pandas as pd
import os

year = '19'
save = r'C:\PhD\Python\notebooks\Fantasy-Football-Big-Data\save'
save = os.path.join(save,year)

#%% Combined dataframe with all variables

save_df = os.path.join(save,'df.pickle')
  
with open(save_df, 'rb') as f:
    df = pickle.load(f)
    
#%% Player names
    
save_names = os.path.join('df_names.pickle')
  
with open(save_names, 'rb') as f:
    df_names = pickle.load(f)
    
#%% Positions
    
save_positions = os.path.join('df_positions.pickle')
  
with open(save_positions, 'rb') as f:
    df_positions = pickle.load(f)
    
#%% Clubs
    
save_clubs = os.path.join('df_clubs.pickle')
  
with open(save_clubs, 'rb') as f:
    df_clubs = pickle.load(f)

#%% Stats
    
save_stats = os.path.join('df_stats.pickle')
  
with open(save_stats, 'rb') as f:
    df_stats = pickle.load(f)
    
#%% Bids

save_bids = os.path.join('df_bids.pickle')
  
with open(save_bids, 'rb') as f:
    df_bids = pickle.load(f)