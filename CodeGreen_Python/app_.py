import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import base64

app = dash.Dash(__name__)

emission = html.Div(id='emitted')
metadata = html.Div(id='metadata')
averageData = html.Div(id='averageData')

data = None

@app.callback(
    [Output('head', 'style'),
     Output('head2', 'style')],
    [Input('btn', 'n_clicks')],
    prevent_initial_call=True
)
def show_hide_graphs(n_clicks):
    if n_clicks is None:
        return {'visibility': 'hidden'}, {'visibility': 'hidden'}
    else:
        return {'visibility': 'visible'}, {'visibility': 'visible'}
    

@app.callback(
    Output('projectDropdown', 'options'),
    [Input('csvFile', 'contents')],
    prevent_initial_call=True
)
def update_project_dropdown(contents):
    global data
    if contents is not None:
        decoded_content = base64.b64decode(contents.split(',')[1]).decode('utf-8')
        data = parse_csv(decoded_content)
        unique_project_names = list({d['project_name'] for d in data})
        return [{'label': name, 'value': name} for name in unique_project_names]
    return []
    


@app.callback(
    [Output('metadata', 'children',allow_duplicate=True),
     Output('emissionRateChart', 'figure',allow_duplicate=True),
     Output('energyComparisonChart', 'figure', allow_duplicate=True),
     Output('powerComparisonChart', 'figure', allow_duplicate=True),
     Output('averageData', 'children',allow_duplicate=True)],
    [Input('btn', 'n_clicks')],
    [State('csvFile', 'contents')],
    prevent_initial_call=True
)
def handle_csv_upload(n_clicks, file):
    global data
    if n_clicks is None or file is None:
        return html.Div(), go.Figure(), go.Figure(), go.Figure(), html.Div()

    decoded_content = base64.b64decode(file.split(',')[1]).decode('utf-8')
    data = parse_csv(decoded_content)

    metadata = generate_metadata(data)
    emission_rate_chart = plot_emission_rate(data)
    energy_comparison_chart = plot_energy_comparison(data)
    power_comparison_chart = plot_power_comparison(data)
    average_data = display_sum(data)

    return metadata, emission_rate_chart, energy_comparison_chart, power_comparison_chart, average_data


def parse_csv(csv):
    lines = csv.splitlines()
    delimiter = ';' if ';' in lines[0] else ','
    headers = lines[0].split(delimiter)
    data = []

    for line in lines[1:]:
        row = line.replace('"', '').split(delimiter)
        rowData = {header: value.strip() for header, value in zip(headers, row) if value.strip() != ''}
        if any(rowData.values()):
            data.append(rowData)

    return data


def generate_metadata(data):
    osVersion = data[0]['os']
    pythonVersion = data[0]['python_version']
    cpuCount = data[0]['cpu_count']
    cpuModel = data[0]['cpu_model']
    gpuCount = data[0]['gpu_count']
    gpuModel = data[0]['gpu_model']
    longitude = data[0]['longitude']
    latitude = data[0]['latitude']
    ramTotalSize = data[0]['ram_total_size']
    trackingMode = data[0]['tracking_mode']

    metadata = html.Div(
        id='container',
        children=[
            html.H3('Metadata:'),
            html.Div(f'OS Version: {osVersion}'),
            html.Div(f'Python Version: {pythonVersion}'),
            html.Div(f'Number of CPUs: {cpuCount}'),
            html.Div(f'CPU Model: {cpuModel}'),
            html.Div(f'Number of GPUs: {gpuCount}'),
            html.Div(f'GPU Model: {gpuModel}'),
            html.Div(f'Longitude: {longitude}'),
            html.Div(f'Latitude: {latitude}'),
            html.Div(f'RAM Total Size: {ramTotalSize} GB'),
            html.Div(f'Tracking Mode: {trackingMode}'),
        ]
    )

    return metadata


def plot_emission_rate(data):
    dates = [d['timestamp'] for d in data]
    emissionRates = [float(d['emissions_rate']) for d in data]

    trace = go.Scatter(
        x=dates,
        y=emissionRates,
        mode='lines',
        name='Emission Rate',
        marker=dict(
            color='#009193'
        )
    )

    layout = go.Layout(
        xaxis=dict(title='Time', gridcolor='#232323'),
        yaxis=dict(title='Emission Rate', gridcolor='#232323'),
        font=dict(
            size=10,
            color='white'
        ),
        plot_bgcolor='#222',
        paper_bgcolor='#222',
    )

    fig = go.Figure(data=[trace], layout=layout)
    return fig


def plot_energy_comparison(data):
    energyConsumption = [float(d['energy_consumed']) for d in data]
    ramEnergy = [float(d['ram_energy']) for d in data]
    gpuEnergy = [float(d['gpu_energy']) for d in data]
    cpuEnergy = [float(d['cpu_energy']) for d in data]

    trace1 = go.Scatter(
        x=energyConsumption,
        y=ramEnergy,
        mode='lines',
        name='RAM Energy',
        marker=dict(
            color='#1C82AD'
        )
    )

    trace2 = go.Scatter(
        x=energyConsumption,
        y=gpuEnergy,
        mode='lines',
        name='GPU Energy',
        marker=dict(
            color='#4E9F3D'
        )
    )

    trace3 = go.Scatter(
        x=energyConsumption,
        y=cpuEnergy,
        mode='lines',
        name='CPU Energy',
        marker=dict(
            color='#C147E9'
        )
    )

    layout = go.Layout(
        xaxis=dict(title='Energy Consumption', gridcolor='#232323'),
        yaxis=dict(title='Energy', gridcolor='#232323'),
        font=dict(
            size=10,
            color='white'
        ),
        plot_bgcolor='#222',
        paper_bgcolor='#222'
    )

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    return fig


def plot_power_comparison(data):
    powerConsumption = [float(d['energy_consumed']) for d in data]
    ramPower = [float(d['ram_power']) for d in data]
    gpuPower = [float(d['gpu_power']) for d in data]
    cpuPower = [float(d['cpu_power']) for d in data]

    trace1 = go.Bar(
        x=powerConsumption,
        y=[sum(ramPower)],
        name='RAM Power',
        marker=dict(
            color='#1C82AD'
        )
    )

    trace2 = go.Bar(
        x=powerConsumption,
        y=[sum(gpuPower)],
        name='GPU Power',
        marker=dict(
            color='#4E9F3D'
        )
    )

    trace3 = go.Bar(
        x=powerConsumption,
        y=[sum(cpuPower)],
        name='CPU Power',
        marker=dict(
            color='#C147E9'
        )
    )

    layout = go.Layout(
        barmode='group',
        xaxis=dict(title='Power Consumption', gridcolor='#232323'),
        yaxis=dict(title='Power', gridcolor='#232323'),
        font=dict(
            size=10,
            color='white'
        ),
        plot_bgcolor='#222',
        paper_bgcolor='#222'
    )

    fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
    return fig


def display_sum(data):
    energyValues = [float(d['energy_consumed']) for d in data]
    emissionValues = [float(d['emissions']) for d in data]
    durationValues = [float(d['duration']) for d in data]

    averageEnergy = sum(energyValues)
    averageEmission = sum(emissionValues)
    averageDuration = sum(durationValues)

    average_data = html.Div(
        id='head',
        children=[
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageEnergy:.5f}', id='avgNum'),
                            html.Span('kwh')
                        ]
                    ),
                    html.H3('Energy Consumed')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageEmission:.5f}', id='avgNum'),
                            html.Span('Kg.Eq.CO2')
                        ]
                    ),
                    html.H3('Emissions Produced')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageDuration:.2f}', id='avgNum'),
                            html.Span('Sec')
                        ]
                    ),
                    html.H3('Duration')
                ]
            )
        ]
    )

    return average_data

def display_average(data):
    energy_values = [float(d['energy_consumed']) for d in data]
    emission_values = [float(d['emissions']) for d in data]
    duration_values = [float(d['duration']) for d in data]

    average_energy = sum(energy_values) / len(energy_values)
    average_emission = sum(emission_values) / len(emission_values)
    average_duration = sum(duration_values) / len(duration_values)

    average_data = html.Div(
        id='head',
        children=[
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{average_energy:.5f}', id='avgNum'),
                            html.Span('kwh')
                        ]
                    ),
                    html.H3('Energy Consumed')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{average_emission:.5f}', id='avgNum'),
                            html.Span('Kg.Eq.CO2')
                        ]
                    ),
                    html.H3('Emissions Produced')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{average_duration:.2f}', id='avgNum'),
                            html.Span('Sec')
                        ]
                    ),
                    html.H3('Duration')
                ]
            )
        ]
    )

    return average_data



app.layout = html.Div(
    children=[
        html.H1('Carbon Emission'),
        html.Div(
            id='head1',
            children=[
                html.Div(
                    id='inputElements',
                    children=[
                        html.Div(
                            id='csvForm',
                            children=[
                                dcc.Upload(
                                    id='csvFile',
                                    accept='.csv',
                                    children=html.Button('Select CSV File', id='csvSelect')
                                )
                            ]
                        ),
                        html.Button('Visualize', id='btn')
                    ]
                ),
                html.Div(
                    id='dateSearch',
                    children=[
                        html.Div(
                            children=[
                                html.H4('Date:'),
                                dcc.DatePickerSingle(id='date', placeholder='Select date'),
                                html.Button('Go', id='Datebtn')
                            ]
                        ),
                        html.Div(id='dailyCO2')
                    ]
                ),
                html.Div(
                    id='RangeSearch',
                    children=[
                                html.H4('Date range:'),
                                dcc.DatePickerSingle(id='rangeStart', placeholder='Start date'),
                                html.H4('-'),
                                dcc.DatePickerSingle(id='rangeEnd', placeholder='End date'),
                                html.Button('Go', id='Rangebtn')
                            ]
                ),
                html.Div(
                    id='p-search',
                    children=[
                        dcc.Dropdown(
                            id='projectDropdown',  
                            options=[],  
                            value=None,
                            placeholder='Select a project'
                        ),
                        html.Button('Go', id='runIdBtn')]
                )
            ]
        ),
        averageData,
        html.Div(
            id='run-id'
        ),
        html.Div(
            id='head',
            style={'visibility': 'hidden'},
            children=[
                metadata,
                dcc.Graph(id='emissionRateChart'),
            ]
        ),
        html.Div(
            id='head2',
            style={'visibility': 'hidden'},
            children=[
                dcc.Graph(id='energyComparisonChart'),
                dcc.Graph(id='powerComparisonChart'),
            ]
        )
    ]
)


@app.callback(
    [Output('emissionRateChart', 'figure',allow_duplicate=True),
     Output('energyComparisonChart', 'figure',allow_duplicate=True),
     Output('powerComparisonChart', 'figure',allow_duplicate=True),
     Output('metadata', 'children',allow_duplicate=True),
     Output('averageData', 'children',allow_duplicate=True),
    Output('run-id', 'children', allow_duplicate=True)],
    [Input('Datebtn', 'n_clicks')],
    [State('date', 'date')],
    prevent_initial_call=True
)
def update_graphs_by_date(n_clicks, selected_date):
    if n_clicks is None or selected_date is None:
        return go.Figure(), go.Figure(), go.Figure()

    filtered_data = filter_data_by_date(selected_date)
    
    run_id = display_run_id(filtered_data)


    emission_rate_chart = plot_emission_rate(filtered_data)
    energy_comparison_chart = plot_energy_comparison(filtered_data)
    power_comparison_chart = plot_power_comparison(filtered_data)
    metadata = generate_metadata(filtered_data)
    average_data = display_latest(filtered_data)


    return (
        emission_rate_chart,
        energy_comparison_chart,
        power_comparison_chart,
        metadata,
        average_data,
        run_id,
    )

@app.callback(
    [Output('emissionRateChart', 'figure',allow_duplicate=True),
     Output('energyComparisonChart', 'figure',allow_duplicate=True),
     Output('powerComparisonChart', 'figure',allow_duplicate=True),
     Output('metadata', 'children',allow_duplicate=True),
     Output('averageData', 'children',allow_duplicate=True)],
    [Input('Rangebtn', 'n_clicks')],
    [State('rangeStart', 'date'),
     State('rangeEnd', 'date')],
    prevent_initial_call=True

)


def update_graphs_by_Range(n_clicks, start_date, end_date):
    if n_clicks is None or start_date is None or end_date is None:
        return go.Figure(), go.Figure(), go.Figure(), html.Div(), html.Div()

    filtered_data = filter_data_by_date_range(start_date, end_date)

    emission_rate_chart = plot_emission_rate(filtered_data)
    energy_comparison_chart = plot_energy_comparison(filtered_data)
    power_comparison_chart = plot_power_comparison(filtered_data)
    metadata = generate_metadata(filtered_data)
    average_data = display_sum(filtered_data)

    return (
        emission_rate_chart,
        energy_comparison_chart,
        power_comparison_chart,
        metadata,
        average_data
    )


def filter_data_by_date(selected_date):
    return [d for d in data if d['timestamp'].split('T')[0] == selected_date]


def filter_data_by_date_range(start_date, end_date):
    return [d for d in data if start_date <= d['timestamp'].split('T')[0] <= end_date]

def display_run_id(filtered_data):
    run_id = filtered_data[0]['run_id'] if filtered_data else "No run ID available"
    return f"Run ID: {run_id}"



def calculate_daily_co2(filtered_data):
    return sum(float(d['emissions']) for d in filtered_data)

def display_latest(data):
    energyValues = [float(d['energy_consumed']) for d in data]
    emissionValues = [float(d['emissions']) for d in data]
    durationValues = [float(d['duration']) for d in data]

    averageEnergy = energyValues[-1]
    averageEmission = emissionValues[-1]
    averageDuration = durationValues[-1]

    latest_data = html.Div(
        id='head',
        children=[
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageEnergy:.5f}', id='avgNum'),
                            html.Span('kwh')
                        ]
                    ),
                    html.H3('Energy Consumed')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageEmission:.5f}', id='avgNum'),
                            html.Span('Kg.Eq.CO2')
                        ]
                    ),
                    html.H3('Emissions Produced')
                ]
            ),
            html.Div(
                id='circle',
                children=[
                    html.Div(
                        id='dataCircle',
                        children=[
                            html.Span(f'{averageDuration:.2f}', id='avgNum'),
                            html.Span('Sec', id='second')
                        ]
                    ),
                    html.H3('Duration')
                ]
            )
        ]
    )

    return latest_data


@app.callback(
    [Output('emissionRateChart', 'figure', allow_duplicate=True),
     Output('energyComparisonChart', 'figure', allow_duplicate=True),
     Output('powerComparisonChart', 'figure', allow_duplicate=True),
     Output('metadata', 'children', allow_duplicate=True),
     Output('averageData', 'children', allow_duplicate=True)],
    [Input('runIdBtn', 'n_clicks')],
    [State('projectDropdown', 'value')],
    prevent_initial_call=True
)
def update_graphs_by_project(n_clicks, selected_project):
    global data
    if n_clicks is None or selected_project is None or data is None:
        return (
            go.Figure(), go.Figure(), go.Figure(),
            html.Div(), html.Div()
        )

    filtered_data = [d for d in data if d['project_name'] == selected_project]

    emission_rate_chart = plot_emission_rate(filtered_data)
    energy_comparison_chart = plot_energy_comparison(filtered_data)
    power_comparison_chart = plot_power_comparison(filtered_data)
    metadata = generate_metadata(filtered_data)
    average_data = display_average(filtered_data)

    return (
        emission_rate_chart,
        energy_comparison_chart,
        power_comparison_chart,
        metadata,
        average_data
    )
@app.callback(
    Output('projectDropdown', 'options', allow_duplicate=True),
    [Input('date', 'date')],
    [State('csvFile', 'contents')],
    prevent_initial_call=True
)
def update_projects_by_date(selected_date, file_contents):
    if selected_date is None or file_contents is None:
        return []

    decoded_content = base64.b64decode(file_contents.split(',')[1]).decode('utf-8')
    data = parse_csv(decoded_content)

    
    filtered_data = [d for d in data if d['timestamp'].split('T')[0] == selected_date]
    unique_project_names = list({d['project_name'] for d in filtered_data})
    return [{'label': name, 'value': name} for name in unique_project_names]

@app.callback(
    Output('projectDropdown', 'options', allow_duplicate=True),
    [Input('rangeStart', 'date'),
     Input('rangeEnd', 'date')],
    [State('csvFile', 'contents')],
    prevent_initial_call=True
)
def update_projects_by_date_range(start_date, end_date, file_contents):
    if not start_date or not end_date or not file_contents:
        return []

    decoded_content = base64.b64decode(file_contents.split(',')[1]).decode('utf-8')
    data = parse_csv(decoded_content)

    
    filtered_data = [d for d in data if start_date <= d['timestamp'].split('T')[0] <= end_date]
    unique_project_names = list({d['project_name'] for d in filtered_data})
    return [{'label': name, 'value': name} for name in unique_project_names]

if __name__ == '__main__':
    app.run_server(debug=True)
