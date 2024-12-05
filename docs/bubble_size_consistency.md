### JIRA Ticket: Maintain Consistent Bubble Sizes During Filter Operations

**Title:** Fix Bubble Size Reset Issue in Marimo Bubble Chart Filtering

**Description:** When filters are applied to the Marimo bubble chart, bubble sizes are currently resetting instead of maintaining consistency. This needs to be fixed to ensure a consistent visualization experience during filter operations.

---

#### Modules and Responsibilities

**1. Bubble Size Normalization Module**
- **Purpose:** Maintain consistent bubble size scaling across filter operations
- **Responsibilities:**
  - Calculate and store initial bubble size scaling factors
  - Preserve size relationships between bubbles after filtering
  - Apply consistent scaling across filter operations
- **Constraints:**
  - Must work with existing bubble size calculation logic
  - Cannot modify the underlying data values
- **Validation Rules:**
  - Verify bubbles maintain relative size proportions
  - Ensure no visual artifacts during filter transitions

**2. Filter State Management Module**
- **Purpose:** Track filter state and associated size parameters
- **Responsibilities:**
  - Store pre-filter size parameters
  - Reapply correct sizing after filter operations
- **Constraints:**
  - Must integrate with existing filter logic
  - Cannot impact filter performance
- **Validation Rules:**
  - Verify size parameters are preserved across all filter operations
  - Confirm no memory leaks from stored parameters

---

#### Acceptance Criteria

1. **GIVEN** a bubble chart is displayed with initial data
   **WHEN** no filters are applied
   **THEN** bubble sizes are calculated and displayed according to data values

2. **GIVEN** a bubble chart with established bubble sizes
   **WHEN** any filter is applied
   **THEN** remaining bubbles maintain their original relative sizes

3. **GIVEN** a filtered bubble chart
   **WHEN** filters are removed
   **THEN** all bubbles return to their original sizes

4. **GIVEN** multiple filter operations
   **WHEN** filters are applied sequentially
   **THEN** bubble sizes remain consistent throughout all operations

---

#### Required Documentation
- [Marimo State Management](https://docs.marimo.io/guides/state.html)
- [Marimo Visualization Components](https://docs.marimo.io/api/visualizations.html)
- [Current Filter Implementation Documentation]

---

#### Out of Scope
1. Implementing new bubble sizing algorithms
2. Adding user controls for bubble sizes
3. Optimizing performance of bubble sizing calculations
4. Handling edge cases like zero-value bubbles
5. Adding animation during size transitions
6. Modifying existing filter functionality
7. Changing the way initial bubble sizes are calculated
8. Adding new visualization features or controls

---

#### Technical Notes
- Solution should focus solely on maintaining size consistency during filtering
- Any size calculation optimizations should be handled in a separate ticket
- Implementation should not affect the current filter logic or performance
- Testing should verify consistency across all possible filter combinations
