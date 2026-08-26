FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instalar dependencias básicas
RUN apt-get update && \
    apt-get install -y \
        software-properties-common \
        curl \
        git \
        build-essential && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
        python3.12 \
        python3.12-venv \
        python3.12-dev \
        python3-pip

# Instalar uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:${PATH}"

# Copiar archivos del proyecto
COPY pyproject.toml uv.lock README.md ./
COPY app ./app
COPY src ./src

# Instalar ODBC Driver
COPY docker/install_odbc.sh /tmp/install_odbc.sh

RUN chmod +x /tmp/install_odbc.sh && \
    /tmp/install_odbc.sh && \
    rm /tmp/install_odbc.sh

# Instalar dependencias Python
RUN uv sync --python python3.12 --frozen

EXPOSE 8000

CMD ["uv", "run", "--python", "python3.12", "python", "app/server.py"]