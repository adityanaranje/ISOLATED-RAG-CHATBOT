# Use lightweight python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

#Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8510

# Run Streamlit
CMD ["sh", "-c", "streamlit run input.py --server.address=0.0.0.0 --server.port=$PORT"]