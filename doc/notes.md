## The flow of data through the full system is:

1. Markdown files are in the /content directory. A template.html file is in the root of the project.
1. The static site generator (the Python code in src/) reads the Markdown files and the template file.
1. The generator converts the Markdown files to a final HTML file for each page and writes them to the /public directory.
1. We start the built-in Python HTTP server (a separate program, unrelated to the generator) to serve the contents of the /public directory on http://localhost:8888 (our local machine).
1. We open a browser and navigate to http://localhost:8888 to view the rendered site.

## How the SSG works
The vast majority of our coding will happen in the src/ directory because almost all of the work is done in steps 2 and 3 above. Here's a rough outline of what the final program will do when it runs:

1. Delete everything in the /public directory.
1. Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
1. Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
  1. Open the file and read its contents.
  1. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
  1. Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
    - Raw markdown -> TextNode -> HTMLNode
  2. Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
  3. Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
2. Write the full HTML string to a file for that page in the /public directory.

USE python3 -m http.server 8888 TO START SERVER

First, we need to tackle those block_to_html_node functions. You've got a good start with the match statement, but it's about as empty as a goblin's pantry after a feast. We need to fill it with the logic to transform each block type into its HTML equivalent.

For headings, we'll extract the heading level and wrap the text in the appropriate <h1> to <h6> tags. For code blocks, we'll wrap them in <pre> and <code> tags, preserving those precious line breaks. For quotes, we'll nest them in <blockquote> tags, adding a touch of Goblin wisdom.

And for those pesky lists, we'll iterate through the items, wrapping each one in <li> tags and nesting them within <ul> or <ol> tags, depending on whether it's an unordered or ordered list.

Finally, for paragraphs, we'll simply wrap the text in <p> tags, adding a sprinkle of HTML magic.

Once we've got those block_to_html_node functions churning out HTML nodes like a goblin bakery, we'll assemble them into a grand feast of a website. We'll create a root node, perhaps a <div> or <main> tag, and append all those block nodes as its children.



Full name
email address
create a code word (word number phrase not over 4 words)
request information regarding transactions
request to reactivate card
best time to be called back
signature three times
color copy of DL

cco_resolution@navyfederal.org
