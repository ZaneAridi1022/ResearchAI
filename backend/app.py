import asyncio
import streamlit as st
from recommend import action
from summary import summarize_text
import uuid

def show_articles(url_input, urls):
    for url in urls:
        st.write(url)
        if st.button("Rabit Hole!", key=uuid.uuid4()):
            main(url_input, url)

def main(url_input, url):
    url_input.write(url)
    if url:
        summary = summarize_text(url)
        st.write(summary)
        col1, col2 = st.columns(2)
        col1.subheader("Supporting Articles")
        col2.subheader("Refuting Articles")
        with col1:
            with st.spinner("Generating supporting articles..."):
                urls = list(set(asyncio.run(action("support", url))))
                show_articles(url_input, urls)
        with col2:
            with st.spinner("Generating refuting articles..."):
                urls = list(set(asyncio.run(action("refute", url))))
                show_articles(url_input, urls)

if __name__ == "__main__":
    st.header("ResearchAI")
    st.subheader("Current Article")
    url_input = st.container()
    url = st.text_input("Enter a research article article:")
    main(url_input, url)
