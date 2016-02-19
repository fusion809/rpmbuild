Name:           atom
Version:        1.5.3
Release:        0
Summary:        A hackable text editor for the 21st century
License:        MIT
Group:          Productivity/Publishing/Other
Url:            https://atom.io/
Source0:        v%{version}.tar.gz
BuildRequires:  git-core
BuildRequires:  hicolor-icon-theme
BuildRequires:  npm
BuildRequires:  nodejs-packaging
BuildRequires:  libgnome-keyring-devel
BuildRequires:  python-setuptools
BuildRequires:  update-desktop-files
# MANUAL BEGIN
Requires:       nodejs
Requires:       python-http-parser
# MANUAL END
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Atom is a text editor that's modern, approachable, yet hackable to the core
- a tool you can customize to do anything but also use productively without
ever touching a config file.

%prep
%setup -q
sed -i -e 's/<%= installDir %>/\/usr/g' \
       -e 's/<%= iconPath %>/atom/g' \
       -e 's/Development;//g' resources/linux/atom.desktop.in

%build
# Hardened package
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"
until ./script/build 2>&1; do :; done

%install
script/grunt install --install-dir "%{buildroot}%{_prefix}"
# copy over icons in sizes that most desktop environments like
for i in 1024 512 256 128 64 48 32 24 16; do
    install -Dm 0644 /tmp/atom-build/icons/${i}.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done
%suse_update_desktop_file %{name}

%post
%desktop_database_post
%icon_theme_cache_post

%postun
%desktop_database_postun
%icon_theme_cache_postun

%files
%defattr(-,root,root,-)
%doc README.md docs/
%{license} LICENSE.md
%{_bindir}/atom
%{_bindir}/apm
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/applications/atom.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_datadir}/%{name}/libgcrypt.so.*
%exclude %{_datadir}/%{name}/libnotify.so.*

%changelog
