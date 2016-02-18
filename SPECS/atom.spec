Name:           atom
Version:        1.6.0~beta4
Release:        0.1%{?dist}
Summary:        A hackable text editor for the 21st Century.
License:        MIT
URL:            https://atom.io/
AutoReqProv:    no # Avoid libchromiumcontent.so missing dependency
Prefix:         /usr

Requires: lsb-core-noarch

%description
A hackable text editor for the 21st Century.

%install
mkdir -p "%{buildroot}//usr/share/atom/"
cp -r "Atom"/* "%{buildroot}//usr/share/atom/"
mkdir -p "%{buildroot}//usr/bin/"
ln -sf "../share/atom/resources/app/apm/node_modules/.bin/apm" "%{buildroot}//usr/bin/apm"
cp atom.sh "%{buildroot}//usr/bin/atom"
chmod 755 "%{buildroot}//usr/bin/atom"
mkdir -p "%{buildroot}//usr/share/applications/"
cp "atom.desktop" "%{buildroot}//usr/share/applications/"

for i in 1024 512 256 128 64 48 32 24 16; do
  mkdir -p "%{buildroot}//usr/share/icons/hicolor/${i}x${i}/apps"
  cp "icons/${i}.png" "%{buildroot}//usr/share/icons/hicolor/${i}x${i}/apps/atom.png"
done

%files
/usr/bin/atom
/usr/bin/apm
/usr/share/atom/
/usr/share/applications/atom.desktop
/usr/share/icons/hicolor/
