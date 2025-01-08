# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code and dependencies
COPY alerting_system.py requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
# ENV SMTP_SERVER=smtp.gmail.com
# ENV SMTP_PORT=587
# ENV EMAIL_ADDRESS=your-email@gmail.com
# ENV EMAIL_PASSWORD=your-email-password

# Run the alerting system
CMD ["python", "alerting_system.py"]

