FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y \
    gcc g++ zbar-tools
 


WORKDIR /app