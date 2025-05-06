# set up
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import pytz
from scipy.io import loadmat
from scipy import signal
import matplotlib.gridspec as gridspec
# relative paths using pyprojroot (see pvwatts_sandbox/paths.py)
from apagon_april28.paths import root, data_dir, shareable_dir, notebooks_dir, figures_dir
from apagon_april28.constants import generation_type_colors, generation_type_column_order # from entsoe
from apagon_april28.constants import pmu_colors, pmu_aliases # from gridradar

# Basic Frequency Plots
## Frequency Plot
def create_frequency_plot(pmu_df, start_time, end_time, pmu_aliases, title_text, ymin=None, ymax=None, events=None):
    
    df_to_plot = pmu_df.loc[start_time:end_time]
    
    fig = go.Figure()

    for pmu, name in pmu_aliases.items():
        fig.add_trace(go.Scatter(
            x=df_to_plot.index,
            y=df_to_plot[pmu],
            mode='lines',
            name=name,
            line=dict(color=pmu_colors[pmu])
        ))

    # Mark +/- 200mHz and +/- 800mHz
    if ymin is None:
        try:
            ymin = round(df_to_plot.min().min() * 10 - 1) / 10
        except:
            ymin = 49.1
    if ymax is None:
        try:
            ymax = round(df_to_plot.max().max() * 10 + 1) / 10
        except:
            ymax = 50.9
    fig.add_hrect(y0=ymin, y1=49.2, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=ymin, y1=49.8, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.2, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.8, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)

    # Note FCR saturation at +/- 200mhz
    fig.add_annotation(
        x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
        y=49.78,
        text="<i>FCR Saturation</i>",
        showarrow=False,
        font=dict(size=12)
    )
    # fig.add_annotation(
    #     x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
    #     y=50.22,
    #     text="<i>FCR Saturation</i>",
    #     showarrow=False,
    #     font=dict(size=12)
    # )

    if events is not None:
        for event in events:
            fig.add_vline(x=event, line_dash="dash", line_color="gray")


    # Update layout
    fig.update_layout(
        title=title_text,
        title_font=dict(size=24),
        xaxis_title=None,
        yaxis_title='Frequency [Hz]',
        yaxis_title_font=dict(size=20),
        yaxis_range=[ymin, ymax],
        showlegend=True,
        legend=dict(
            font=dict(size=24),
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='right',
            x=1
        ),
        xaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        height = 800,
        width = 1600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=90, b=60)
    )
    
    return fig

def generic_frequency_plot(series, start_time, end_time, title_text, ymin=None, ymax=None):
    
    df_to_plot = series.loc[start_time:end_time]
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_to_plot.index,
        y=df_to_plot,
        mode='lines',
        name=title_text,
        line=dict(color='black')
        ))

    # Mark +/- 200mHz and +/- 800mHz
    if ymin is None:
        try:
            ymin = round(df_to_plot.min().min() * 10 - 1) / 10
        except:
            ymin = 49.1
    if ymax is None:
        try:
            ymax = round(df_to_plot.max().max() * 10 + 1) / 10
        except:
            ymax = 50.9
    fig.add_hrect(y0=ymin, y1=49.2, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=ymin, y1=49.8, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.2, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.8, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)

    # Note FCR saturation at +/- 200mhz
    fig.add_annotation(
        x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
        y=49.78,
        text="<i>FCR Saturation</i>",
        showarrow=False,
        font=dict(size=12)
    )
    # fig.add_annotation(
    #     x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
    #     y=50.22,
    #     text="<i>FCR Saturation</i>",
    #     showarrow=False,
    #     font=dict(size=12)
    # )

    # Add a vertical line at 12:33:16.5
    # t_first_event = pd.to_datetime('2025-04-28 12:33:16.5').tz_localize('Europe/Madrid')
    # fig.add_vline(x=t_first_event, line_dash="dash", line_color="gray")

    # t_second_event = pd.to_datetime('2025-04-28 12:33:17.8').tz_localize('Europe/Madrid')
    # fig.add_vline(x=t_second_event, line_dash="dash", line_color="gray")

    # t_france_disconnection = pd.to_datetime('2025-04-28 12:33:20.3').tz_localize('Europe/Madrid')
    # fig.add_vline(x=t_france_disconnection, line_dash="dash", line_color="gray")

    # Update layout
    fig.update_layout(
        title=title_text,
        title_font=dict(size=24),
        xaxis_title=None,
        yaxis_title='Frequency [Hz]',
        yaxis_title_font=dict(size=20),
        yaxis_range=[ymin, ymax],
        showlegend=True,
        legend=dict(
            font=dict(size=24),
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='right',
            x=1
        ),
        xaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            dtick='900000' # 15 minutes in milliseconds
        ),
        yaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        height = 800,
        width = 1600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=90, b=60)
    )
    
    return fig

def plot_N_frequency_comparison(series_to_plot, t_comparison_start=None, t_comparison_end=None):
    """Creates a frequency comparison plot for multiple time series.
    
    Args:
        series_to_plot (dict): Dictionary mapping series names to pandas Series objects
        t_comparison_start (pd.Timestamp, optional): Start time for comparison. Defaults to earliest timestamp.
        t_comparison_end (pd.Timestamp, optional): End time for comparison. Defaults to latest timestamp.
    
    Returns:
        plotly.graph_objects.Figure: The comparison plot figure
    """
    # Set default start/end times if not provided
    if t_comparison_start is None:
        t_comparison_start = min([t_min for t_min in [series.index.min() for series in series_to_plot.values()] if t_min is not None])
    
    if t_comparison_end is None:
        t_comparison_end = max([t_max for t_max in [series.index.max() for series in series_to_plot.values()] if t_max is not None])

    fig = go.Figure()

    for series_name, series in series_to_plot.items():
        fig.add_trace(go.Scatter(
            x=series.loc[t_comparison_start:t_comparison_end].index,
            y=series.loc[t_comparison_start:t_comparison_end],
            mode='lines',
            name=series_name,
        ))

    # Add standard frequency bands
    ymin = 49.75
    ymax = 50.25
    fig.add_hrect(y0=ymin, y1=49.2, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=ymin, y1=49.8, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.2, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=50.8, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)

    # Note FCR saturation
    fig.add_annotation(
        x=list(series_to_plot.values())[0].loc[t_comparison_start:t_comparison_end].index[0] + pd.Timedelta(seconds=0.2),
        y=49.78,
        text="<i>FCR Saturation</i>",
        showarrow=False,
        font=dict(size=12)
    )

    # Update layout
    fig.update_layout(
        title='Frequency Comparison: Toledo vs Malaga',
        title_font=dict(size=24),
        xaxis_title=None,
        yaxis_title='Frequency [Hz]',
        yaxis_title_font=dict(size=20),
        yaxis_range=[ymin, ymax],
        showlegend=True,
        legend=dict(
            font=dict(size=24),
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='right',
            x=1
        ),
        xaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            dtick='900000'  # 15 minutes in milliseconds
        ),
        yaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        height=800,
        width=1600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=90, b=60)
    )

    return fig

## RoCoF Plots
### Comparison Plot
def create_rocof_comparison_plot(pmu_df, start_time, end_time, pmu_aliases, title_text, ymin=None, ymax=None):
    """Creates a plot comparing Rate of Change of Frequency (RoCoF) measurements from multiple PMUs.
    
    Args:
        pmu_df (pd.DataFrame): DataFrame containing PMU frequency measurements, with PMU names as columns
        start_time (pd.Timestamp): Start time for the plot window
        end_time (pd.Timestamp): End time for the plot window  
        pmu_aliases (dict): Dictionary mapping PMU names to display names for the legend
        title_text (str): Title text for the plot
        ymin (float, optional): Minimum y-axis value. Defaults to -1.5 Hz/s if None
        ymax (float, optional): Maximum y-axis value. Defaults to 1.5 Hz/s if None
        
    Returns:
        plotly.graph_objects.Figure: Figure object containing the RoCoF comparison plot with:
            - Line traces for each PMU's RoCoF measurements
            - ENTSO-E RoCoF limit annotations at ±1.25 Hz/s
            - Gray shading for unreliable data regions
            - Customized layout with grid, fonts, and legend
    """
    
    df_to_plot = pmu_df.loc[start_time:end_time]
    
    fig = go.Figure()
    for pmu, name in pmu_aliases.items():
        fig.add_trace(go.Scatter(
            x=df_to_plot.index,
            y=df_to_plot[pmu],
            mode='lines',
            name=name,
            line=dict(color=pmu_colors[pmu])
        ))

    # Plot parameters
    ymin = -1.5
    ymax = 1.5


    # Note unreliable data after 12:33:16.5
    fig.add_vrect(x0=pd.to_datetime('2025-04-28 12:33:23').tz_localize('Europe/Madrid'), x1=end_time, fillcolor="gray", opacity=0.7, line_width=0)
    fig.add_annotation(
        x = end_time,
        y=1.3,
        text="<i>ES_Malaga PMU data<br>is unreliable after blackout</i>",
        showarrow=False,
        font=dict(size=12),
        xanchor='right',
        yanchor='top'
    )

    # Note entso-e RoCoF limit
    fig.add_hrect(y0=ymin, y1=-1.25, fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=1.25, y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)

    fig.add_annotation(
        x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
        y=1.25 + 0.03,
        text="<i>entso-e RoCoF limit</i>",
        showarrow=False,
        font=dict(size=12)
    )
    fig.add_annotation(
        x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
        y=-(1.25 + 0.03),
        text="<i>entso-e RoCoF limit</i>",
        showarrow=False,
        font=dict(size=12)
    )

    # Update layout
    fig.update_layout(
        title=title_text,
        title_font=dict(size=24),
        xaxis_title=None,
        yaxis_title='Rate of Change of Frequency [Hz/s]',
        yaxis_title_font=dict(size=20),
        yaxis_range=[ymin, ymax],
        showlegend=True,
        legend=dict(
            font=dict(size=24),
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='right',
            x=1
        ),
        xaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        height = 800,
        width = 1600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=90, b=60)
    )
    
    return fig


### Closeup Plot
def create_rocof_closeup_plot(rocof_df, start_time, end_time, title_text, ymin=-1.5, ymax=1.5):
    """
    Create a plot comparing different ROCOF calculation window sizes for a given time period.

    Parameters
    ----------
    rocof_df : pandas.DataFrame
        DataFrame containing ROCOF values calculated with different window sizes.
        Expected columns are 'rocof_instantaneous', 'rocof_500ms', 'rocof_1000ms', 'rocof_2000ms'
    start_time : datetime-like
        Start time for the plot window
    end_time : datetime-like
        End time for the plot window
    title_text : str
        Title for the plot
    ymin : float, optional
        Minimum y-axis value, defaults to -1.5 Hz/s
    ymax : float, optional
        Maximum y-axis value, defaults to 1.5 Hz/s

    Returns
    -------
    plotly.graph_objects.Figure
        Figure object containing the ROCOF comparison plot with:
        - Lines for each ROCOF calculation window size in different shades of red
        - Gray shaded region indicating unreliable data after blackout
        - Horizontal bands indicating ENTSO-E ROCOF limits
        - Annotations for data reliability and ROCOF limits
    """
    fig = go.Figure()   

    rocof_colors = {
        'rocof_instantaneous': '#ff3333',  # bright red
        'rocof_500ms': '#ff6666',  # lighter red
        'rocof_1000ms': '#ff9999', # even lighter red
        'rocof_2000ms': '#ffcccc'  # very light red
    }

    df_to_plot = rocof_df.loc[start_time:end_time]

    for column in df_to_plot.columns:
        fig.add_trace(
            go.Scatter(
                x=df_to_plot.index,
                y=df_to_plot[column],
                name=column,
                mode='lines',
                line=dict(color=rocof_colors[column])
            )
        )

    # Note unreliable data after 12:33:16.5
    fig.add_vrect(x0=pd.to_datetime('2025-04-28 12:33:20.4').tz_localize('Europe/Madrid'), x1=end_time, fillcolor="gray", opacity=0.7, line_width=0)
    fig.add_annotation(
        x = end_time,
        y=min(1.3,ymax),
        text="<i>ES_Malaga PMU data<br>is unreliable after blackout</i>",
        showarrow=False,
        font=dict(size=12),
        xanchor='right',
        yanchor='top'
    )

    # Note entso-e RoCoF limit
    fig.add_hrect(y0=ymin, y1=max(ymin, -1.25), fillcolor="gray", opacity=0.1, line_width=0)
    fig.add_hrect(y0=min(ymax, 1.25), y1=ymax, fillcolor="gray", opacity=0.1, line_width=0)

    if ymax > 1.3:
        fig.add_annotation(
            x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
            y=1.28,
            text="<i>ensto-e RoCoF limit (500ms moving average)</i>",
            showarrow=False,
            font=dict(size=12)
        )
    if ymin < -1.25:
        fig.add_annotation(
            x=df_to_plot.index[0] + pd.Timedelta(seconds=0.2),
            y=-1.28,
            text="<i>entso-e RoCoF limit (500ms moving average)</i>",
            showarrow=False,
            font=dict(size=12)
    )

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            font=dict(size=24)
        ),
        xaxis=dict(
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title="ROCOF (Hz/s)",
            tickfont=dict(size=20),
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            range=[ymin, ymax]
        ),
        height=800,
        width=1600,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=50, r=50, t=120, b=60),
        showlegend=True,
        legend=dict(
            font=dict(size=20),
            orientation='h',
            yanchor='bottom',
            y=1.0,
            xanchor='right',
            x=1
        )
    )

    return fig

## Spectrogram
def create_grid_frequency_spectrogram(data, pmu_name, fs=10, window_size=600, overlap=0.75, plot=True):
    """
    Create a spectrogram from grid frequency measurements, focusing on sub-synchronous oscillations.
    
    Parameters:
    -----------
    data : pandas Series or numpy array
        Grid frequency measurements
    fs : float, default=10
        Sampling frequency in Hz
    window_size : int, default=600
        Number of samples in each FFT window (60 seconds at 10 Hz)
    overlap : float, default=0.75
        Overlap between consecutive windows (75% overlap)
    plot : bool, default=True
        Whether to plot the results
        
    Returns:
    --------
    dict : Dictionary containing spectrogram data
    """
    # Ensure data is a numpy array
    y = np.array(data)
    
    # Use just frequency error (remove 50 Hz)
    y = y - 50
    
    # Calculate parameters for spectrogram
    nperseg = window_size
    noverlap = int(nperseg * overlap)
    
    # Create spectrogram
    f, t, Sxx = signal.spectrogram(
        y, 
        fs=fs, 
        window='hann',
        nperseg=nperseg, 
        noverlap=noverlap, 
        detrend='constant',
        scaling='density'
    )
    
    # Calculate total duration in hours:minutes:seconds
    total_duration_sec = len(y) / fs
    hours = int(total_duration_sec // 3600)
    minutes = int((total_duration_sec % 3600) // 60)
    seconds = int(total_duration_sec % 60)
    date = data.index[0].strftime('%Y-%m-%d')
    
    if plot:
        # Create the plot
        fig = plt.figure(figsize=(14, 10))
        gs = gridspec.GridSpec(2, 2, width_ratios=[20, 1], height_ratios=[1, 1], wspace=0.05)
        
        # Plot 1: Original time series
        ax1 = plt.subplot(gs[0, 0])
        time = np.arange(len(y)) / fs   # Time in seconds
        t_datetime = [data.index[0] + pd.Timedelta(seconds=t) for t in time]

        ax1.plot(time, y+50)
        ax1.grid(True)
        #ax1.set_xlabel('Time (minutes)')
        ax1.set_xlim([0, 20.5])
        ax1.set_xticks(time[::len(time)//6])  # Show 6 ticks
        ax1.set_xticklabels([t.strftime('%H:%M') for t in t_datetime[::len(time)//6]])
        ax1.set_ylabel('Frequency (Hz)')
        ax1.set_title(f'Grid Frequency Measurements | {pmu_name} | {date}')
        
        # Plot 2: Spectrogram, focusing on the range of interest
        ax2 = plt.subplot(gs[1, 0])
        mask = (f >= 0.05) & (f <= 0.3)
        pcm = ax2.pcolormesh(t, f[mask], 10 * np.log10(Sxx[mask]), 
                             shading='gouraud', cmap='viridis')
        ax2.set_ylabel('Frequency (Hz)')
        # ax2.set_xlabel('Time (minutes)')
        # ax2.set_xlim([0, 20.33333333333])
        # ax2.set_xticks(time[::len(time)//6])  # Show 6 ticks
        ax2.set_xticklabels([t.strftime('%H:%M') for t in t_datetime[::len(time)//6]])
        ax2.set_title(f'Spectrogram: Sub-synchronous Oscillations (window size: {window_size/(fs)} seconds)')
        
        # Colorbar in its own axes
        cax = plt.subplot(gs[1, 1])
        plt.colorbar(pcm, cax=cax, label='Power/Frequency (dB/Hz)')
        
        plt.tight_layout()
        #plt.show()
    
    return {
        'fig': fig,
        'frequencies': f,
        'times': t,
        'power': Sxx,
        'fs': fs,
        'window_size': window_size,
        'overlap': overlap
    }


