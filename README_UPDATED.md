# LlaMA-ViSIONX

This project is an Image to Speech GenAI tool that utilizes large language models (LLMs) to convert images into spoken words.

## Installation

To install the required packages, run:

```bash
pip install -r requirements.txt
```

## Usage

To run the application, use:

```bash
streamlit run app.py
```

## Styling the Streamlit App

To make the Streamlit app look more appealing with cool fonts and enhanced styling, you can customize it using the following approaches:

### 1. Use Custom Fonts

You can add custom fonts by injecting CSS styles into your Streamlit app. For example:

```python
import streamlit as st

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)
```

Replace `'Roboto'` with any Google Font of your choice.

### 2. Streamlit Theming

Streamlit supports theming via the `config.toml` file or programmatically. You can customize primary colors, background colors, font sizes, and more. For example, create a `.streamlit/config.toml` file with:

```toml
[theme]
primaryColor = "#1abc9c"
backgroundColor = "#f0f2f6"
secondaryBackgroundColor = "#e6e8eb"
textColor = "#262730"
font = "sans serif"
```

### 3. Additional CSS Styling

You can further enhance the UI by adding custom CSS for buttons, headers, and other elements using the same `st.markdown` method with `unsafe_allow_html=True`.

---

Feel free to explore Streamlit's [theming documentation](https://docs.streamlit.io/library/advanced-features/theming) for more customization options.
