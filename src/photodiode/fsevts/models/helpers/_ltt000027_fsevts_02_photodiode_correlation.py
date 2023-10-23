import numpy as np
import pandas as pd
import os
import netCDF4 as nc

class Helper:

    def read_photopic(self, _path) -> pd.DataFrame:
        return pd.read_csv(_path, sep='\t', index_col=None, names=['wl_', 'v_lambda_'], usecols=['wl_', 'v_lambda_'],
                           header=0)

    def transform_photopic(self, df_photopic) -> pd.DataFrame:
        # Pivot the dataframe
        df_photopic_ = df_photopic.copy()
        pivoted_result = df_photopic_.pivot_table(index=None, columns='wl_', values='v_lambda_')
        # Reset index and column names
        pivoted_result.reset_index(inplace=True)
        pivoted_result.columns = map(str, pivoted_result.columns)
        pivoted_result.columns.name = None
        return pivoted_result

    def read_monitorpd(self, _path) -> pd.DataFrame:
        df_ = pd.read_csv(_path, skiprows=2, sep='\t', index_col=None, names=['timestamp', 'lx_'], encoding='latin1')
        df_['timestamp_'] = df_['timestamp'].apply(pd.to_datetime)
        df_['utc_'] = df_['timestamp_'].apply(lambda x: int(pd.to_datetime(x).timestamp()))
        return df_[['utc_','lx_']]

    def transform_monitorpd(self, df_monitorpd) -> pd.DataFrame:
        df_monitorpd_ = df_monitorpd.copy()
        df_monitorpd_['lx_inv_'] = 1 / df_monitorpd_['lx_']
        return df_monitorpd_

    def get_list_of_files(self, _path_to_dir) -> map:
        return map(lambda name: os.path.join(_path_to_dir, name), os.listdir(_path_to_dir))

    def get_nc_wavelength(self, _path) -> pd.DataFrame:
        try:
            nc_file = nc.Dataset(_path)
            var_wavelength = nc_file.variables['wavelength']
            df = pd.DataFrame(np.array(var_wavelength))
            df['wl_'] = df[0].apply(lambda x: round(x))
            df['wavelength_'] = df[0]
            nc_file.close()
            return df[['wl_', 'wavelength_']]
        except Exception as e:
            pass

    def get_nc_acquisition_time(self, _path, series_nr=0) -> int:
        try:
            nc_file = nc.Dataset(_path)
            var_acquisition_time = nc_file.variables['acquisition_time']
            df = pd.DataFrame(map(int, np.array(var_acquisition_time)))
            nc_file.close()
            return (df.loc[series_nr, 0])
        except Exception as e:
            pass

    def get_nc_irradiance(self, _path, series_nr=0) -> pd.DataFrame:
        try:
            nc_file = nc.Dataset(_path)
            var_irradiance = nc_file.variables['irradiance']
            df = pd.DataFrame(np.array(var_irradiance))
            at_ = self.get_nc_acquisition_time(_path, series_nr)
            df['utc_'] = at_
            df['irradiance_'] = df[series_nr]
            nc_file.close()
            return df[['utc_', 'irradiance_']]
        except Exception as e:
            pass

    def get_nc_combined_and_transformed(self, df_wavelength, df_irradiance) -> pd.DataFrame:
        df_wavelength_ = df_wavelength.copy()
        df_irradiance_ = df_irradiance.copy()
        df_wavelength_['irradiance_'] = df_irradiance_['irradiance_']
        df_wavelength_['utc_'] = df_irradiance_['utc_']
        df_grouped = df_wavelength_[['wl_', 'irradiance_', 'utc_']].groupby(['utc_', 'wl_'])
        df_grouped = df_grouped['irradiance_'].mean().reset_index()
        # Pivot the dataframe
        pivoted_result = df_grouped.pivot_table(index='utc_', columns='wl_', values='irradiance_')
        # Reset index and column names
        pivoted_result.reset_index(inplace=True)
        pivoted_result.columns.name = None
        return pivoted_result

    def get_nc_transformed_0(self, _path) -> pd.DataFrame:
        try:
            df_wavelength = self.get_nc_wavelength(_path)
            df_irradiance = self.get_nc_irradiance(_path, series_nr=0)
            return self.get_nc_combined_and_transformed(df_wavelength, df_irradiance)
        except Exception as e:
            pass

    def get_nc_transformed_1(self, _path) -> pd.DataFrame:
        try:
            df_wavelength = self.get_nc_wavelength(_path)
            df_irradiance = self.get_nc_irradiance(_path, series_nr=1)
            return self.get_nc_combined_and_transformed(df_wavelength, df_irradiance)
        except Exception as e:
            pass