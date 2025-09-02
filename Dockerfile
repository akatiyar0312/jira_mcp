# Use a Python base image with uv preinstalled
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Ensure stdout/stderr are not buffered
ENV PYTHONUNBUFFERED=1
# Ensure uv uses copies instead of symlinks (better for Docker)
ENV UV_LINK_MODE=copy

# Copy only dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies (without dev deps or reinstalling project)
RUN uv sync --locked --no-install-project --no-dev

# Copy the rest of the project
COPY . .

# Install the project itself (inside .venv)
RUN uv sync --locked --no-dev

# Ensure the virtual environment is in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the service port
EXPOSE 8000

# Start the MCP server
ENTRYPOINT ["uv", "run", "mcp_server.py"]