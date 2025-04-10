import streamlit as st
from streamlit_elements import elements, mui, html, lazy, sync

st.markdown("# Editor page 1 ❄️")
st.sidebar.markdown("# Editor page 1 ❄️")



# with elements("nested_children"):

#     # You can nest children using multiple 'with' statements.
#     #
#     # <Paper>
#     #   <Typography>
#     #     <p>Hello world</p>
#     #     <p>Goodbye world</p>
#     #   </Typography>
#     # </Paper>

#     with mui.Paper:
#         with mui.Typography:
#             html.p("Hello world")
#             html.p("Goodbye world")

# with elements("monaco_editors"):

#     # Streamlit Elements embeds Monaco code and diff editor that powers Visual Studio Code.
#     # You can configure editor's behavior and features with the 'options' parameter.
#     #
#     # Streamlit Elements uses an unofficial React implementation (GitHub links below for
#     # documentation).

#     from streamlit_elements import editor

#     if "content" not in st.session_state:
#         st.session_state.content = "Default value"

#     mui.Typography("Content: ", st.session_state.content)

#     def update_content(value):
#         st.session_state.content = value

#     editor.Monaco(
#         height=300,
#         defaultValue=st.session_state.content,
#         onChange=lazy(update_content)
#     )

#     mui.Button("Update content", onClick=sync())

#     editor.MonacoDiff(
#         original="Happy Streamlit-ing!",
#         modified="Happy Streamlit-in' with Elements!",
#         height=300,
#     )

# col1, col2, col3, col4, col5 = st.columns(5)

# with col1():
#     if st.button("add box")

# def add_element():
#     for i in layout:
#     layout.append(dashboard.Item("untitled item", ))

with elements("dashboard"):

    # You can create a draggable and resizable dashboard using
    # any element available in Streamlit Elements.

    from streamlit_elements import dashboard

    # First, build a default layout for every element you want to include in your dashboard

    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 2, 2),
        dashboard.Item("second_item", 2, 0, 2, 2, moved=False),
        dashboard.Item("third_item", 0, 2, 1, 1),
    ]

    # Next, create a dashboard layout using the 'with' syntax. It takes the layout
    # as first parameter, plus additional properties you can find in the GitHub links below.

    with dashboard.Grid(layout):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item")

    # If you want to retrieve updated layout values as the user move or resize dashboard items,
    # you can pass a callback to the onLayoutChange event parameter.

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item")