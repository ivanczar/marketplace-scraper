FROM python:3.10

# Install dependencies, including cron and supervisor
RUN apt-get update && apt-get install -y \
    chromium-driver \
    supervisor \
    cron \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# Copy application code to /app
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install --upgrade pip && pip install hatch
RUN pip install .

# Add and configure cron job
COPY ./config/crontab /etc/cron.d/marketplace_cron
RUN chmod 0644 /etc/cron.d/marketplace_cron && \
crontab /etc/cron.d/marketplace_cron

# Copy Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose logs for easier debugging
VOLUME /var/log

EXPOSE 5000

# Start Supervisor as the container's main process
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
