arch-autorepo
-------------

.. image:: http://www.repostatus.org/badges/1.0.0/concept.svg
   :alt: Project Status: Concept - Minimal or no implementation has been done yet.
   :target: http://www.repostatus.org/#concept

Automatic Arch Linux package rebuilds and repository creation.

This is just a concept right now. The plan is:

* Have a local configuration file (in a fork of this repo? somewhere on disk? still TBD) that lists git repository URLs for packages you want to build (i.e. AUR repos, or your own laid out the same way) and the ref (commit hash/branch/tag) to build.
* The main arch-autorepo script takes a pointer to that config file, and builds all packages in it, or a subset of them
* A helper script to add git repos (by URL) to the config file
* A helper script that clones all repos in the config file, and if there are any commits on master past the hash specified in the config file, shows you a diff to review. Assuming you accept it, the config file is updated for the new hash (this is intended to be an easy way for you to manually verify the safety of package contants, per the `AUR documentation <https://wiki.archlinux.org/index.php/Arch_User_Repository#Build_and_install_the_package>`_).
* An option to bypass any commit hashes in the config file, and just build everything from master.
* The build process will run inside a `Docker <https://www.docker.com/>`_ container for safety and isolation.
* A metadata generation script, which essentially fires up an isolated bash session, sources the PKGBUILD file, captures the important variables, and saves them for later use.
* The main script which installs required dependencies in a clean container, copies in (or mounts?) the source and then triggers a `makepkg` run, capturing the output (both logs and the resulting tarball) and the return code (overall success/failure).
* A test script which uses a clean container or VM and attempts to install the newly-build package, run a pacman `--check` on it, and optionally run some manually-defined test commands (like actually running the software from the package).
* Assuming the build and test both complete, a script to update the package in a `custom Pacman repository <https://wiki.archlinux.org/index.php/Pacman_tips#Custom_local_repository>`_ and then push that updated repository to Amazon S3.
* `makepkg` logging should also be pushed to S3, along with an HTML summary of the build (assuming at least one package was built) with links to the log output and git diffs; this should be able to be configured to be sent via email.

Thoughts/Questions
==================

* can we use one or more of the `AUR Helpers <https://wiki.archlinux.org/index.php/AUR_helpers>`_ to do part of this?
* With this amount of logic, should we just use Jenkins? Then this project would essentially be a set of Jenkins jobs (and a list of required plugins and packages) and the code that they run. That would make a LOT of this simpler, though we'd need good installation instructions (maybe a puppet module for the dependencies). The main questions are, even if we do something like `Jenkins in Docker <https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+with+Docker>`_, would that be too much resource consumption on a "home" system (either processor/CPU or disk consumption) for this project?

References
==========

* The `virtualbox/Vagrant box <https://github.com/jantman/packer-arch-workstation>`_ that I use for testing my archlinux workstation puppet stuff
* `Dockerfile <http://ebalaskas.gr/wiki/Dockerfile/archlinux/openssh>`_ for Arch with SSH
* `how to create a Docker image <https://github.com/BlackIkeEagle/docker-images/blob/master/blackikeeagle/archlinux/create-docker-baseimg.sh>`_ using pacstrap, and the related `Docker hub <https://registry.hub.docker.com/u/base/archlinux/>`_
* Docker's official `installation instructions <https://docs.docker.com/installation/archlinux/>`_ for Arch just use `yaourt` for the git versions.
* `Arch wiki Docker page <https://wiki.archlinux.org/index.php/Docker>`_
* `Arch wiki AUR Installing Packages <https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages>`_
* Can anything from `OBS <http://openbuildservice.org/>`_ help us? It's probably too heavy-weight itself, but maybe some parts are useful?
* maybe `repose <https://github.com/vodik/repose>`_ contains the logic we need to work with the repository?
* `openSuSE Build Service <https://build.opensuse.org/>`_ is publicly accessible and free, and can build for many popular distributions including "Arch Core" and "Arch Extras". It has a `ReST API <https://build.opensuse.org/apidocs/>`_, so theoretically it could be automated to provide the build infrastructure. It also _seems_ to allow building of any package.
* The source to Arch/Pacman's `repo-add <https://projects.archlinux.org/pacman.git/tree/scripts/repo-add.sh.in>`_, which is just a shell script

Status
======

* Docker is at least minimally working:

  * Build the docker image: ``docker build -t archautorepo .``; It should exit with something like ``Successfully built <IMAGE_ID>``
  * Run bash in the image to confirm it works: ``docker run --name=initial_archautorepo --rm -i -t archautorepo /bin/bash`` (the ``--rm`` automatically deletes the container when exited)

* Docker notes:

  * List all containers with ``docker ps -a`` and then delete the container you just used with ``docker rm initial_archautorepo``
  * You can also add a ``--rm`` to the ``run`` command to remove the container automatically when the process exits
  * mount pwd as a volume at /localfs and run the command in it: ``docker run -v /localfs:\`pwd\` -w /localfs -i -t IMAGE_NAME COMMAND``
  * ``docker run --cidfile /path/to/file`` writes the container ID to /path/to/file and closes the file when the run exits

* Idea:

  * Run a new container detatched, with a command that keeps it running: ``docker run --name=initial_archautorepo -d archautorepo /bin/bash -c 'while true; do sleep 10; done'``
  * We can now ``docker exec initial_archautorepo <command>`` and get back the command's output and exit code
  * When done, ``docker stop initial_archautorepo && docker rm initial_archautorepo``
  * So, `docker-py <https://github.com/docker/docker-py>`_ should be able to replicate this. Note that `Avoid docker-py <http://blog.bordage.pro/avoid-docker-py/>`_ has some good information in it.

* Design Question: what's the right way to do this? I think I have an idea of the high-level overview:

  1. In Python locally, clone the git repo for the package. Make sure the clone is clean and at the right hash, and no package files are in the directory.
  2. In Python locally, we'll try to handle dependency resolution, at least figuring out if a package we're building depends on any other packages we're building, and build them first. We should also add deps back into our config file or cache them.
  3. In Python, start a new docker container backgrounded, with two mount points: the git clone, and a workdir.
  4. Place any locally-built deps into the workdir.
  5. Use docker exec(s) to install the deps into the container.
  6. Use docker exec(s) to install any repo (official) deps into the container.
  7. Use a docker exec to run ``makepkg`` in the git clone directory; capture the STDERR, STDOUT and exit code.
  8. In Python locally, find the package file and move it to the right destination (the workdir?)
  9. Repeat for all packages.
  10. Put the packages in a repo.
