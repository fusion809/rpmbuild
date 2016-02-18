Name:           atom-beta
Version:        1.6.0
Release:        4
Summary:        A hackable text editor for the 21st century
License:        MIT
Group:          Productivity/Publishing/Other
Url:            https://atom.io/
Source0:        v%{version}-beta%{release}.tar.gz
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
BuildRoot:      %{_tmppath}/atom-%{version}-beta%{release}-build

%description
Atom is a text editor that's modern, approachable, yet hackable to the core
- a tool you can customize to do anything but also use productively without
ever touching a config file.

This is the beta release of Atom.

%prep
%setup -q -n atom-%{version}-beta%{release}
sed -i -e "s|<%= installDir %>/share/<%= appFileName %>/atom %U|/usr/bin/atom %U|g" \
      -e "s/Development;//g" \
      -e "s/<%= iconPath %>/atom-beta/g" \
      resources/linux/atom.desktop.in > resources/linux/atom-beta.desktop

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
mv %{buildroot}%{_datadir}/applications/atom.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
%desktop_database_post
%icon_theme_cache_post

%postun
%desktop_database_postun
%icon_theme_cache_postun

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING.md README.md docs/
%{license} LICENSE.md
%{_bindir}/atom
%{_bindir}/apm
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/atom
%{_datadir}/applications/atom-beta.desktop
%{_datadir}/icons/hicolor/*/apps/atom-beta.png
%exclude %{_datadir}/atom/libgcrypt.so.*
%exclude %{_datadir}/atom/libnotify.so.*

%changelog
