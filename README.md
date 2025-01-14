# Requirements:
- ~~uv~~
- ~~pyzbar~~
- gemini api key (free)

# Usage
0. create .env and set your api key
1. `docker compose up -d` and `docker exec -it [container-id] /bin/bash`
2. `uv sync`
3. `uv run python src/test/create_dummy_data.py` (You may not need to do this since you already have test.db)
4. `uv run streamlit run src/main_streamlit.py`
  
