package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"math/rand"
	"net/http"
	"strings"
)

const letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

var alphabetSize = len(letters)

func randomString(n int) string {
	sb := strings.Builder{}
	sb.Grow(n)

	for i := 0; i < n; i++ {
		sb.WriteByte(letters[rand.Intn(alphabetSize)])
	}

	return sb.String()
}

func info(c *gin.Context) {
	randomStr := randomString(50)
	c.JSON(http.StatusOK, gin.H{"random_string": randomStr})
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gin.Recovery())
	r.GET("/info", info)
	err := r.Run("0.0.0.0:8080")
	if err != nil {
		fmt.Println("Error starting upstream service: ", err)
	}
}
