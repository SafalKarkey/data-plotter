#Graph plotter for sensor values read from ESP32

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys

max_val = 3000
min_val = 1800

def scale_func(y_values, min, max):
    mid_val = (max + min)/2
    length = len(y_values)
    length = length - 1
    high_diff = max - y_values.iloc[0]

    y_values += high_diff
    low_diff = - min + y_values.iloc[length]
    y_values -= ((low_diff)/2)
    y_values -= mid_val
    new_max_value = y_values.iloc[0]
    scaling_fac = (max - mid_val)/new_max_value
    y_values *= scaling_fac
    y_values += mid_val

    return y_values


def plotter(filepaths):
    # Create an empty figure
    fig = go.Figure()

    # Define a color cycle for lines
    colors = px.colors.qualitative.Set1

    # Max and Min values
    mid_val = (max_val + min_val)/2

    # Iterate through each file
    for i, filepath in enumerate(filepaths):
        column_names = ['X-Value', 'Y-Value']
        df = pd.read_csv(filepath, header=None, names=column_names)

        df['Y-Value'] = scale_func(df['Y-Value'], min_val, max_val)

        trace = go.Scatter(x=df['X-Value'], y=df['Y-Value'], mode='lines',
                           line=dict(color=colors[i % len(colors)]),
                           name=f'Sensor {i+1}',
                           visible='legendonly')

        fig.add_trace(trace)

    #Buttons to show or hide all the subgraphs
    buttons = [dict(label='Show all', method='update', args=[{'visible': [True] * len(filepaths)}])]
    buttons.append(dict(label='Hide all', method='update', args=[{'visible': [False] * len(filepaths)}]))
    fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=buttons)])

    #################### Add horizontal dotted lines ########################
    fig.add_shape(type="line", x0=min(df['X-Value']), x1=max(df['X-Value']), y0=max_val, y1=max_val,
                      line=dict(color="black", width=1, dash="dot"))

    fig.add_shape(type="line", x0=min(df['X-Value']), x1=max(df['X-Value']), y0=min_val, y1=min_val,
                  line=dict(color="black", width=1, dash="dot"))              

    fig.add_shape(type="line", x0=min(df['X-Value']), x1=max(df['X-Value']), y0=mid_val, y1=mid_val,
                  line=dict(color="black", width=1, dash="dot"))              
    ##########################################################################
    fig.show()

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <filepath1> <filepath2> ... <filepathN>")
        return
    filepaths = sys.argv[1:]
    plotter(filepaths)

if __name__ == "__main__":
    main()
