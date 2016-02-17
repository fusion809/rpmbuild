# rpmbuild
This is the repository I use whenever I wish to build an RPM package for Atom, manually. Pre-built Atom binaries can be installed from https://github.com/atom/atom/releases. To create all the necessary subfolders to this repo (which I have not included due to the effect they have on the size of this repository) and download the source code tarball for Atom into `SOURCES/` run `./setup.sh`. To update the `SPECS/atom.spec` file to the latest stable version available, then build and install it run `./update.sh`. If Atom is the latest stable version it will give the output "Atom is up-to-date". 
