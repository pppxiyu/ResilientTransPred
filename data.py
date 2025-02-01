import pandas as pd
import geopandas as gpd


def unzip_pems_speed(dir_pems, dir_cache, func, date_select=None):
    import os
    import gzip

    df_list = []
    for filename in os.listdir(dir_pems):
        if date_select is not None:
            if "".join(filename.split('.')[0].split('_')[-3:]) not in date_select:
                continue
        if filename.endswith(".gz"):
            filepath = os.path.join(dir_pems, filename)
            with gzip.open(filepath, 'rt') as file:
                df = pd.read_csv(file, header=None)
                df = df.rename(columns={
                    df.columns[0]: 'timestamp', df.columns[1]: 'station', df.columns[2]: 'district',
                    df.columns[3]: 'freeway_number', df.columns[4]: 'direction', df.columns[5]: 'lane_type',
                    df.columns[6]: 'station_length', df.columns[7]: 'samples', df.columns[8]: 'percent_observed',
                    df.columns[9]: 'total_flow', df.columns[10]: 'ave_occupancy', df.columns[11]: 'ave_speed',
                    df.columns[12]: 'lane_n_samples', df.columns[13]: 'lane_n_flow', df.columns[14]: 'lane_n_ave_occu',
                    df.columns[15]: 'lane_n_ave_speed', df.columns[16]: 'lane_n_observed',
                })
                df = func(df)
                df_list.append(df)
    df = pd.concat(df_list, ignore_index=True)

    # save_path = os.path.join(
    #     dir_cache,
    #     f"pems_{filename.split('_')[0]}"
    #     f"_{df.iloc[0][0].split(' ')[0].replace('/', '')}"
    #     f"_{df.iloc[-1][0].split(' ')[0].replace('/', '')}.csv")
    # if not os.path.exists(save_path):
    #     df.to_csv(save_path, index=False)
    #     print(f"Process PEMS data saved to {save_path}")
    # else:
    #     print(f"Process PEMS data already exists: {save_path}")
    return df


def read_pems_meta(dir_pems_meta):
    from shapely.geometry import Point
    df = pd.read_csv(dir_pems_meta, delimiter="	")
    geometry = [Point(xy) for xy in zip(df["Longitude"], df["Latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
    return gdf


def get_pems_day_speed_ave(df, sample_rate=0.1):
    import math
    df = df[['timestamp', 'ave_speed']]
    df = df[~df['ave_speed'].isna()]
    mean_value = df[['ave_speed']].sample(math.floor(len(df) * sample_rate)).mean()
    df_out = pd.DataFrame({'timestamp': df['timestamp'].iloc[0],'ave_speed': [mean_value.values[0]],})
    return df_out


def get_pems_5min_speed_ave(df, sample_rate=0.1):
    df = df[['timestamp', 'ave_speed']]
    df = df[~df['ave_speed'].isna()]
    df_sample = df.groupby('timestamp').sample(frac=sample_rate)
    mean_values = df_sample.groupby('timestamp').mean()
    return mean_values