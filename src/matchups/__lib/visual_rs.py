import os
import pandas as pd
import numpy as np
from plotnine import *

class HelperVisualRS:

    def __init__(selfself):
        pass

    def get_reflectance_signature_facet(self, df, facet_column_name) -> ggplot:
        assert('Band' in df.columns), "'Band' column is missing"
        assert ('Reflectance' in df.columns), "'Reflectance' column is missing"

        plot = (ggplot(df, aes(x='Band', y='Reflectance'))
                + geom_point()
                + facet_wrap(f'~{facet_column_name}')  # Added scales='free' to allow individual y-axis scaling
                + labs(title='Reflectance for Each Item', x='Band', y='Reflectance')
                + theme(figure_size=(12, 6),  # Width, height in inches
                        axis_text_x=element_text(size=10),
                        axis_text_y=element_text(size=10),
                        subplots_adjust={'wspace': 0.25}))
        return plot

    def get_reflectance_signature(self, df, band_range, band_vlines, reflectance_range, reflectance_hlines, item_id_column_name) -> ggplot:
        assert('Band' in df.columns), "'Band' column is missing"
        assert ('Reflectance' in df.columns), "'Reflectance' column is missing"
        assert (len(df[f'{item_id_column_name}'].unique()) == 1), "Only one instance is allowed"

        plot = (ggplot(df, aes(x='Band', y='Reflectance'))
                + scale_x_continuous(breaks=band_range)
                + scale_y_continuous(breaks=reflectance_range, limits=[0, np.max(reflectance_range)])
                + theme(aspect_ratio=1
                        #, axis_text_x = element_text(angle=-90)
                        , axis_text_x = element_blank()
                        , axis_text_y = element_blank()
                        , axis_title_x=element_blank()
                        , axis_title_y=element_blank()
                        , panel_grid=element_blank()
                        , panel_background=element_blank()
                        , axis_ticks=element_blank())
                + geom_area(fill='black', alpha=0.1)
                + geom_vline(aes(xintercept='x_coord', color='line_color'), data=band_vlines, show_legend=False, size=0.1)
                + geom_hline(aes(yintercept='y_coord', color='line_color'), data=reflectance_hlines, show_legend=False, size=0.1)
        )
        return plot

    def get_reflectance_signature_facets(self, df, ncol, scale_x_continuous_breaks, scale_y_continuous_breaks) -> ggplot:
        assert('Band' in df.columns), "'Band' column is missing"
        assert ('mean' in df.columns), "'mean' column is missing"
        assert ('std' in df.columns), "'std' column is missing"
        assert ('Cluster_' in df.columns), "'Cluster_' column is missing"

        p = (ggplot(df, aes(x='Band', y='mean'))
                + geom_ribbon(aes(ymin='mean-std*2', ymax='mean+std*2'), fill='lightgrey')
                + geom_line()
                + facet_wrap("~Cluster_", ncol=ncol)
                + scale_x_continuous(breaks=scale_x_continuous_breaks)
                + scale_y_continuous(breaks=scale_y_continuous_breaks)
                + xlab("Band")
                + ylab("Reflectance")
                + theme(
                    axis_text_x=element_text(size=7, rotation=90),
                    axis_text_y=element_text(size=7),
                    strip_text=element_text(size=7)
                )
        )
        return p

    def save_plot(self, plot, path_file, width, height, dpi, format='png') -> None:
        plot.save(filename=path_file, width=width, height=height, dpi=dpi, format=format)
