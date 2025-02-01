from config import *
import data as dd
import model as mo
import visualization as vis
import matplotlib.pyplot as plt

pems_meta = dd.read_pems_meta(dir_pems_meta)
pems_ave_speed = dd.unzip_pems_speed(
    dir_pems_speed, dir_cache, dd.get_pems_5min_speed_ave,
    # [
    #     '20230308', '20230309', '20230310', '20230311', '20230312',
    # ]
)

### data processing

crime_pred = mo.TransPred()
crime_pred.build_adj()
crime_pred.build_dataset(train_x, train_y, val_x, val_y, test_x, test_y)
crime_pred.build_model(1, 1,)
crime_pred.train_model(16, 0.002, 500, dir_cache)
pred, true = crime_pred.pred_trans_test_set(dir_cache)

crime_pred_tuner = mo.TransPredTuner()
crime_pred_tuner.build_adj(crime_data.polygon.to_crs('EPSG:4326'), 'Queen')
crime_pred_tuner.build_dataset(train_x, train_y, val_x, val_y, test_x, test_y)
crime_pred_tuner.run_study()





print()