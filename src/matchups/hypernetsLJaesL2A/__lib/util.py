import numpy as np
import pandas as pd
import os
import netCDF4 as nc

class HelperUtil:

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

    def get_nc_reflectance(self, _path) -> pd.DataFrame:
        try:
            nc_file = nc.Dataset(_path)
            var_reflectance = nc_file.variables['reflectance']
            df = pd.DataFrame(np.array(var_reflectance))
            df['refl_'] = df[0].apply(lambda x: round(x))
            df['reflectance_'] = df[0]
            nc_file.close()
            return df[['refl_', 'reflectance_']]
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

    def get_nc_viewing_azimuth_angle(self, _path, series_nr=0) -> float:
        try:
            nc_file = nc.Dataset(_path)
            var_viewing_azimuth_angle = nc_file.variables['viewing_azimuth_angle']
            df = pd.DataFrame(map(int, np.array(var_viewing_azimuth_angle)))
            nc_file.close()
            return (df.loc[series_nr, 0])
        except Exception as e:
            pass

    def get_nc_viewing_zenith_angle(self, _path, series_nr=0) -> float:
        try:
            nc_file = nc.Dataset(_path)
            var_viewing_zenith_angle = nc_file.variables['viewing_zenith_angle']
            df = pd.DataFrame(map(int, np.array(var_viewing_zenith_angle)))
            nc_file.close()
            return (df.loc[series_nr, 0])
        except Exception as e:
            pass

    def get_nc_combined_and_transformed(self, df_wavelength, df_reflectance, int_acquisitiontime,
                                        float_viewingazimuthangle, float_viewingzenithangle) -> pd.DataFrame:
        df_wavelength_ = df_wavelength.copy()
        df_reflectance_ = df_reflectance.copy()
        df_wavelength_['reflectance_'] = df_reflectance_['reflectance_']
        df_wavelength_['utc_'] = int_acquisitiontime
        df_wavelength_['viewing_azimuth_angle_'] = float_viewingazimuthangle
        df_wavelength_['viewing_zenith_angle_'] = float_viewingzenithangle
        df_wavelength_['utc_'] = int_acquisitiontime
        df_grouped = df_wavelength_[['wl_', 'reflectance_', 'utc_', 'viewing_azimuth_angle_', 'viewing_zenith_angle_']].groupby(['utc_', 'wl_', 'viewing_azimuth_angle_', 'viewing_zenith_angle_'])
        df_grouped = df_grouped['reflectance_'].mean().reset_index()
        # Pivot the dataframe
        pivoted_result = df_grouped.pivot_table(index=['utc_', 'viewing_azimuth_angle_', 'viewing_zenith_angle_'], columns='wl_', values='reflectance_')
        # Reset index and column names
        pivoted_result.reset_index(inplace=True)
        pivoted_result.columns.name = None
        return pivoted_result

    def get_nc_transformed(self, _path) -> pd.DataFrame:
        try:
            df_wavelength = self.get_nc_wavelength(_path)
            df_reflectance = self.get_nc_reflectance(_path)
            int_acquisitiontime = self.get_nc_acquisition_time(_path)
            float_viewingazimuthangle = self.get_nc_viewing_azimuth_angle(_path)
            float_viewingzenithangle = self.get_nc_viewing_zenith_angle(_path)
            return self.get_nc_combined_and_transformed(df_wavelength, df_reflectance, int_acquisitiontime,
                                                        float_viewingazimuthangle, float_viewingzenithangle)
        except Exception as e:
            pass
