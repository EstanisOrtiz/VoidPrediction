import pandas as pd

# Custom modules
from gbvoid_dataset import gbvoid_dataset
#from .gbvoid_dataset import *

# Junction and Prox_par have null values

inputs = ['1_001', '1_002', '1_003', '1_004', '1_005', '1_006', '1_007', '1_008', '1_009', '1_010',
          '2_001', '2_002', '2_003', '2_004', '2_005', '2_006', '2_007', '2_008', '2_009',
          '3_001', '3_002', '3_003', '3_004', '3_005', '3_006', '3_007', '3_008', '3_009', '3_010',
          '4_001', '4_002', '4_003', '4_004', '4_005', '4_007', '4_008', '4_009',
          '5_001', '5_002', '5_003', '5_004', '5_005', '5_006', '5_007', '5_008', '5_009', '5_010', '5_011',
          '6_001', '6_002', '6_003', '6_004', '6_005', '6_006', '6_007', '6_008', '6_009', '6_010']

#inputs=['1_001']

columns_void = ['phi1_right', 'PHI_right', 'phi2_right', 'phi1_left', 'PHI_left', 'phi2_left',
                'misorientation', 'mis_x_right', 'mis_y_right', 'mis_z_right',
                'mis_x_left', 'mis_y_left', 'mis_z_left',
                'Length', 'Trace', 'x_start', 'y_start', 'x_end', 'y_end', 'gbID_right', 'gbID_left', 'Sigma',
                'Distance_Center',
                'Void_id', 'x_junction', 'y_junction', 'Rebuild_len', 'Junction','Prox_par', 'Void', 'Void_Parameter']

drop_col=['phi1_right', 'PHI_right', 'phi2_right', 'phi1_left', 'PHI_left',
       'phi2_left', 'mis_x_right', 'mis_y_right',
       'mis_z_right', 'mis_x_left', 'mis_y_left', 'mis_z_left',
       'x_start', 'y_start', 'x_end', 'y_end', 'gbID_right',
       'gbID_left','x_junction','y_junction']

data=[]
data_sel=[]
for name in inputs:
    void_dataset = gbvoid_dataset(name)

    # Drop negative Void Parameter
    void_dataset = void_dataset.loc[void_dataset['Void'] != -1.0]  # Drop Noise

    data.append(void_dataset) # big df
    void_dataset.columns = columns_void

    # Drop extra features
    void_dataset = void_dataset.drop(drop_col, axis=1)

    # Selected dataframe
    df_selected = void_dataset[void_dataset['Void'] == 1]

    # No void selected dataframe
    df_no=void_dataset[void_dataset['Void']==0]

    # Save sample DataSets
    path_out1='/home/estanislao/Documents/ML_GB/GrainLearning/output/'+name+'/df_all.csv'
    path_out2 = '/home/estanislao/Documents/ML_GB/GrainLearning/output/' + name + '/df_selected.csv'
    void_dataset.to_csv(path_out1, header=True)
    df_selected.to_csv(path_out2, header=True)

    print('Dataframe for ', name, 'is DONE')

# Full all dataset.
all_df=pd.concat(data, ignore_index='True')
all_df.columns=columns_void
# Selected total dataframe
sel_all = all_df[all_df['Void'] == 1]

# Fill null values
all_df['Junction'] = all_df['Junction'].fillna(0)
sel_all['Junction'] = sel_all['Junction'].fillna(0)

# Save
p_out1='/home/estanislao/Documents/ML_GB/GrainLearning/output/total_gb_df.csv'
p_out2 = '/home/estanislao/Documents/ML_GB/GrainLearning/output/total_sel_df.csv'
all_df.to_csv(p_out1, header=True)
sel_all.to_csv(p_out2, header=True)
print('Total dataframe is DONE')




