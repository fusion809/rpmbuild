# Not working
%global   debug_package %{nil}
Name:     runescape-launcher
Version:  2.2.2
Release:  1
Summary:  Massively Multiplayer Online Role-Playing Game by Jagex (NXT Client)
License:  Proprietary
URL:      https://www.runescape.com
Provides: %{name} = %{version}-%{release}
Source0:  https://content.runescape.com/downloads/ubuntu/pool/non-free/r/runescape-launcher/runescape-launcher_2.2.2_amd64.deb

Requires: hicolor-icon-theme
Requires: xdg-utils
Requires: libGLEW
Requires: gstreamer-plugins-base
Requires: libcurl7520
Requires: libpng12
Requires: SDL2
Requires: webkitgtk

%description
The NXT Client for the MMORPG RuneScape

%prep
%setup -q -c -T
ar x %{SOURCE0}
tar -xJf data.tar.xz

%build

%install
mkdir -p %{buildroot}%{_datadir}/games/%{name}
cp -frp ./usr/share/games/runescape-launcher/runescape %{buildroot}%{_datadir}/games/%{name}

mkdir -p %{buildroot}%{_bindir}
ln -sf %{_datadir}/games/%{name}/runescape %{buildroot}%{_bindir}/runescape-launcher

install -m 0644 -D -p ./usr/share/applications/runescape-launcher.desktop \
    %{buildroot}%{_datadir}/applications/runescape-launcher.desktop

for size in 16 24 32 48 64 256 512; do
    install -p -D -m 644 .%{_datadir}/icons/hicolor/${size}x${size}/apps/runescape.png \
        %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/runescape.png
done

desktop-file-validate %{buildroot}%{_datadir}/applications/runescape-launcher.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/runescape-launcher
%{_datadir}/applications/runescape-launcher.desktop
%{_datadir}/games/%{name}/runescape
%{_datadir}/icons/hicolor/*
