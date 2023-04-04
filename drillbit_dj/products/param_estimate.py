from multiprocessing import Process, Queue, Pool
import scipy.stats as scist
import time
import itertools as it
import numpy as np
import pandas as pd

from products.models import WeatherData, WeatherStation

def estimate_parameters(queue, diurnal_key, station_id):
    datas = diurnal_key[station_id]
    dfs = []
    months = []
    for data in datas:
        df = pd.DataFrame(data['data']) \
            .set_index('Hour')
        month = pd.Period(data['period'], freq='M', year=2022)
        months.append(month)
        dfs.append(df)

    df = pd.concat(dfs, keys=months, names=['Month', 'Hour']).sort_index()
    temps = df.values.reshape(-1, 24, 6)

    q = [.1, .25, .5, .75, .9]
    degs_of_f = np.arange(1,30)
    variances = np.arange(2,12,.1)
    params = list(it.product(degs_of_f, variances))
    estimates = np.zeros((len(params), *temps.shape[:2], len(q)))
    for i in range(len(params)):
        df, var = params[i]
        for (j, k), mean_temp in np.ndenumerate(temps[:, :, 0]):
            estimates[i, j, k] = scist.t(df, loc=mean_temp, scale=var).ppf(q)

    errors = temps[:, :, 1:] - estimates
    sq_errs = errors**2
    std_errs = sq_errs.sum(axis=3) / len(q)
    idx_of_optimal_params = std_errs.argmin(axis=0)

    params_est = np.zeros_like(idx_of_optimal_params, dtype=object)
    for (m, hr), val in np.ndenumerate(idx_of_optimal_params):
        df, var = params[val]
        params_est[m,hr] = float(df), float(var)

    queue.put(station_id, params_est)

def get_parameters_for_all_weather_stations():
    all_diurnal = WeatherData.objects.filter(
        type='diurnal',
        variable='Dry-Bulb'
    )

# all_diurnal = WeatherData.objects.filter(
#     type='diurnal',
#     variable='Dry-Bulb'
# )

# diurnal_key = {}
# for diurnal in all_diurnal:
#     if diurnal.station_id not in diurnal_key:
#         diurnal_key[diurnal.station_id] = [{'period': diurnal.period, 'data': diurnal.data}]
#     else:
#         diurnal_key[diurnal.station_id].append({'period': diurnal.period, 'data': diurnal.data})

# stations = WeatherStation.objects.filter(region='Texas')
# has_stations = WeatherData.objects.filter(
#     type='month-hour-params-students-t',
#     variable='Dry-Bulb',
# ).values_list('station', flat=True)
# stations = stations.exclude(id__in=has_stations)
# station_ids = stations.values_list('id', flat=True)

# results = {}
# for station_id in tqdm(station_ids):
#     station_id, params_est = estimate_parameters(diurnal_key, station_id)
#     results[station_id] = params_est.tolist()

# for station_id, params_est in results.items():
#     station = stations.get(id=station_id)
#     weather_data = WeatherData(
#         station=station,
#         type='month-hour-params-students-t',
#         variable='Dry-Bulb',
#         data=params_est
#     )
#     weather_data.save()

# q = [.1, .25, .5, .75, .9]
# variances = np.arange(2,8,.1)
# estimates = np.zeros((variances.size, *temps.shape[:2], len(q)))

# for i in trange(variances.size):
#     var = variances[i]
#     for (j, k), mean_temp in np.ndenumerate(temps[:, :, 0]):
#         estimates[i, j, k] = scist.norm(mean_temp, var).ppf(q)

# errors = temps[:, :, 1:] - estimates
# sq_errs = errors**2
# std_errs = sq_errs.sum(axis=3) / len(q)
# idx_of_optimal_var = std_errs.argmin(axis=0)
# optimal_vars = variances[idx_of_optimal_var]