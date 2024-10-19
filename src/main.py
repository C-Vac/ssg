import sys
from utils import markdown_to_html_node


def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts a Markdown file to an HTML file.

    Args:
        markdown_file (str): The path to the Markdown file.
        html_file (str): The path to the HTML file to be created.
    """
    try:
        with open(markdown_file, "r") as f:
            markdown = f.read()

        html_node = markdown_to_html_node(markdown)
        html = (
            """
<!doctype html><head>
  <base href="/goblin/">
</head>" """
            + html_node.to_html()
        )

        with open(html_file, "w") as f:
            f.write(html)

        print(f"Successfully converted {markdown_file} to {html_file}")

    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <markdown_file> <html_file>")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]
    convert_markdown_to_html(markdown_file, html_file)
