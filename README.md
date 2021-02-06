# Sitemapper

It crawls the given web page in multi threaded, which it can concurrently make request 25. 
After finishing crawls it prints out to screen both unique accessible web pages list and relative links as tree.  

### Pre-requirements

* docker

### Build
After cloning the repository and locating to path which has the Dockerfile:

```
docker build -t sitemapper .
```

### Run

There is an environment variable _**DEST_URL**_ which is http://www.piedpiper.com/ as default value.

```
docker run -it sitemapper:latest
```

or

```
docker run -it -e DEST_URL=http://www.piedpiper.com/ sitemapper:latest
```