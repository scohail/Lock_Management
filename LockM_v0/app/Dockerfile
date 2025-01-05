FROM python:3.9-slim

WORKDIR /app

# Update package lists and install Java
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    wget \
    gnupg \
    && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | apt-key add - && \
    echo "deb https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list && \
    apt-get update --fix-missing && \
    apt-get install -y temurin-11-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask-wtf

COPY . .

CMD ["python", "app.py"]