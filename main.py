from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
import json


def read_json(filename='output.json'):
    '''
    Read the `.json` file specified by filename and return
    the deserialization according to the json module
    '''
    with open(filename, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def main():
    '''
    Generate a Bokeh chart based on a specified `.json` file
    '''
    json_obj = read_json()
    data = {
        'x_coords': [],
        'y_coords': [],
        'label': []
    }

    for entry in json_obj:
        data['x_coords'].append(entry['x'][0])
        data['y_coords'].append(entry['x'][1])
        data['label'].append(entry['y'])

    data_source = ColumnDataSource(data)

    p = figure(title='proof of concept', x_axis_label='x', y_axis_label='y')
    p.circle(x='x_coords', y='y_coords', line_width=3, source=data_source)

    hover = HoverTool()
    hover.tooltips = '''
        <div>X: @x_coords</div>
        <div>Y: @y_coords</div>
        <div>Label: @label</div>
    '''
    p.add_tools(hover)

    # save the results
    output_file('output.html')
    save(p)


if __name__ == '__main__':
    main()
