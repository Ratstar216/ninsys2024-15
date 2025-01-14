# Requirements:
- uv
- pyzbar
- gemini api key (free)

# Usage
0. create .env and set your api key
1. `uv sync`
2. `uv run python src/test/create_dummy_data.py` (You may not need to do this since you already have test.db)
3. `uv run python src/main.py` **or** `uv run streamlit run src/main_streamlit.py`
  
