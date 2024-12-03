### JIRA Ticket: Interactive Marimo Notebook with Scalable Bubble Chart Visualization

**Title:** Interactive Marimo Notebook with Scalable Bubble Chart Visualization

**Description:** Implement an interactive Marimo notebook that visualizes data using a bubble chart. The notebook must handle large datasets, dynamically update dimensions using Marimo interactions, and support grouping by a third dimension with subplots and color. The implementation must strictly adhere to Plotly and Marimo documentation and guidelines.

---

#### Modules and Responsibilities

**1. Data Generation Module**
- **Purpose:** Generate a synthetic dataset with at least three categorical dimensions and one numerical dimension.
- **Responsibilities:**
  - Create a pandas DataFrame with 1,000+ rows.
  - Populate with three categorical dimensions (`Category1`, `Category2`, `Category3`) and one numerical dimension (`Value`).
- **Constraints:**
  - Ensure randomness with a reproducible seed.
  - All categorical dimensions must have 3-5 unique values.
- **Validation Rules:**
  - Confirm the DataFrame has at least 1,000 rows.
  - Ensure all dimensions contain non-null values.

Python Code:
---
import pandas as pd
import numpy as np

np.random.seed(42)  # Ensure reproducibility
data = {
    "Category1": np.random.choice(["A", "B", "C"], size=1000),
    "Category2": np.random.choice(["X", "Y", "Z"], size=1000),
    "Category3": np.random.choice(["M", "N"], size=1000),
    "Value": np.random.rand(1000) * 100
}
df = pd.DataFrame(data)
print(df.head())
---

---

**2. Plotly Visualization Module**
- **Purpose:** Generate the bubble chart visualization.
- **Responsibilities:**
  - Plot two categorical dimensions on the X and Y axes.
  - Use the numerical dimension for bubble size.
  - Dynamically adjust the chart based on user-selected dimensions.
  - Add hover tooltips to display all relevant dimension values.
- **Constraints:**
  - Enable multicategory axes where needed.
  - Subplots for the third dimension must be automatically generated when selected.
  - Use distinct colors for categories in the third dimension when subplots are not applicable.
- **Validation Rules:**
  - Confirm hover details display all selected dimensions.
  - Ensure subplots and color logic work as intended for the third dimension.

Python Code:
---
import plotly.express as px

fig = px.scatter(
    df,
    x="Category1",
    y="Category2",
    size="Value",
    color="Category3",
    facet_col="Category3",  # Subplot configuration
    hover_name="Category3",
    title="Interactive Bubble Chart"
)
fig.update_traces(marker=dict(opacity=0.7))  # Adjust marker visibility
fig.show()
---

---

**3. Marimo Interaction Module**
- **Purpose:** Handle user interaction through Marimo's UI components.
- **Responsibilities:**
  - Provide dropdowns for users to select the X, Y, and third grouping dimensions.
  - Ensure dropdowns are reactive and update the Plotly chart on selection.
- **Constraints:**
  - All interaction logic must use Marimo components.
  - Avoid using custom or external interaction handlers.
- **Validation Rules:**
  - Verify dropdown changes update the chart instantly.
  - Test dropdown usability for large datasets.

Marimo Interaction Example:
---
import marimo as mo

x_axis_dropdown = mo.ui.dropdown(
    options=["Category1", "Category2", "Category3"], 
    value="Category1", 
    label="X-axis"
)
y_axis_dropdown = mo.ui.dropdown(
    options=["Category1", "Category2", "Category3"], 
    value="Category2", 
    label="Y-axis"
)
grouping_dropdown = mo.ui.dropdown(
    options=["Category3"], 
    value="Category3", 
    label="Group by (Subplots)"
)
---

---

#### Acceptance Criteria

1. **GIVEN** a synthetic dataset is generated with the required dimensions,  
   **WHEN** the notebook is executed,  
   **THEN** the initial bubble chart must display with two categorical axes and a numerical bubble size.

2. **GIVEN** a third dimension is selected by the user,  
   **WHEN** subplots are appropriate for grouping,  
   **THEN** the notebook must render subplots with bubbles grouped by the third dimension.

3. **GIVEN** a third dimension is selected by the user,  
   **WHEN** subplots are not practical,  
   **THEN** the notebook must assign distinct colors for categories in the third dimension.

4. **GIVEN** a dataset with more than 1,000 rows,  
   **WHEN** the notebook is executed,  
   **THEN** all interactions and visualizations must complete within 2 seconds.

---

#### Required Documentation

- [Marimo Working with Data - Plotting](https://docs.marimo.io/guides/working_with_data/plotting.html)
- [Plotly Categorical Axes](https://plotly.com/python/categorical-axes/)
- [Plotly Bubble Charts](https://plotly.com/python/bubble-charts/)
- [Marimo Interactivity](https://docs.marimo.io/guides/interactivity.html)

---

#### Out of Scope
1. Custom Plotly extensions
2. Advanced filtering or aggregation
3. External integrations
4. Styling preferences or themes

---
