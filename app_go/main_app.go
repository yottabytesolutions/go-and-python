package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"

	"github.com/gin-gonic/gin"
)

const (
	serviceOneURL = "http://upstream_service_one_go:8080/info"
	serviceTwoURL = "http://upstream_service_two_go:8080/info"
)

type InfoResponse struct {
	RandomString string `json:"random_string"`
}

var httpClient = &http.Client{
	Transport: &http.Transport{
		MaxIdleConnsPerHost: 10,
		MaxConnsPerHost:     5000,
		DisableKeepAlives:   true,
		DisableCompression:  true,
	},
}

func fetchInfo(url string, ch chan InfoResponse, wg *sync.WaitGroup) {
	defer wg.Done()

	resp, err := httpClient.Get(url)
	if err != nil {
		fmt.Println("Error fetching info:", err)
		return
	}
	defer func(Body io.ReadCloser) {
		err := Body.Close()
		if err != nil {
			fmt.Println("Error closing response body:", err)
		}
	}(resp.Body)

	var info InfoResponse
	err = json.NewDecoder(resp.Body).Decode(&info)
	if err != nil {
		fmt.Println("Error decoding response:", err)
		return
	}

	ch <- info
}

func hello(c *gin.Context) {
	name := c.Param("name")

	wg := &sync.WaitGroup{}
	ch := make(chan InfoResponse, 2)

	wg.Add(2)
	go fetchInfo(serviceOneURL, ch, wg)
	go fetchInfo(serviceTwoURL, ch, wg)

	wg.Wait()
	close(ch)

	infoResponses := make([]InfoResponse, 2)
	i := 0
	for info := range ch {
		infoResponses[i] = info
		i++
	}

	c.JSON(
		http.StatusOK, gin.H{
			"hello":  name,
			"result": infoResponses,
		},
	)
}

func main() {
	gin.SetMode(gin.ReleaseMode)
	r := gin.New()
	r.Use(gin.Recovery())
	r.GET("/:name", hello)
	err := r.Run("0.0.0.0:8123")
	if err != nil {
		fmt.Println("Error starting server:", err)
	}
}
