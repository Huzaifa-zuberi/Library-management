import streamlit as st
import json
import os

# Load and Save Functions
def load_library():
    if os.path.exists("library.txt"):
        with open("library.txt", "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open("library.txt", "w") as file:
        json.dump(library, file)

# Initialize
library = load_library()

# Streamlit App
st.title("📚 Personal Library Manager")

menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add a Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", step=1, format="%d")
    genre = st.text_input("Genre")
    read = st.selectbox("Have you read it?", ["Yes", "No"])

    if st.button("Add Book"):
        book = {
            "title": title,
            "author": author,
            "year": int(year),
            "genre": genre,
            "read": read == "Yes"
        }
        library.append(book)
        save_library(library)
        st.success("Book added successfully!")

elif choice == "Remove a Book":
    st.subheader("Remove a Book")
    titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", titles)
    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success("Book removed successfully!")

elif choice == "Search for a Book":
    st.subheader("Search for a Book")
    search_by = st.radio("Search by", ["Title", "Author"])
    query = st.text_input("Enter search text")

    if query:
        if search_by == "Title":
            results = [book for book in library if book["title"].lower() == query.lower()]
        else:
            results = [book for book in library if book["author"].lower() == query.lower()]

        if results:
            st.write("### Results")
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif choice == "Display All Books":
    st.subheader("Your Library")
    if not library:
        st.info("Your library is empty.")
    else:
        for book in library:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

elif choice == "Display Statistics":
    st.subheader("Library Statistics")
    total_books = len(library)
    read_books = sum(book["read"] for book in library)
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0
    st.metric("Total Books", total_books)
    st.metric("Books Read", read_books)
    st.metric("Percentage Read", f"{percentage_read:.2f}%")
