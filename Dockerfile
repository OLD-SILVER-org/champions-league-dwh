# Use Python 3.13.1 as the base image
FROM python:3.13.1  

# Set the working directory inside the container
WORKDIR /etl_project

# Install system dependencies required for Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg fonts-liberation \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 \
    libatspi2.0-0 libcups2 libdbus-1-3 libgbm1 \
    libgtk-3-0 libnspr4 libnss3 libvulkan1 \
    libxcomposite1 libxdamage1 libxfixes3 \
    libxkbcommon0 libxrandr2 xdg-utils && \
    rm -rf /var/lib/apt/lists/*  # Clean up cache

# Download and install Google Chrome
RUN wget -q -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome.deb && \
    rm google-chrome.deb  # Remove the installer after installation

# Install ChromeDriver matching Chrome's version
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /usr/local/bin/chromedriver

# Copy requirements.txt first to optimize Docker caching
COPY requirements.txt /etl_project/
RUN pip install -r /etl_project/requirements.txt  # Install dependencies

# Copy the entire project into the container
COPY . /etl_project/

# Set PYTHONPATH to allow easier module imports
ENV PYTHONPATH="/etl_project"

# Set the default ETL mode to 'new' but allow override via environment variable
ENV ETL_MODE=new
# Install Rust
RUN apt-get update && apt-get install -y curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Execute the ETL process based on the mode (old or new)
CMD ["sh", "-c", "python /etl_project/tasks/etl_main.py $ETL_MODE"]
