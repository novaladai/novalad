import dash
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output
import os


def render_knowledge_graph(data: dict, save: bool = False) -> None:
    """
    Render an interactive knowledge graph using Dash and Dash Cytoscape.

    Args:
        data (dict): Knowledge graph data with nodes and edges.
        save (bool): If True, saves the graph as a static HTML file. Default is False.
        filename (str): Base name for the output HTML file if save=True.

    Returns:
        None
    """
    data = data["data"].get("knowledge_graphs", {})

    # Convert data to Cytoscape elements
    elements = []

    for node in data["nodes"]:
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

    for edge in data["edges"]:
        elements.append({
            "data": {
                "source": edge["fromId"],
                "target": edge["toId"],
                "label": edge["description"]
            }
        })

    # Initialize Dash App
    app = dash.Dash(__name__)

    app.layout = html.Div([
        html.H3("Interactive Knowledge Graph"),
        html.Div(id="node-info", style={"margin": "10px", "font-size": "14px", "color": "#F58634"}),

        cyto.Cytoscape(
            id="cytoscape",
            elements=elements,
            layout={"name": "cose"},
            style={"width": "800px", "height": "500px"},
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

    if save:
        from dash import DiskcacheManager
        import dash.dash  # needed to access the app layout string

        # Save layout HTML
        app.index_string = f"""
        <!DOCTYPE html>
        <html>
            <head>
                {{%metas%}}
                <title>Knowledge Graph</title>
                {{%favicon%}}
                {{%css%}}
            </head>
            <body>
                {{%app_entry%}}
                <footer>
                    {{%config%}}
                    {{%scripts%}}
                    {{%renderer%}}
                </footer>
            </body>
        </html>
        """

        # Save layout to file (using Dash's HTML string)
        app_path = "kg.html"
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app.index_string.replace("{%app_entry%}", app._repr_html_()))

    else:
        app.run_server(debug=True)
