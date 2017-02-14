#
# spec file for package sublime_text
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:    sublime_text
Version: 3126
Release: 1
Group: Applications/Editors
%ifarch x86_64
Source: https://download.sublimetext.com/%{name}_3_build_%{version}_x64.tar.bz2
%else
Source: https://download.sublimetext.com/%{name}_3_build_%{version}_x32.tar.bz2
%endif
Summary: Sublime Text 3
URL: http://www.sublimetext.com/3
License: SUSE-NonFree
BuildRoot: %{_tmppath}/%{name}-root
Vendor: Sublime Text Authors
Requires: libgobject-2.0.so.0
Requires: librt.so.1
Requires: libglib-2.0.so.0
Requires: libpthread.so.0
Requires: libdl.so.2
Requires: libX11.so.6
Requires: libm.so.6
Requires: libc.so.6
Requires: libxcb.so.1
Requires: libXau.so.6

%description
Sublime Text 3 for GNU/Linux is a sophisticated text editor for code, markup and prose.

%prep
%setup -q -c -n %{name}

%build
# Do nothing...

%install
# Unpacking...
rm -rf %{buildroot}

# Creating general directories...
mkdir -p %{buildroot}/usr/share/applications/
mkdir -p %{buildroot}/opt/%{name}/
mkdir -p %{buildroot}/usr/bin/

# Installing to working directory from official package...
mv "%_builddir/%{name}/%{name}_3" %_builddir/%{name}/%{name}
cp -fpr %_builddir/%{name}/%{name}/* %{buildroot}/opt/%{name}/
rm -f %{buildroot}/opt/%{name}/%{name}.desktop
chmod +x %{buildroot}/opt/%{name}/%{name}
ln -sf /opt/%{name}/%{name} %{buildroot}/usr/bin/sublime3

# Creating desktop icon...
echo "[Desktop Entry]" > %{buildroot}/usr/share/applications/%{name}.desktop
echo "GenericName=Text Editor" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Name=Sublime Text 3" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Name[ru]=Sublime Text 3" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Comment=Edit text files" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Exec=/opt/%{name}/sublime_text" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Icon=/opt/%{name}/Icon/256x256/sublime-text.png" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Terminal=false" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Type=Application" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Encoding=UTF-8" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "Categories=Utility;TextEditor;" >> %{buildroot}/usr/share/applications/%{name}.desktop
echo "MimeType=application/javascript;application/json;application/x-desktop;application/x-httpd-eruby;application/x-httpd-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/x-ruby;application/x-bash;application/x-csh;application/x-sh;application/x-zsh;application/x-shellscript;application/x-sql;application/x-tcl;application/xhtml+xml;application/xml;application/xml-dtd;application/xslt+xml;text/coffeescript;text/css;text/html;text/plain;text/xml;text/xml-dtd;text/x-bash;text/x-c++;text/x-c++hdr;text/x-c++src;text/x-c;text/x-chdr;text/x-csh;text/x-csrc;text/x-dsrc;text/x-diff;text/x-go;text/x-java;text/x-java-source;text/x-makefile;text/x-markdown;text/x-objc;text/x-perl;text/x-php;text/x-python;text/x-ruby;text/x-sh;text/x-zsh;text/yaml;inode/directory;" >> %{buildroot}/usr/share/applications/%{name}.desktop

# Generating list of files...
find %{buildroot} -not -type d -printf "\"/%%P\"\n" | sed '/\/man\//s/$/\*/' > manifest

%files -f manifest
%defattr(-,root,root)
%dir /opt/%{name}
%dir /opt/%{name}/Icon/
%dir /opt/%{name}/Icon/*
%dir /opt/%{name}/Packages

%changelog
