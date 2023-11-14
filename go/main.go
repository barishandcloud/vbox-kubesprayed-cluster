package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var (
	mongoHost = getEnv("MONGO_HOST", "192.168.164.128")
	dbName    = "employees"
	collName  = "employee_data"
)

type Employee struct {
	UID        string    `json:"UID" bson:"UID"`
	EmployeeID string    `json:"EmployeeID" bson:"EmployeeID"`
	MetaInfo   MetaInfo  `json:"metainfo" bson:"metainfo"`
}

type MetaInfo struct {
	InsertedBy string    `json:"inserted_by" bson:"inserted_by"`
	Date       string    `json:"date" bson:"date"`
	Time       string    `json:"time" bson:"time"`
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func connectDB() (*mongo.Client, error) {
	clientOptions := options.Client().ApplyURI(fmt.Sprintf("mongodb://%s:27017/", mongoHost))
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		return nil, err
	}

	return client, nil
}

func generateEmployeeID(uid string) string {
	return fmt.Sprintf("employee-%s", uid)
}

func getMetadata() MetaInfo {
	podName := getEnv("POD_NAME", "unknown_pod")
	currentTime := time.Now()
	dateToday := currentTime.Format("2006-01-02")
	timeNow := currentTime.Format("15:04:05")

	return MetaInfo{
		InsertedBy: podName,
		Date:       dateToday,
		Time:       timeNow,
	}
}

func updateEmployee(c *gin.Context) {
	uid := c.Param("uid")

	client, err := connectDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to connect to the database"})
		return
	}
	defer client.Disconnect(context.Background())

	collection := client.Database(dbName).Collection(collName)

	// Check if the UID exists in the database
	existingEmployee := Employee{}
	err = collection.FindOne(context.Background(), bson.M{"UID": uid}).Decode(&existingEmployee)
	if err == nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "EmployeeID already exists for this UID"})
		return
	}

	// If the UID doesn't exist, create a new entry with metadata
	employeeID := generateEmployeeID(uid)
	metadata := getMetadata()
	newEmployee := Employee{
		UID:        uid,
		EmployeeID: employeeID,
		MetaInfo:   metadata,
	}

	_, err = collection.InsertOne(context.Background(), newEmployee)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to insert new employee"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "New employee created"})
}

func getEmployee(c *gin.Context) {
	uid := c.Param("uid")

	client, err := connectDB()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to connect to the database"})
		return
	}
	defer client.Disconnect(context.Background())

	collection := client.Database(dbName).Collection(collName)

	// Check if the UID exists in the database
	existingEmployee := Employee{}
	err = collection.FindOne(context.Background(), bson.M{"UID": uid}).Decode(&existingEmployee)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": "Employee with this UID not found"})
		return
	}

	c.JSON(http.StatusOK, existingEmployee)
}

func main() {
	r := gin.Default()

	r.PUT("/update_employee/:uid", updateEmployee)
	r.GET("/get_employee/:uid", getEmployee)

	if err := r.Run(":9000"); err != nil {
		log.Fatal(err)
	}
}
