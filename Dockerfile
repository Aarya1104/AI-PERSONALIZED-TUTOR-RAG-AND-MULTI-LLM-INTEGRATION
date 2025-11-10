FROM python:3.10.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBIAN_FRONTEND=noninteractive \
    OLLAMA_HOST=0.0.0.0:11434 \
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS"

WORKDIR /app

# Install system dependencies including updated SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    ca-certificates \
    cmake \
    git \
    libopenblas-dev \
    pkg-config \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Build and install SQLite 3.43.0 (latest stable)
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-3430000.tar.gz \
    && tar xvfz sqlite-autoconf-3430000.tar.gz \
    && cd sqlite-autoconf-3430000 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3430000* \
    && ldconfig

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Upgrade pip and install pysqlite3-binary to use newer SQLite
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pysqlite3-binary && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY config.py ./

# Create necessary directories
RUN mkdir -p data/chroma_db data/conversations uploads models && \
    chmod -R 777 data uploads models

# Expose ports
# 7866 - Gradio app
# 11434 - Ollama API
EXPOSE 7866 11434

# Copy and set permissions for startup script
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7866/ || exit 1

# Run the startup script
CMD ["/startup.sh"]
