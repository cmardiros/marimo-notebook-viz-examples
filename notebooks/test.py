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
        "Category2": np.random.choice(["X", "Y", "Z"], size=1000, p=[0.1, 0.2, 0.7]),   # Z dominates
        "Category3": np.random.choice(["M", "N"], size=1000, p=[0.9, 0.1]),             # M is much more common
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
        options=["Category1", "Category2", "Category3"],
        value="Category1",
        label="X-axis Dimension",
    )

    y_axis_dropdown = mo.ui.dropdown(
        options=["Category1", "Category2", "Category3"],
        value="Category2",
        label="Y-axis Dimension",
    )

    group_dropdown = mo.ui.dropdown(
        options=["None", "Category1", "Category2", "Category3"],
        value="Category3",
        label="Group/Color Dimension",
    )

    # Add subplot toggle for better control
    use_subplots = mo.ui.checkbox(
        value=True,
        label="Use subplots when grouping"
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
                    mo.md("**Grouping:**"),
                    mo.hstack([group_dropdown, use_subplots], 
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
        group_dropdown,
        use_subplots,
        x_axis_dropdown,
        y_axis_dropdown,
    )


@app.cell
def create_bubble_chart(
    df,
    group_dropdown,
    px,
    use_subplots,
    x_axis_dropdown,
    y_axis_dropdown,
):
    """Create the bubble chart visualization based on selected dimensions"""
    # Get selected dimensions
    x_dim = x_axis_dropdown.value
    y_dim = y_axis_dropdown.value
    group_dim = group_dropdown.value

    # Prepare data based on selected dimensions
    dimensions = [x_dim, y_dim]
    if group_dim != "None":
        dimensions.append(group_dim)

    # Sort categories alphabetically for consistent display
    category_orders = {
        'Category1': sorted(df['Category1'].unique()),
        'Category2': sorted(df['Category2'].unique()),
        'Category3': sorted(df['Category3'].unique())
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
        'height': 500,
        'hover_data': ['count'],
        'category_orders': category_orders  # Use consistent category ordering
    }

    # Handle grouping dimension
    if group_dim != "None":
        fig_args['color'] = group_dim
        if use_subplots.value:
            fig_args['facet_col'] = group_dim

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
        showlegend=True if group_dim != "None" else False,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return (
        category_orders,
        dimensions,
        fig,
        fig_args,
        group_dim,
        plot_data,
        x_dim,
        y_dim,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
