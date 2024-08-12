import pandas as pd
pd.options.plotting.backend = "plotly"
import datetime
import pickle
from skforecast.utils import load_forecaster
import skforecast
from skforecast import preprocessing
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly

class NWDAFDataSet:

  def __init__( self, cell_id, cat_id, pe_id, df):
    self.df = self.format_data_set( self.data_subset( cell_id, cat_id, pe_id, df ) )
    self.id = f"cell_id-{cell_id}--cat_id-{cat_id}--pe_id-{pe_id}"


  def data_subset( self,  cell_id, cat_id, pe_id, df ):
    """return a subset of the dataset """
    df = df[ ( df.cell_id == cell_id ) & ( df.cat_id == cat_id ) & ( df.pe_id == pe_id ) ]
    for col_name in ['cell_id', 'cat_id', 'pe_id' ]:
      df = df.drop( col_name, axis=1 )
    self.df = df.reset_index()
    return df

  def format_data_set( self, df ):
    time_list = df[ 't' ].to_list()
    # print(time_list)
    freq = time_list[ 1 ] - time_list[ 0 ]
    # print(freq)

    date_list = []
    for t in time_list:
      date_list.append( datetime.datetime.fromisoformat('2024-01-01') +\
                             datetime.timedelta( seconds=t ) )
    df[ 't' ] = date_list
    df = df.rename( columns={ 't' : 'date' } )
    df = df.set_index('date')
    df = df.asfreq(f"{freq}s") # 'ms' 'ns'
    df = df.sort_index()
    df = df.rename( columns={ 'load' : 'exog_1' } )
    return df

def get_multi_series_data(df):
    sub_exog_list = []

    cell_id_list = df['cell_id'].unique()
    cat_id_list = df['cat_id'].unique()
    pe_id_list = df['pe_id'].unique()

    for cell_id in cell_id_list:
        for cat_id in cat_id_list:
            for pe_id in pe_id_list:
                # if not df[ ( df.cell_id == cell_id ) & ( df.cat_id == cat_id ) & ( df.pe_id == pe_id ) ].empty:
                data = NWDAFDataSet ( cell_id=cell_id, cat_id=cat_id, pe_id=pe_id, df=df )
                sub_exog = data.df[ [ 'exog_1' ] ].reset_index()
                sub_exog[ 'series_id' ] = data.id
                sub_exog_list.append( sub_exog )

    exog = pd.concat( sub_exog_list )

    exog_dict = skforecast.preprocessing.exog_long_to_dict(
        data      = exog,
        series_id = 'series_id',
        index     = 'date',
        freq      = 'S'
    )

    return exog_dict, exog


def get_prediction( data, steps):
    file_name = '000_multi_serie_forecaster.pickle'
    forecaster = load_forecaster(file_name, verbose=True)
    
    predictions = forecaster.predict( steps=steps, exog=data, suppress_warnings=True )

    return predictions


def get_plot_html(data):
  # Create heatmap
  fig = go.Figure(data=go.Heatmap(
    z=data.values,                  # Values of the heatmap
    x=data.columns,                 # Node names as x-axis labels
    y=data.index,                   # Time as y-axis labels (dates)
    colorscale='Viridis',                    # Color scale
    colorbar=dict(
        title='Anomaly Score',
        tickvals=[0, 0.5, 1],                # Ensure ticks are at 0, 0.5, and 1
        ticktext=['0', '0.5', '1']          # Label for each tick
    ),
    zmin=0,                                  # Set color scale minimum
    zmax=1                                   # Set color scale maximum
  ))

  # Update layout for better readability
  fig.update_layout(
      title='Anomaly Scores Over Time',
      xaxis_title='Nodes',
      yaxis_title='Time',
      yaxis=dict(
          tickmode='auto',
          tickformat='%Y-%m-%d %H-%M-%S',                # Format dates in the y-axis
      )
  )

  # Show the plot
  fig.show()
  fig.write_html('anomaly_scores_heatmap.html')

  graph_html  =  plotly.io.to_html(fig, full_html=False, include_plotlyjs ='cdn' )
  return graph_html