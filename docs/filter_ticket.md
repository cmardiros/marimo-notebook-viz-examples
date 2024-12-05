TODO: keep bubble size consistent cause it resets on filtering

### JIRA Ticket: Add Include/Exclude Filtering to Marimo Bubble Chart

**Title:** Implement Include/Exclude Filtering Controls for Interactive Bubble Chart

**Description:** Add filtering capabilities to the existing Marimo bubble chart visualization with separate include and exclude filter dropdowns in the controls section. Filters should affect the underlying DataFrame before visualization.

---

#### Modules and Responsibilities

**1. Filter Options Module**
- **Purpose:** Generate filter options from DataFrame columns
- **Responsibilities:**
  - Create filter options in format "Column=Value" for all categorical columns
  - Support multiple selections
- **Constraints:**
  - Only generate options for categorical columns
  - Format must be "Column=Value" (e.g., "Category1=A")
- **Validation Rules:**
  - Verify all generated options are unique
  - Ensure format consistency

Python Example:
```python
def create_filter_options(df):
    """Create filter options in format CategoryName=Value"""
    options = []
    for col in df.select_dtypes(include=['object']).columns:
        for val in df[col].unique():
            options.append(f"{col}={val}")
    return sorted(options)
```

**2. Filter Application Module**
- **Purpose:** Apply include and exclude filters to DataFrame
- **Responsibilities:**
  - Parse filter strings into column/value pairs
  - Apply include filters (OR within same column, AND between columns)
  - Apply exclude filters after includes
- **Constraints:**
  - Handle empty filter lists gracefully
  - Maintain original DataFrame order
- **Validation Rules:**
  - Verify filtered DataFrame contains valid rows
  - Confirm exclude filters override includes

Python Example:
```python
def apply_filters(df, include_filters, exclude_filters):
    """Apply include and exclude filters to the dataframe"""
    filtered_df = df.copy()
    
    if include_filters:
        mask = pd.Series(False, index=df.index)
        for filter_str in include_filters:
            col, val = filter_str.split('=')
            mask |= (df[col] == val)
        filtered_df = filtered_df[mask]
    
    if exclude_filters:
        for filter_str in exclude_filters:
            col, val = filter_str.split('=')
            filtered_df = filtered_df[filtered_df[col] != val]
            
    return filtered_df
```

**3. UI Integration Module**
- **Purpose:** Add filter controls to existing UI
- **Responsibilities:**
  - Create include/exclude filter dropdowns
  - Update visualization when filters change
  - Place filters in controls section
- **Constraints:**
  - Maintain existing UI layout
  - Use Marimo components only
- **Validation Rules:**
  - Verify filter controls update chart immediately
  - Confirm filter state persists during dimension changes

---

#### Acceptance Criteria

1. **GIVEN** the bubble chart is displayed
   **WHEN** no filters are selected
   **THEN** all data points are shown

2. **GIVEN** an include filter is selected
   **WHEN** the chart updates
   **THEN** only matching records are displayed

3. **GIVEN** an exclude filter is selected
   **WHEN** the chart updates
   **THEN** matching records are removed from display

4. **GIVEN** both include and exclude filters are active
   **WHEN** they affect the same category
   **THEN** exclude takes precedence over include

5. **GIVEN** the user changes chart dimensions
   **WHEN** filters are active
   **THEN** filters continue to affect the underlying data

---

#### Required Documentation
- [Marimo UI Components](https://docs.marimo.io/api/inputs.html)
- [Marimo State Management](https://docs.marimo.io/guides/state.html)
- [Pandas Boolean Indexing](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing)

---

#### Out of Scope
1. Complex filter logic (AND/OR combinations)
2. Filter state persistence across notebook sessions
3. Custom filter input formats
4. Filter validation beyond basic format checking
5. Performance optimization for large datasets
6. Filter presets or saved filter combinations
7. Filter history or undo/redo
8. Filter statistics or impact preview

---
