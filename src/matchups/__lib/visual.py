import os
import pandas as pd
import numpy as np
from plotnine import *

class HelperVisual:

    def __init__(self):
        pass

    def get_all_filepaths_by_extension(self, path_to_dir, extension) -> list:
        _filePaths = []

        for _dirpath, _dirnames, _filenames in os.walk(path_to_dir):
            for _filename in _filenames:
                if _filename.endswith(extension) and not _filename.startswith('.'):
                    _filePaths.append(os.path.join(_dirpath, _filename))
        return _filePaths

    def get_pca_plot(self, pca) -> ggplot:
        # Calculate explained variance
        """
            import pandas as pd
            from sklearn.datasets import make_blobs
            from plotnine import *
            from models.datamanager.__lib._util import visual as _helper_visual
            from sklearn.preprocessing import StandardScaler
            from sklearn.decomposition import PCA

            X, _ = make_blobs(n_samples=100, n_features=298, centers=4, random_state=42)

            # Standardize the data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)

            helper_visual = _helper_visual.HelperVisual()

            helper_visual.get_pca_plot(pca).draw()
        """
        exp_var = pca.explained_variance_ratio_
        cum_exp_var = np.cumsum(exp_var)

        # Prepare a DataFrame for plotnine
        exp_var_df = pd.DataFrame({
            'Principal Component': np.arange(1, len(exp_var) + 1),
            'Individual Explained Variance': exp_var,
            'Cumulative Explained Variance': cum_exp_var
        })

        # Calculate percentage labels for annotation
        exp_var_df['Percentage Label'] = (exp_var_df['Cumulative Explained Variance'] * 100).round(1).astype(str) + '%'

        # Melt the DataFrame for plotnine
        exp_var_melted = exp_var_df.melt(id_vars=['Principal Component', 'Percentage Label'],
                                         value_vars=['Individual Explained Variance',
                                                     'Cumulative Explained Variance'],
                                         var_name='Variance Type',
                                         value_name='Explained Variance')

        # Plot with plotnine
        plot = (ggplot(exp_var_melted)
                + geom_bar(aes(x='Principal Component',
                               y='Explained Variance',
                               fill='Variance Type'),
                           data=exp_var_melted[exp_var_melted['Variance Type'] == 'Individual Explained Variance'],
                           stat="identity",
                           position=position_dodge(width=0.8))
                + geom_line(aes(x='Principal Component',
                                y='Explained Variance',
                                group=1,
                                color='Variance Type'),
                            data=exp_var_melted[exp_var_melted['Variance Type'] == 'Cumulative Explained Variance'])
                + geom_point(aes(x='Principal Component',
                                 y='Explained Variance',
                                 color='Variance Type'),
                             data=exp_var_melted[exp_var_melted['Variance Type'] == 'Cumulative Explained Variance'])
                + geom_text(aes(x='Principal Component',
                                y='Explained Variance',
                                label='Percentage Label'),
                            va='bottom',
                            nudge_y=0.02)
                + scale_fill_manual(values=['lightsalmon', '#00B9FF'])
                + scale_color_manual(values=['black', '#00B9FF'])
                + labs(title='Cumulative Explained Variance Plot for PCA',
                       x='Principal Component Number',
                       y='Explained Variance')
                + theme_minimal()
                + theme(legend_title=element_blank(), legend_position='top')
                + guides(color=False)
                )
        return plot

    def get_line_plot(self, df, x_name, y_name, xlab_name, ylab_name, x_continuous_breaks):
        p = (ggplot(df, aes(x=x_name, y=y_name))
                + geom_line()
                + geom_point()
                + scale_x_continuous(breaks=x_continuous_breaks)
                + xlab(xlab_name)
                + ylab(ylab_name)
                + theme(
            axis_text_x=element_text(size=7),
            axis_text_y=element_text(size=7),
            strip_text=element_text(size=7)
            )
        )
        return p

    def get_line_facets_plot(self, df, ncol, x_name, y_name, facet_name, xlab_name, ylab_name, x_continuous_breaks):
        p = (ggplot(df, aes(x=x_name, y=y_name))
             + geom_line()
             + geom_point()
             + facet_wrap(facet_name, ncol=ncol)
             + scale_x_continuous(breaks=x_continuous_breaks)
             + scale_y_continuous(labels=lambda y: [f"{val / 1e6:.1f}e6" for val in y])  # Format y-axis labels
             + xlab(xlab_name)
             + ylab(ylab_name)
             + theme(
                    axis_text_x=element_text(size=7),
                    axis_text_y=element_text(size=7),
                    strip_text=element_text(size=7)
                )
             )
        return p