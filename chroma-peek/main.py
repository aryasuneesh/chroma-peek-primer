import streamlit as st
import pandas as pd
from utils.peek import ChromaPeek

st.set_page_config(page_title="chroma-peek", page_icon="👀")

## styles ##
padding = 100
st.markdown(""" <style>
            #MainMenu {
                visibility: hidden;
            }
            footer {
                visibility: hidden;
            }
            </style> """, 
            unsafe_allow_html=True)
############

st.title("Chroma Peek 👀")

# get uri of the persist directory
path = ""
col1, col2 = st.columns([4,1])  # adjust the ratio as needed
with col1:
    path = st.text_input("Enter persist path", placeholder="paste full path of persist")
with col2:
    st.write("") 
    if st.button('🔄'):
        st.experimental_rerun()

st.divider()

# load collections
if not(path==""):
    peeker = ChromaPeek(path)

    ## create radio button of each collection
    col1, col2 = st.columns([1,3])
    with col1:
        collection_selected=st.radio("select collection to view",
                 options=peeker.get_collections(),
                 index=0,
                 )
        
    with col2:
        df = peeker.get_collection_data(collection_selected, dataframe=True)
        st.markdown(f"<b>Data in </b>*{collection_selected}*", unsafe_allow_html=True)
        
        if 'embeddings' in df.columns:
            df.drop(columns=['embeddings'], inplace=True)
        if 'documents' in df.columns:
            df.drop(columns=['documents'], inplace=True)
        if 'uris' in df.columns:
            df.drop(columns=['uris'], inplace=True)
        if 'data' in df.columns:
            df.drop(columns=['data'], inplace=True)
        
       # Insert a delete column with checkboxes
        df['Delete'] = [st.checkbox("", key=str(index)) for index in range(len(df))]

        # Reorder columns to include the "Delete" column along with the rest of the columns
        columns = df.columns.tolist()
        columns.remove('Delete')
        columns.insert(0, 'Delete')
        df = df[columns]

        st.dataframe(df)
        
        st.data_editor(df, use_container_width=True, height=300, num_rows="dynamic")
        
    st.divider()

    # Button to delete selected rows
    if st.button('Delete'):
        # Get selected rows
        selected_rows = df.loc[df['Delete'] == True]  # Retrieve rows where 'Delete' column is True
        print("Selected rows:", selected_rows)
        to_delete_ids = selected_rows['ids'].tolist()  # Assuming 'id' is the column containing unique identifiers
        print("IDs to delete:", to_delete_ids)
        # Delete selected rows from the database
        peeker.delete_rows(collection_selected, ids=to_delete_ids)
        
        # Reload the data after deletion
        df = peeker.get_collection_data(collection_selected, dataframe=True)
        
        st.success("Selected rows deleted successfully.")

else:
    st.subheader("Enter Valid Full Persist Path")
