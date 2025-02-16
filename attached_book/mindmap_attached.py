import streamlit as st
import networkx as nx
import pyvis
from pyvis.network import Network
import tempfile
import pandas as pd
from collections import defaultdict
import re
# import pprint as pp
import os
import matplotlib.pyplot as plt

# File paths for importing content
book_title = "Attached: The New Science of Adult Attachment"
content_file_path = "Notes - Content.txt"
notes_file_path = "Notes - Attached - 15Feb25.txt"

# Allow for releative paths
#DEBUG
# print(os.getcwd())
subdir = os.path.join(os.getcwd(), "attached_book")
content_file_path = os.path.join(subdir, content_file_path)
notes_file_path = os.path.join(subdir, notes_file_path)


def create_mindmap_attached():
    # Read chapter start pages from the content file, Define Chapters as a dictionary  (NOTE:  a List will be used with this dictionary to store the chapters and their respective page numbers)
    chapter_pages = {}

    with open(content_file_path, "r", encoding="utf-8") as file:

        #DEBUG
        # print(f"File Opened for Content reading : {content_file_path}")

        for line in file:
            #   Extract the chapter name and page number  m the items in the brackets are the groups
            match = re.match(r"(.+?)\s+-\s+page\s+(\d+)", line.strip(), re.IGNORECASE)
            
            #DEBUG 
            # print(f"Match: {match}")

            if match:
                chapter_name = match.group(1).strip()
                page_number = int(match.group(2))

                chapter_pages[chapter_name] = page_number

                #DEBUG 
                # print(f"Mathc found , Elements : Chapter Name: {chapter_name}, Page Number: {page_number}")


    # Sort chapters by page number
    sorted_chapters = sorted(chapter_pages.items(), key=lambda x: x[1])

    #DEBUG
    # print(f"Sorted Chapters: {sorted_chapters}")

    # Read highlights and categorize them based on page numbers
    # highlights = []
    # current_chapter = None

    # with open(notes_file_path, "r", encoding="utf-8") as file:

    #     #DEBUG
    #     print(f"File Opened for Notes reading : {notes_file_path}")

    #     for line in file:
    #         # Extract the page number, only the digits are extracted and returned from the group
    #         page_match = re.match(r".*Page:\s+(\d+)", line.strip(), re.IGNORECASE)

    #         if page_match:
    #             page_number = int(page_match.group(1))

    #             #DEBUG
    #             print(f"Page Number Matched: {page_number}")

    #             # Determine the correct chapter for this highlight
    #             for chapter, chapter_start_page in sorted_chapters:
    #                 if page_number >= chapter_start_page:
    #                     current_chapter = chapter
    #                 else:
    #                     break

    #             highlights.append((current_chapter, line.strip()))

    #             #DEBUG
    #             print(f"Highlights: {highlights}")


    # Read highlights and categorize them based on page numbers
    # highlights = []
    # current_chapter = None

    # with open(notes_file_path, "r", encoding="utf-8") as file:

    #     # DEBUG
    #     print(f"File Opened for Notes reading : {notes_file_path}")

    #     # The readlines() method reads all the lines from a file and returns them as a list of strings. Each element in the list represents a single line from the file, including the newline character at the end of each line
    #     lines = file.readlines()

    #     i = 0

    #     while i < len(lines):
            
    #         line = lines[i]

    #         # Extract the page number, only the digits are extracted and returned from the group
    #         page_match = re.match(r".*Page:\s+(\d+)", line.strip(), re.IGNORECASE)

    #         # DEBUG
    #         print(f"MAtching for Page number -  page_match: {page_match}")

    #         if page_match:
    #             page_number = int(page_match.group(1))

    #             # DEBUG
    #             print(f"Page Number (converted to integer) : {page_number}")

    #             # Determine the correct chapter for this highlight
    #             for chapter, chapter_start_page in sorted_chapters:
    #                 if page_number >= chapter_start_page:
    #                     current_chapter = chapter
    #                 else:
    #                     break

    #             # Read the next line for the actual highlight
    #             if i + 1 < len(lines):
    #                 highlight_text = lines[i + 1].strip()
    #                 highlights.append((current_chapter, highlight_text))

    #                 # DEBUG
    #                 print(f"Highlight added: {highlight_text}")

    #             # Move to the line after the highlight
    #             i += 1

    #         i += 1



    # Read highlights and categorize them based on page numbers
    highlights = []
    current_chapter = None

    with open(notes_file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]  # Remove empty lines
        
        #DEBUG
        # print("Lines:")
        # pp.pprint(lines)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            page_match = re.match(r".*Page:\s+(\d+)", line, re.IGNORECASE)
            if page_match:
                page_number = int(page_match.group(1))
                # Determine the correct chapter for this highlight
                for chapter, chapter_start_page in sorted_chapters:
                    if page_number >= chapter_start_page:
                        current_chapter = chapter
                    else:
                        break

                # Read the following lines for multi-line highlights
                highlight_text = ""
                i += 1
                # while i < len(lines) and not re.match(r".*highlight.*Page:", lines[i], re.IGNORECASE):
                while i < len(lines) and not re.match(r".*highlight.*Page:", lines[i]):
                    highlight_text += " " + lines[i] if highlight_text else lines[i]
                    i += 1

                #DEBUG
                # print(f"Highlight Text: {highlight_text}")

                highlights.append((current_chapter, highlight_text))
            else:
                i += 1


    #DEBUG
    # for chapter, highlight in highlights:
    #     print(f"### Highlights structure output,  Chapter:    {chapter}   -   {highlight}")


    # Structure highlights in a dictionary
    # The code mind_map_dict = defaultdict(lambda: defaultdict(list)) creates a nested defaultdict structure in Python. Let's break it down to understand what it does:
    # defaultdict: This is a subclass of the built-in dict class from the collections module. It provides a dictionary-like object which can return default values for keys that haven't been set yet.
    # lambda: defaultdict(list): This is an anonymous function (lambda) that returns a new defaultdict(list) when called.
    # The outer defaultdict is initialized with this lambda function as its default_factory.
    # Here's what this structure allows:
    # It creates a two-level nested dictionary structure.
    # If you access any key in the outer dictionary that doesn't exist, it automatically creates a new inner defaultdict(list) for that key.
    # For any key in the inner dictionary, if it doesn't exist, it automatically creates an empty list.
    mind_map_defaultdict = defaultdict(lambda: defaultdict(list))

    for chapter, highlight in highlights:
        if chapter:
            mind_map_defaultdict[chapter]["Highlights"].append(highlight)

            # #DEBUG
            # print(f"Mind Map Dictionary ( Default  Dictionary) for chapter {chapter} --> Highlights are : {mind_map_defaultdict[chapter]['Highlights']}")


    # Convert to standard dictionary
    mind_map_dict = {chapter: dict(subchapters) for chapter, subchapters in mind_map_defaultdict.items()}

    #DEBUG
    # print("Mind Map Dictionary ( Normal Dictionary )")
    # for chapter, subchapters in mind_map_defaultdict.items():
    #     print(f"Chapter: {chapter}")
    #     for subchapter, notes in subchapters.items():
    #         print(f"Subchapter: {subchapter} --> Notes: {notes}")






    # Create a directed graph
    G = nx.DiGraph()

    # pos = nx.spiral_layout(G)


    # Add the root node (book title) at level 0
    G.add_node(book_title, level=0, title=book_title)

    # Add nodes and edges
    for chapter, subchapters in mind_map_dict.items():
        # Here change the subchapter from 'Highlight'  to chapter number and Highlight
        subchapter_text = re.match(r"(\d+).", chapter, re.IGNORECASE)
        subchapter_text = subchapter_text.group(1) + " - Highlight" if subchapter_text else "Highlight"

        G.add_node(chapter, level=1, title=chapter)  # Main chapter node
        G.add_edge(book_title, chapter)  # Link chapters to book title

        for subchapter, notes in subchapters.items():
            G.add_node(f"{subchapter_text}", level=2, title=subchapter)  # Subchapter node per chapter
            G.add_edge(chapter, f"{subchapter_text}")  # Link chapter to its unique subchapter

            for note in notes[:5]:  # Limit to 5 notes per subchapter for clarity
                G.add_node(f"{note}", level=3, title=note)  # Unique summary node per chapter
                G.add_edge(f"{subchapter_text}", f"{note}")  # Link subchapter to its highlight


    #DEBUG: Print node and edge counts to verify graph content
    # print(f"Total Nodes: {len(G.nodes())}")
    # print(f"Total Edges: {len(G.edges())}")
    # print("Nodes:", G.nodes())
    # print("Edges:", G.edges())


    # Custom the labels:
    nx.draw(G, with_labels=True, node_size=1500, font_size=25, font_color="yellow", font_weight="bold")
    plt.show()

    # Create an interactive Pyvis network
    net = Network(notebook=True, height="750px", width="100%", directed=True, cdn_resources="remote")

    # Enable physics for better layout
    net.toggle_physics(True)
    # net.show_buttons(filter_=['physics'])

    # Customize node size and text appearance
    net.set_options('''
    var options = {
        "nodes": {
            "shape": "box",
            "size": 60,
            "label" : "center",
            "font": { "size": 10, "face": "arial", "color": "black", "multi": true },
            "margin": 10
        },
        "edges": {
            "arrows": {
            "to": { "enabled": true }
            },
            "color": "black",
            "width": 1
        },
        "physics": {
            "barnesHut": {
            "gravitationalConstant": -2000,
            "centralGravity": 0.1,
            "springLength": 350,
            "springConstant": 0.01,
            "damping": 0.09
            }
        },
        "interaction": {
            "navigationButtons": true,
            "tooltipDelay": 50,
            "hover": true
        }
    }''')


    # Add nodes with color based on level
    for node, data in G.nodes(data=True):
        level = data.get("level", 3)
        color = "lightblue" if level == 1 else "lightgreen" if level == 2 else "lightgray"
        net.add_node(node, label=node, title=data.get("title", node), color=color, physics=True)  # Ensure nodes are visible

    # Add edges
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    # # TEST GRAPH (Manually adding nodes to verify rendering)
    # test_graph = Network(notebook=True, height="750px", width="100%", directed=True, cdn_resources="remote")
    # test_graph.add_node("Test Node 1", color="red")
    # test_graph.add_node("Test Node 2", color="blue")
    # test_graph.add_edge("Test Node 1", "Test Node 2")

    # # Save test graph
    # with tempfile.NamedTemporaryFile(delete=False, suffix="_test.html") as tmp_file:
    #     test_graph.show(tmp_file.name)
    #     print(f"Test graph saved at: {tmp_file.name}")

    # Save main graph
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html_file = tmp_file.name

    # Streamlit app
    st.title("Interactive Mind Map of 'Attached'")
    st.write("Explore the book's chapters, subchapters, and key takeaways interactively. Double-click on a node to expand it.")

    # Display interactive HTML
    with open(html_file, "r", encoding="utf-8") as f:
        html_code = f.read()
    st.components.v1.html(html_code, height=750, scrolling=True)


# Create the mind map
if __name__ == "__main__":
    create_mindmap_attached()
