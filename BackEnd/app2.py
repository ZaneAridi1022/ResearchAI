import asyncio
import streamlit as st
from recommend import Recommendation
import uuid
import graphviz


def show_articles(url):
    if st.button("Rabbit Hole!", key=uuid.uuid4()):
        url = "url2new"
        st.session_state.rabbit_hole = True
        main(url)

def main(url):
    st.subheader("Current Article")
    st.session_state.url_input = st.empty()
    if url:
        st.session_state.url_input.text_input("Enter a research article:", value=url)
        summary = "summary"
        topic = st.empty()
        st.write(summary)
        col1, col2 = st.columns(2)
        with topic.container():
            topic.write("topic")
        col1.subheader("Supporting Articles")
        col2.subheader("Refuting Articles")
        show_articles(url)

        st.subheader("Graph")
        st.graphviz_chart(st.session_state.graph, use_container_width=True)

if __name__ == "__main__":
    st.session_state.rabbit_hole = False
    st.session_state.graph = graphviz.Digraph()
    st.header("Rabbit Hole")
    if not st.session_state.rabbit_hole:
        url = st.text_input("Enter a research article:")
        main(url)
