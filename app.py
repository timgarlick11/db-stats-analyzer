# app.py

import dash
from dash import dcc, html
import dash_table
import plotly.express as px
from data.queries import (
    fetch_table_stats, fetch_table_sizes, fetch_index_usage,
    fetch_slow_queries, fetch_locks, generate_recommendations
)

# Existing data
df_usage = fetch_table_stats()
df_sizes = fetch_table_sizes()
df_index = fetch_index_usage()

# Create charts for table usage, sizes, and index usage
fig_usage = px.bar(
    df_usage,
    x="table_name",
    y=["seq_scan", "idx_scan", "n_live_tup"],
    title="Table Usage Insights",
    labels={"value": "Count", "variable": "Metric"},
    barmode="group"
)

if not df_sizes.empty:
    df_sizes['table_size_mb'] = df_sizes['table_size'] / 1024 / 1024
    df_sizes['index_size_mb'] = df_sizes['index_size'] / 1024 / 1024
    fig_sizes = px.bar(
        df_sizes,
        x="table_name",
        y=["table_size_mb", "index_size_mb"],
        title="Table Sizes (MB)",
        labels={"value": "Size (MB)", "variable": "Type"},
        barmode="stack"
    )
else:
    fig_sizes = {}

if not df_index.empty:
    df_index['index_size_mb'] = df_index['index_size'] / 1024 / 1024
    fig_index = px.bar(
        df_index,
        x="index_name",
        y="idx_scan",
        title="Index Scan Counts",
        labels={"idx_scan": "Index Scans", "index_name": "Index"}
    )
else:
    fig_index = {}

# New data for slow queries, locks, and recommendations
df_slow = fetch_slow_queries()
df_locks = fetch_locks()
recommendations = generate_recommendations()

# Prepare DataTable columns and data for slow queries and locks
slow_columns = [{"name": col, "id": col} for col in df_slow.columns] if not df_slow.empty else []
slow_data = df_slow.to_dict('records') if not df_slow.empty else []

lock_columns = [{"name": col, "id": col} for col in df_locks.columns] if not df_locks.empty else []
lock_data = df_locks.to_dict('records') if not df_locks.empty else []

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=["/assets/style.css"])

app.layout = html.Div([
    html.H1("Enhanced Database Insights Dashboard"),
    dcc.Tabs([
        dcc.Tab(label="Table Usage", children=[
            dcc.Graph(figure=fig_usage)
        ]),
        dcc.Tab(label="Table Sizes", children=[
            dcc.Graph(figure=fig_sizes)
        ]),
        dcc.Tab(label="Index Usage", children=[
            dcc.Graph(figure=fig_index)
        ]),
        dcc.Tab(label="Slow Queries", children=[
            html.H3("Top Slow Queries"),
            dash_table.DataTable(
                data=slow_data,
                columns=slow_columns,
                page_size=10,
                style_table={'overflowX': 'auto'},
            )
        ]),
        dcc.Tab(label="Locks", children=[
            html.H3("Waiting Locks"),
            dash_table.DataTable(
                data=lock_data,
                columns=lock_columns,
                page_size=10,
                style_table={'overflowX': 'auto'},
            )
        ]),
        dcc.Tab(label="Recommendations", children=[
            html.H3("Recommendations"),
            html.Ul([html.Li(rec) for rec in recommendations])
        ])
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
