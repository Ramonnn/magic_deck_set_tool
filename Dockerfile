FROM python:3.12-slim

# Install pipx and poetry
RUN apt-get update \
	&& python -m pip install --upgrade pip \
	&& pip install pipx \
	&& pipx install poetry

# Set the PATH for pipx to work
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Copy pyproject.toml and poetry.lock if available
COPY pyproject.toml poetry.lock* /app/

# Install dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . /app

# Run the application
CMD ["poetry", "run", "python", "setchecker.py"]
