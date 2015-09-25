arch-autorepo
-------------

.. image:: http://www.repostatus.org/badges/1.0.0/concept.svg
   :alt: Project Status: Concept - Minimal or no implementation has been done yet.
   :target: http://www.repostatus.org/#concept

Automatic Arch Linux package rebuilds and repository creation.

This is just a concept right now. The plan is:

* Maintain a Git repository containing your PKGBUILDS (and their patches, etc.) Per the `advice <https://gist.github.com/jantman/e9a6b9ed360f67bb780e>`_ of many in the Arch community, don't build anything from AUR without examining it manually first, and pulling it into local source control.
* A script that takes a pointer to an external (i.e. AUR) package and either pulls it into your git repo, or updates it if already present (you then manually review the diff and commit it).
* A metadata generation script, which essentially fires up an isolated bash session (in a chroot as a different user? in a `Docker <https://www.docker.com/>`_ container? in a Vagrant VM?), sources the PKGBUILD file, captures the important variables, and writes them out to a metadata.json file which is committed back to the git repo.
* A script that "figures out" (possibly with additional configuration) the current/latest version of a package's upstream, and is capable of updating a PKGBUILD file for it - essentially, the configuration that we need in order to do automated builds of upstream releases or nightly source control snapshots. The updated PKGBUILD should be committed to git and pushed, with a special name (i.e. AUTOPKGBUILD.release and AUTOPKGBUILD.nightly).
* A package build script that installs required dependencies in an isolated environment (once again, chroot, Docker, or a full-out VM) and then triggers a `makepkg` run there, capturing the output (both logs and the resulting tarball) and the return code (overall success/failure).
* A test script which uses a clean container or VM and attempts to install the newly-build package, run a pacman `--check` on it, and optionally run some manually-defined test commands (like actually running the software from the package).
* Assuming the build and test both complete, a script to update the package in a `custom Pacman repository <https://wiki.archlinux.org/index.php/Pacman_tips#Custom_local_repository>`_ and then push that updated repository to Amazon S3.
* `makepkg` logging should also be pushed to S3, along with an HTML summary of the build (assuming at least one package was built) with links to the log output and git diffs; this should be able to be configured to be sent via email.

Thoughts/Questions
==================

* can we use one or more of the `AUR Helpers <https://wiki.archlinux.org/index.php/AUR_helpers>`_ to do part of this?
* With this amount of logic, should we just use Jenkins? Then this project would essentially be a set of Jenkins jobs (and a list of required plugins and packages) and the code that they run. That would make a LOT of this simpler, though we'd need good installation instructions (maybe a puppet module for the dependencies). The main questions are, even if we do something like `Jenkins in Docker <https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+with+Docker>`_, would that be too much resource consumption on a "home" system (either processor/CPU or disk consumption) for this project?
* To do this, we'd really need some up-to-date containers or VMs running Arch - at least the last official release image, and that plus the latest updates. Ideally this process would be automated too, but that's a totally different problem.

References
==========

* Arch Vagrant boxes - so far, all the ones that I could `find <https://github.com/terrywang/vagrantboxes/blob/master/archlinux-x86_64.md>`_ are hand-made. Crap.
* `Dockerfile <http://ebalaskas.gr/wiki/Dockerfile/archlinux/openssh>`_ for Arch with SSH
* `how to create a Docker image <https://github.com/BlackIkeEagle/docker-images/blob/master/blackikeeagle/archlinux/create-docker-baseimg.sh>`_ using pacstrap, and the related `Docker hub <https://registry.hub.docker.com/u/base/archlinux/>`_
* Docker's official `installation instructions <https://docs.docker.com/installation/archlinux/>`_ for Arch just use `yaourt` for the git versions.
* `Arch wiki Docker page <https://wiki.archlinux.org/index.php/Docker>`_
* `Arch wiki AUR Installing Packages <https://wiki.archlinux.org/index.php/Arch_User_Repository#Installing_packages>`_
* Can anything from `OBS <http://openbuildservice.org/>`_ help us? It's probably too heavy-weight itself, but maybe some parts are useful?
* maybe `repose <https://github.com/vodik/repose>`_ contains the logic we need to work with the repository?
* `openSuSE Build Service <https://build.opensuse.org/>`_ is publicly accessible and free, and can build for many popular distributions including "Arch Core" and "Arch Extras". It has a `ReST API <https://build.opensuse.org/apidocs/>`_, so theoretically it could be automated to provide the build infrastructure. It also _seems_ to allow building of any package.
