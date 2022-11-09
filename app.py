#Import Libraries
import dash
from dash import html, callback, Input, Output, State, dcc
import dash_bootstrap_components as dbc

#Adding data folder to the system path
import sys
sys.path.insert(0, '/app/data')

#Own functions
from predict import generate_prediction

#Create App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO],
meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])

app.config.suppress_callback_exceptions=True

app.title = "Low Birth Weight Risk Detector"


#Create form with prediction parameters
tges = dbc.Row(
    [
        dbc.Label("Gestation Period", html_for="model_form_tges", width=2),
        dbc.Col(dcc.Slider(min=1, max=6, step=1, value=1, id="model_form_tges",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

numconsul = dbc.Row(
    [
        dbc.Label("Pre-natal Medical Visits", html_for="model_form_numcosul", width=2),
        dbc.Col(dcc.Slider(min=0, max=20, step=1, value=0, id="model_form_numconsul",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

edadmadre = dbc.Row(
    [
        dbc.Label("Age - Mother", html_for="model_form_edadmadre", width=2),
        dbc.Col(dcc.Slider(min=1, max=9, step=1, value=1, id="model_form_edadmadre",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

estcivm = dbc.Row(
    [
        dbc.Label("Marital Status - Mother", html_for="model_form_estcivm", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="model_form_estcivm",
                options=[
                    {"label": "Cohabiting - 2Y or more", "value": "Cohabiting - 2Y or more)"},
                    {"label": "Cohabiting - less than 2Y", "value": "Cohabiting - less than 2Y"},
                    {"label": "Divorced", "value": "Divorced"},
                    {"label": "Widowed", "value": "Widowed"},
                    {"label": "Single", "value": "Single"},
                    {"label": "Married", "value": "Married"},
                ],
                inline = True,
            ),
        ),
    ],
    className="mb-3",
)

nivedum = dbc.Row(
    [
        dbc.Label("Education Level - Mother", html_for="model_form_nivedum", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="model_form_nivedum",
                options=[
                    {"label": "Preschool", "value": "Preschool"},
                    {"label": "Primary", "value": "Primary"},
                    {"label": "Secondary", "value": "Secondary"},
                    {"label": "Non-University Higher", "value": "Non-University Higher"},
                    {"label": "Undegraduate", "value": "Undegraduate"},
                    {"label": "Postgraduate", "value": "Postgraduate"},
                    {"label": "None", "value": "None"},
                ],
                inline = True,
            ),
        ),
    ],
    className="mb-3",
)

nhijosv = dbc.Row(
    [
        dbc.Label("Living Children - Mother", html_for="model_form_nhijosv", width=2),
        dbc.Col(dcc.Slider(min=0, max=25, step=1, value=0, id="model_form_nhijosv",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

nemb = dbc.Row(
    [
        dbc.Label("Previous Pregnancies - Mother", html_for="model_form_nemb", width=2),
        dbc.Col(dcc.Slider(min=0, max=25, step=1, value=0, id="model_form_nemb",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

segsocial = dbc.Row(
    [
        dbc.Label("Health Insurance Regime - Mother", html_for="model_form_nivedum", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="model_form_segsocial",
                options=[
                    {"label": "Contributory", "value": "Contributory"},
                    {"label": "Subsidized", "value": "Subsidized"},
                    {"label": "Exception", "value": "Exception"},
                    {"label": "Special", "value": "Special"},
                    {"label": "Non-insured", "Non-insured": "Undegraduate"},
                ],
                inline = True,
            ),
        ),
    ],
    className="mb-3",
)

areares = dbc.Row(
    [
        dbc.Label("Residential Area - Mother", html_for="model_form_areares", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="model_form_areares",
                options=[
                    {"label": "Cabecera Municipal", "value": "Cabecera Municipal"},
                    {"label": "Centro Poblado", "value": "Centro Poblado"},
                    {"label": "Rural", "value": "Rural"},
                ],
                inline = True,
            ),
        ),
    ],
    className="mb-3",
)

edadpadre = dbc.Row(
    [
        dbc.Label("Age - Father", html_for="model_form_edadpadre", width=2),
        dbc.Col(dcc.Slider(min=10, max=100, step=5, value=10, id="model_form_edadpadre",
            tooltip={"placement": "bottom", "always_visible": True})),
    ],
    className="mb-3",
)

nivedup = dbc.Row(
    [
        dbc.Label("Education Level - father", html_for="model_form_nivedum", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="model_form_nivedup",
                options=[
                    {"label": "Preschool", "value": "Preschool"},
                    {"label": "Primary", "value": "Primary"},
                    {"label": "Secondary", "value": "Secondary"},
                    {"label": "Non-University Highe", "value": "Non-University Highe"},
                    {"label": "Undegraduate", "value": "Undegraduate"},
                    {"label": "Postgraduate", "value": "Postgraduate"},
                    {"label": "None", "value": "None"},
                ],
                inline = True,
            ),
        ),
    ],
    className="mb-3",
)

form = dbc.Form([tges, numconsul, edadmadre, estcivm, nivedum, nhijosv, nemb, segsocial, areares, edadpadre, nivedup], 
id="model_form")

#Generate Card with Prediction Results
results_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H6("Low Birth Weight Risk Prediction", className="card-title"),
                html.P("Probability of Low Birth Weight:"),
                dcc.Input(id="probability_alert", value=0, type="number")
            ]
        ),
    ],
    style={"width": "18rem"},
)

#Define layout
app.layout = html.Div([
    dbc.Row(dbc.Alert("Low Birth Weight Risk Detector", color="primary", style={'textAlign': 'center', "font-weight":"bold", 
                "padding":"30px"})),
    dbc.Row(
        [
            dbc.Col([
                dbc.Row(form, style={"padding":"20px"}),
                 ]),
            dbc.Col([
                dbc.Row(dbc.Button("Submit", id="probability_alert_button", class_name="me-2", n_clicks=0),
                    style={"padding":"20px"}),
                dbc.Row([results_card], style={"padding":"20px"}),
                dbc.Row(dbc.Badge("Git Hub Repo", href="#", color="primary"), style={"padding":"20px"}),
            ], width=3, align="start"),
        ],
    ),
]) 

#Callbacks
@callback(
        [Output("probability_alert", "value")], 
        [State("model_form_tges", "value"),
         State("model_form_numconsul", "value"),
         State("model_form_edadmadre", "value"),
         State("model_form_estcivm", "value"),
         State("model_form_nivedum", "value"),
         State("model_form_nhijosv", "value"),
         State("model_form_nemb", "value"),
         State("model_form_segsocial", "value"),
         State("model_form_areares", "value"),
         State("model_form_edadpadre", "value"),
         State("model_form_nivedup", "value"),
         Input("probability_alert_button", "n_clicks"),
        ], prevent_initial_call=True
    )

def predict(tges_selector, numconsul_selector, edadmadre_selector, estcivm_selector, nivedum_selector, nhijosv_selector, nemb_selector,
segsocial_selector, areares_selector, edadpadre_selector, nivedup_selector, n_clicks):

    results = {"t_ges": tges_selector, "numconsul":numconsul_selector, "edad_madre":edadmadre_selector, "est_civm":estcivm_selector, 
    "niv_edum":nivedum_selector, "n-hijos":nhijosv_selector, "n_emb":nemb_selector, "seg_social":segsocial_selector, 
    "area_res":areares_selector, "edad_padre":edadpadre_selector, "nivedup":nivedup_selector}

    if n_clicks is not None:
        new_probability = generate_prediction(results)
        return [str(new_probability)]
    else:
        return ["Please Submit Form"]

# This call will be used with Gunicorn server
server = app.server

# Testing server
if __name__ == "__main__":
    app.run_server(debug=True, host="localhost", port=8050)
