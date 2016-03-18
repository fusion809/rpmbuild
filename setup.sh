SPEC=SPECS
if ! [[ -d BUILD ]]; then
	mkdir BUILD
fi

if ! [[ -d BUILDROOT ]]; then
	mkdir BUILDROOT
fi

if ! [[ -d RPMS ]]; then
	mkdir RPMS
fi

if ! [[ -d SRPMS ]]; then
	mkdir SRPMS
fi

verc=$(sed -n 's/Version:\s\s\s\s\s\s\s\s*//p' $SPEC/atom.spec)
if [[ -f SOURCES/v$verc.tar.gz ]]; then
	wget -cqO- https://github.com/atom/atom/archive/v$verc.tar.gz > SOURCES/v$verc.tar.gz
fi
