docker stop cnt-my-running-app
docker rm cnt-my-running-app
docker rmi my-python-app
docker build -f dockerfile -t my-python-app .
docker run -it --rm --name cnt-my-running-app my-python-app