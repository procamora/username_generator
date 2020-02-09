# username_generator


This is a script to generate a list with possible username using a first name and last name. It is compatible with compound first name and last name





# Requirements

```bash
pip3 install -r requirements.txt --user
```




# Use


```bash
python3 generator.py -f "juan" -l "sanchez perez" -o juan.lst -v
```



![example][example]

[example]: example.png



# Docker


This generator can be launched with a docker, although it has the problem that when generating the usernames dictionary in a text file, a root user is required to read the volume where the output files are saved.

In the future I will have to investigate how to mount the volume within the directory itself to be able to access it more efficiently, although in the tests I have had problems.


```bash
# Create volumen
docker volume create --name data-generartor-usernames
# Generate image docker
docker build -t app-generator .
# Execute image
docker run -it --rm -v data-generartor-usernames:/usr/src/app:rw app-generator
```

The volume directory where the dictionary is located should be _/var/lib/docker/volumes/data-generartor-usernames/_data/output/_ although it can be checked with the following command


```bash
docker volume inspect data-generartor-usernames
```
