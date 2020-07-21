import streamlit as st
import pandas as pd
import json
import os

from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

from dummy_mnist import main as mnist_generate


def read_json(filename='output.json'):
    '''
    Read the `.json` file specified by filename and return
    the deserialization according to the json module
    '''
    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


st.sidebar.markdown('# Program Arguments')
type_algorithm = st.sidebar.selectbox('type', ['pca', 'tsne', 'umap'])
dimensions = st.sidebar.selectbox('dimensions', [2, 3])
seed = st.sidebar.number_input('seed', value=42)
output_path = os.path.join(
    'output',
    st.sidebar.text_input('output file', 'output.json')
)

st.sidebar.markdown('### Generated Arguments')
args = {
    'type': type_algorithm,
    'dims': dimensions,
    'seed': seed,
    'output': output_path,
}
st.sidebar.json(args)

data = {'x_coords': [], 'y_coords': [], 'label': [], 'color': []}

color_map = {
    0: '#171614',
    1: '#3AFF18',
    2: '#754043',
    3: '#9A8873',
    4: '#DD423D',
    5: '#547AA5',
    6: '#50D8D7',
    7: '#BBBDF6',
    8: '#9893DA',
    9: '#5398BE',
}

with st.spinner('Loading data...'):
    mnist_generate(args)
    json_obj = read_json(output_path)
    for entry in json_obj:
        data['x_coords'].append(entry['x'][0])
        data['y_coords'].append(entry['x'][1])
        data['label'].append(entry['y'])
        data['color'].append(color_map[entry['y']])
st.success('Data loaded successfully!')

st.markdown('# Graph')
data_source = ColumnDataSource(data)
p = figure(title=f'MNIST Graph by {type_algorithm}', x_axis_label='x', y_axis_label='y')
p.circle(x='x_coords', y='y_coords', line_width=3, source=data_source, color='color', legend='label')
p.legend.location = 'top_right'

hover = HoverTool()
hover.tooltips = '''
    <div>X: @x_coords</div>
    <div>Y: @y_coords</div>
    <div>Label: @label</div>
    <div style="color: @color;">@color</div>
'''
p.add_tools(hover)
st.bokeh_chart(p)

st.markdown('### Raw Data')
st.dataframe(data, width=1200)
