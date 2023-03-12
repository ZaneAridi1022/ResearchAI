import asyncio
import streamlit as st
from recommend import Recommendation
import uuid
import graphviz


def show_articles(urls):
    for url in urls:
        st.write(url)
        if "pdf" in url:
            if st.button("Rabbit Hole!", key=uuid.uuid4()):
                st.session_state.rabbit_hole = True
                st.subheader("Current Article")
                main(url)

def main(url):
    if url:
        summary = Recommendation().summarize_text(url)
        st.subheader("Current Article")
        st.write(url)
        with st.spinner("Formulating arguments..."):
            json_ = asyncio.run(Recommendation().recommend(summary))
        st.subheader("Topic")
        st.write(json_["topic"])
        st.subheader("Summary")
        st.write(summary)
        col1, col2 = st.columns(2)
        if st.session_state.get("tag_line_support"):
            st.session_state.graph.edge(st.session_state.tag_line_support, "Support")
        else:
             st.session_state.graph.edge(json_["topic"], "Support")
        if st.session_state.get("tag_line_refute"):
            st.session_state.graph.edge(st.session_state.tag_line_refute, "Support")
        else:
            st.session_state.graph.edge(json_["topic"], "Refute")
        col1.subheader("Supporting Articles")
        col2.subheader("Refuting Articles")
        with col1:
            for arg in json_["supporting_arguments"]:
                st.session_state.tag_line_support = arg["tagline"]
                with st.expander(arg["tagline"]):
                    st.write(arg["argument"])
                    st.session_state.graph.edge("Support", arg["tagline"])
                    show_articles(arg["urls"])
        with col2:
            for arg in json_["refuting_arguments"]:
                st.session_state.tag_line_refute = arg["tagline"]
                with st.expander(arg["tagline"]):
                    st.write(arg["argument"])
                    st.session_state.graph.edge("Refute", arg["tagline"])
                    show_articles(arg["urls"])

        st.subheader("Graph")
        st.graphviz_chart(st.session_state.graph, use_container_width=True)

if __name__ == "__main__":
    if not st.session_state.get("rabbit_hole"):
        st.session_state.rabbit_hole = False
    st.session_state.graph = graphviz.Digraph()
    st.header("Rabbit Hole")
    url_input = st.text_input("Enter a research article:")
    if not st.session_state.rabbit_hole:
        main(url_input)
