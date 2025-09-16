FROM starwitorg/base-python-image:3.13.0 AS build

RUN apt update && apt install --no-install-recommends -y \
    libpq-dev 

# Copy only files that are necessary to install dependencies
COPY poetry.lock poetry.toml pyproject.toml /code/
WORKDIR /code
RUN poetry install
    
# Copy the rest of the project
COPY . /code/

### Main artifact / deliverable image

FROM python:3.13-slim
RUN apt update && apt install --no-install-recommends -y \
    libpq-dev 

RUN /usr/bin/pg_config

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --from=build --chown=appuser:appgroup /code /code
WORKDIR /code

# Switch to non-root user
USER appuser

ENV PATH="/code/.venv/bin:$PATH"
CMD [ "python", "main.py" ]