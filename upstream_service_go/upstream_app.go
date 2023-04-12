package main

import (
	"github.com/gin-gonic/gin"
	"math/rand"
	"net/http"
	"strings"
)

func randomString(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	sb := strings.Builder{}
	sb.Grow(n)

	for i := 0; i < n; i++ {
		sb.WriteByte(letters[rand.Intn(len(letters))])
	}

	return sb.String()
}

func info(c *gin.Context) {
	//if rand.Float32() < 0.1 {
	//	c.String(http.StatusInternalServerError, "Internal Server Error")
	//	return
	//}

	randomStr := randomString(50)
	c.JSON(http.StatusOK, gin.H{"random_string": randomStr})
}

func main() {
	r := gin.Default()
	r.GET("/info", info)
	r.Run("0.0.0.0:8080")
}
