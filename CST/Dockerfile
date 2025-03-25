# Use official Python image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "CST.wsgi:application"]
