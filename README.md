# Comparing Go and Python for a simple API

This is a simple API that calls two upstream services, combines the results, and returns them to the client. The API is written in both Go and Python to compare the two languages.

I assume you have a recent version of docker installed and also ddosify.

If you need to install ddosify on a Mac, you can do so with homebrew:
```shell
brew install ddosify/tap/ddosify
``` 

## Running the API
```shell
docker compose up
```

## Running the tests
```shell
#Directly hammer the go solution: 
ddosify -n 1000 -l waved -t "http://localhost:8123/{{_randomString}}"

#Directly hammer the python solution: 
ddosify -n 1000 -l waved -t "http://localhost:8124/{{_randomString}}"

#Go through nginx: 
ddosify -n 1000 -l waved -t "http://localhost/go/{{_randomString}}"

#Python through nginx: 
ddosify -n 1000 -l waved -t "http://localhost/python/{{_randomString}}"
```