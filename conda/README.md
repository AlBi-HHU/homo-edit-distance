# How to Upload a New Release to Anaconda Cloud

0. You already made a new tag, and a new GitHub release. The tag's name should resemble the version number.
1. Edit [meta.yaml](meta.yaml) so that the version in the first line matches the new tag.
2. Now you can either use Docker if you'd like to have up-to-date tools and don't want to mess with Conda too much.

* Either Docker...

```sh
    docker container build --tag build-and-upload:latest .
    docker container run --interactive --tty --rm build-and-upload:latest
```

* ... or natively.

```sh
    conda-build .
    anaconda login
    anaconda upload <insert path as shown in output from conda-build>
```
