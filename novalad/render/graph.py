import sys
import json
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output

# Use JupyterDash in Colab, Dash locally
if "google.colab" in sys.modules:
    from jupyter_dash import JupyterDash
    DashApp = JupyterDash
else:
    from dash import Dash
    DashApp = Dash


def render_knowledge_graph(data: dict) -> None:
    """
    Render an interactive knowledge graph using Dash and Dash Cytoscape.

    Args:
        data (dict): Knowledge graph data with nodes and edges.

    Returns:
        None
    """
    graph_data = data["data"].get("knowledge_graphs", {})

    # Convert to Cytoscape elements
    elements = []

    for node in graph_data["nodes"]:
        elements.append({
            "data": {
                "id": node["id"],
                "label": (
                    node["name"][10:20] + "..."
                    if len(node.get("name", "")) > 10 and node["type"] not in ["root", "page", "title", "section"]
                    else node["name"]
                ),
                "hover_text": node.get("name", "No additional info available")
            }
        })

    for edge in graph_data["edges"]:
        elements.append({
            "data": {
                "source": edge["fromId"],
                "target": edge["toId"],
                "label": edge["description"]
            }
        })

    # Build the app
    app = DashApp(__name__)
    app.layout = html.Div([
        html.H3("Interactive Knowledge Graph"),
        html.Div(id="node-info", style={"margin": "10px", "font-size": "14px", "color": "#F58634"}),

        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={"name": "cose"},
            style={"width": "100%", "height": "500px"},
            stylesheet=[
                {"selector": "node", "style": {
                    "content": "data(label)",
                    "background-color": "#004DB5",
                    "color": "#F3F3EE",
                    "font-size": "10px",
                    "text-valign": "center"
                }},
                {"selector": "edge", "style": {
                    "curve-style": "bezier",
                    "target-arrow-shape": "triangle",
                    "line-color": "#F58634"
                }},
                {"selector": "edge[label]", "style": {
                    "label": "data(label)",
                    "color": "#94B8E9",
                    "font-size": "10px"
                }},
            ],
        ),
    ])

    @app.callback(
        Output("node-info", "children"),
        [Input("cytoscape", "tapNodeData")]
    )
    def display_click_info(node_data):
        if node_data and "hover_text" in node_data:
            return f"Selected Node: {node_data['hover_text']}"
        return "Click on a node to see details"

    # Show app inline if in Colab, else open in browser
    if "google.colab" in sys.modules:
        app.run(mode='inline', debug=True)
    else:
        app.run(debug=True)
