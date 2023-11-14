# Use the official Go image as the base image
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install required dependencies
RUN go get github.com/gin-gonic/gin
RUN go get go.mongodb.org/mongo-driver/mongo
RUN go get go.mongodb.org/mongo-driver/mongo/options
RUN go get go.mongodb.org/mongo-driver/bson

# Build the Go application
RUN go build -o main .

# Expose the port on which the application will run
EXPOSE 9000

# Command to run the executable
CMD ["./main"]
