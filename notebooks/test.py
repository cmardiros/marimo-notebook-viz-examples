import marimo

__generated_with = "0.9.29"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import plotly.express as px
    return mo, np, pd, px


@app.cell
def setup(np):
    """Initialize random seed for reproducibility"""
    np.random.seed(42)
    return


@app.cell
def generate_data(np, pd):
    """Generate synthetic dataset with required dimensions"""

    data = {
        "Category1": np.random.choice(["A", "B", "C"], size=1000, p=[0.8, 0.15, 0.05]),  # A is much more common
        "Category2": np.random.choice(["X", "Y", "Z"], size=1000, p=[0.1, 0.2, 0.7]),    # Z dominates
        "Category3": np.random.choice(["M", "N"], size=1000, p=[0.9, 0.1]),              # M is much more common
        "Category4": np.random.choice(["P", "Q", "R", "S"], size=1000, p=[0.4, 0.3, 0.2, 0.1]),  # P is most common
        "Category5": np.random.choice(["Alpha", "Beta", "Gamma"], size=1000, p=[0.6, 0.3, 0.1]),  # Alpha dominates
        "Profiles": 1
    }
    df = pd.DataFrame(data)
    return data, df


@app.cell
def analyze_grouped_data():
    # Group by all categorical dimensions and get counts
    # df.groupby(['Category1', 'Category2', 'Category3']).size().reset_index(name='Profiles')
    return


@app.cell
def create_controls(mo):
    """Create UI controls for dimension selection"""
    # Create dropdowns with improved labels and organization
    x_axis_dropdown = mo.ui.dropdown(
        options=["Category1", "Category2", "Category3", "Category4", "Category5"],
        value="Category1",
        label="X-axis Dimension",
    )

    y_axis_dropdown = mo.ui.dropdown(
        options=["Category1", "Category2", "Category3", "Category4", "Category5"],
        value="Category2",
        label="Y-axis Dimension",
    )

    color_dropdown = mo.ui.dropdown(
        options=["None", "Category1", "Category2", "Category3", "Category4", "Category5"],
        value="None",
        label="Color Dimension",
    )

    facet_col_dropdown = mo.ui.dropdown(
        options=["None", "Category1", "Category2", "Category3", "Category4", "Category5"],
        value="None",
        label="Column Facet Dimension",
    )

    facet_row_dropdown = mo.ui.dropdown(
        options=["None", "Category1", "Category2", "Category3", "Category4", "Category5"],
        value="None",
        label="Row Facet Dimension",
    )

    mo.md("### Interactive Bubble Chart Controls")
    mo.md("Select dimensions for visualization:")

    # Organize controls in a more structured layout
    controls = mo.hstack(
        [
            mo.vstack(
                [
                    mo.md("**Axes:**"),
                    mo.hstack([x_axis_dropdown, y_axis_dropdown], 
                            justify="start", 
                            gap=1.0)
                ],
                align="start",
                gap=0.5
            ),
            mo.vstack(
                [
                    mo.md("**Faceting:**"),
                    mo.hstack([facet_col_dropdown, facet_row_dropdown], 
                            justify="start", 
                            gap=1.0)
                ],
                align="start",
                gap=0.5
            ),
                        mo.vstack(
                [
                    mo.md("**Color:**"),
                    mo.hstack([color_dropdown], 
                            justify="start", 
                            gap=1.0)
                ],
                align="start",
                gap=0.5
            )
        ],
        justify="start",
        align="start",
        gap=2.0
    )
    controls
    return (
        controls,
        color_dropdown,
        facet_col_dropdown,
        facet_row_dropdown,
        x_axis_dropdown,
        y_axis_dropdown,
    )


@app.cell
def create_bubble_chart(
    df,
    color_dropdown,
    facet_col_dropdown,
    facet_row_dropdown,
    px,
    x_axis_dropdown,
    y_axis_dropdown,
):
    """Create the bubble chart visualization based on selected dimensions"""
    # Get selected dimensions
    x_dim = x_axis_dropdown.value
    y_dim = y_axis_dropdown.value
    col_dim = facet_col_dropdown.value
    row_dim = facet_row_dropdown.value
    color_dim = color_dropdown.value

    # Prepare data based on selected dimensions
    dimensions = [x_dim, y_dim]
    if col_dim != "None":
        dimensions.append(col_dim)
    if row_dim != "None":
        dimensions.append(row_dim)

    # Sort categories alphabetically for consistent display
    category_orders = {
        'Category1': sorted(df['Category1'].unique()),
        'Category2': sorted(df['Category2'].unique()),
        'Category3': sorted(df['Category3'].unique()),
        'Category4': sorted(df['Category4'].unique()),
        'Category5': sorted(df['Category5'].unique())
    }

    plot_data = df.groupby(dimensions).sum(['Profiles']).reset_index()
    plot_data = plot_data.rename(columns={'Profiles': 'count'})

    # Base figure configuration
    fig_args = {
        'data_frame': plot_data,
        'x': x_dim,
        'y': y_dim,
        'size': 'count',
        'title': 'Interactive Bubble Chart - Size shows record count',
        'height': 800,
        'hover_data': ['count'],
        'category_orders': category_orders  # Use consistent category ordering
    }

    # Handle color dimension
    
    if color_dim != "None":
        fig_args['color'] = color_dim

    # Handle faceting dimensions
    if col_dim != "None":
        fig_args['facet_col'] = col_dim
    if row_dim != "None":
        fig_args['facet_row'] = row_dim

    # Create figure
    fig = px.scatter(**fig_args)


    # Update axes to ensure categorical treatment and proper ordering
    fig.update_xaxes(
        type='category',
        categoryorder='array',
        categoryarray=category_orders[x_dim],
        showgrid=True,
        ticks="outside",
        linecolor='lightgray',
        linewidth=2,
        #gridcolor='lightgray'
    )

    fig.update_yaxes(
        type='category',
        categoryorder='array',
        categoryarray=category_orders[y_dim],
        showgrid=True,
        ticks="outside",
        linecolor='lightgray',
        linewidth=2,
        #gridcolor='lightgray'
    )



    # Update traces for better visualization
    fig.update_traces(
        marker=dict(
            opacity=0.7,
            sizemode='area',
            sizeref=2.*max(plot_data['count'])/(40.**2),
            sizemin=4
        ),
        selector=dict(mode='markers')
    )

    # Improve layout
    fig.update_layout(
        plot_bgcolor='white',
        showlegend=True if color_dim != "None" else False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return (
        category_orders,
        dimensions,
        fig,
        fig_args,
        col_dim,
        row_dim,
        plot_data,
        x_dim,
        y_dim,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
