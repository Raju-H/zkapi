# Use multi-stage builds to keep the final image small
FROM python:3.12.6-alpine as builder

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app

# Final stage
FROM python:3.12.6-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Copy the entrypoint script
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["sh", "/entrypoint.sh"]

# Switch to the non-root user
USER appuser
