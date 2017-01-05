import os , pickle
import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure


base_path = '/Users/julienschroder/Desktop/data/'
domain = 'IEM_Domain'
metric = 'total_area_burned'
scenarios = ['rcp45','rcp85']


def get_dataset(dic ,selection , scenario = scenarios):
    def _get_mean_cumsum(df ,name):
        _df = pd.DataFrame(df)
        _df = _df.mean(axis = 1).cumsum(axis=0)
        _df = _df.to_frame(name=name)
        return _df

    data = { scenario : pd.concat([_get_mean_cumsum(dic[model] , model) for model in selection if scenario in model ] ,axis=1)  for scenario in scenarios }

    return data

def make_plot(source, title):
    plot = figure(x_axis_type="datetime", plot_width=800, tools="")
    plot.title.text = title

    for col in source['rcp45']:
        plot.line(source['rcp45'].index,source['rcp45'][col] )

    for col in source['rcp85']:
        plot.line(source['rcp85'].index , source['rcp85'][col])

    # fixed attributes
    plot.xaxis.axis_label = 'Year'
    plot.yaxis.axis_label = "Area burned (km)"
    plot.axis.axis_label_text_font_style = "bold"

    return plot

def update_plot(attrname, old, new):
    rcp45 = rcp45_select.value
    rcp85 = rcp85_select.value

    source = get_dataset(dic,[rcp45 ,rcp85])
    print(source) # <- gets updated properly after dropdown action

rcp45 = 'CCSM4_rcp45'
rcp85 = 'CCSM4_rcp85'

# dic = pickle.load(open(os.path.join(base_path , "_".join([domain , metric ]) + '.p'), 'rb'),encoding='latin1')

dic = pickle.load(open('IEM_Domain_total_area_burned.p', 'rb'),encoding='latin1')

rcp45_models = [ i for i in dic.keys() if 'rcp45' in i]
rcp85_models = [ i for i in dic.keys() if 'rcp85' in i]

rcp45_select = Select(value=rcp45, title='RCP 45', options=sorted(rcp45_models))
rcp85_select = Select(value=rcp85, title='RCP 85', options=sorted(rcp85_models))

source = get_dataset(dic,[rcp45 ,rcp85])

plot = make_plot(source , "Total area burned ")


rcp45_select.on_change('value', update_plot)
rcp85_select.on_change('value', update_plot)

controls = column(rcp45_select, rcp85_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "Total Area burned"






