Name:           codelite
Version:        9.2
Release:        1%{?dist}
License:        GPLv2+
Group:          Development/Tools
Summary:        CodeLite is a powerful open-source, cross platform code editor for C/C++
URL:            http://codelite.sourceforge.net
Source:         http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%if %{fedora} > 21
# clang also provides clang-format
Requires:       xterm libssh clang
%if %{fedora} == 23
#fed 23 has a liblldb which breaks compilation
BuildRequires:	wxGTK3-devel cmake clang-devel libssh-devel hunspell-devel sqlite-devel desktop-file-utils
%else
BuildRequires:	wxGTK3-devel  cmake clang-devel lldb-devel libssh-devel hunspell-devel sqlite-devel desktop-file-utils
%endif
%else
# clang also provides clang-format
Requires:       xterm libssh clang
BuildRequires:	wxGTK31-devel cmake clang-devel lldb-devel libssh-devel hunspell-devel
%endif

# Needed to prevent cpio "digest mismatch" errors when trying to install an rpm that incorporates
# already-prelinked .so libs. See http://www.redhat.com/archives/rhl-devel-list/2009-December/msg00813.html
%global __prelink_undo_cmd %{nil}

# Filter out these false-alarms from 'requires', as the package itself supplies them!
%{?filter_setup:
%filter_from_requires libcodeliteu.so; libpluginu.so; libwxscintillau.so; libwxsqlite3u.so;
%filter_setup
}

%description
CodeLite uses a sophisticated, yet intuitive interface which allows
users to easily create, build and debug complex projects.

%prep
%setup -q

%build
mkdir -p build_release
%if %{fedora} > 21
export PATH=/usr/libexec/wxGTK31/:$PATH
(cd build_release && cmake -G "Unix Makefiles" -DCOPY_WX_LIBS=1 -DAUTOGEN_REVISION=0 ..)
%else
(cd build_release && cmake -G "Unix Makefiles" -DCOPY_WX_LIBS=1 -DAUTOGEN_REVISION=0 ..)
%endif
(cd build_release && make %{?_smp_mflags})

%install
%{__rm} -rf $RPM_BUILD_ROOT
(cd build_release && make DESTDIR=$RPM_BUILD_ROOT install)

# Create the .desktop on the fly, as it's not quite the same as the tarball one
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Name=%{name}
GenericName=C/C++ IDE
Comment=An IDE for creating C/C++ programs
Exec=%{name} %f
Icon=codelite.png
Terminal=false
Type=Application
MimeType=application/x-codelite-workspace;application/x-codelite-project;
Categories=Development;
StartupNotify=false
Version=1.0
EOF

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mime/packages/
cp -p %{name}.xml $RPM_BUILD_ROOT%{_datadir}/mime/packages/

cp -p $RPM_BUILD_ROOT%{_datadir}/%{name}/images/cubes.png $RPM_BUILD_ROOT%{_datadir}/%{name}/images/codelite.png # Without this line, no icon was displayed in the kde menu or taskbar

mkdir -p $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/mimetypes/
cp -p $RPM_BUILD_ROOT%{_datadir}/%{name}/images/cubes.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-%{name}-workspace.png
cp -p $RPM_BUILD_ROOT%{_datadir}/%{name}/images/cubes.png $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-%{name}-project.png

desktop-file-install  --delete-original       \
          --dir $RPM_BUILD_ROOT%{_datadir}/applications            \
                $RPM_BUILD_ROOT%{_datadir}/applications/codelite.desktop

%find_lang %{name}

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS LICENSE COPYING
%{_bindir}/codelite
%{_bindir}/codelite_indexer
%{_bindir}/codelite_cppcheck
%{_bindir}/codelite_fix_files
%{_bindir}/codelite_exec
%{_bindir}/codelite_kill_children
%{_bindir}/codelite_xterm
%{_bindir}/codelite-terminal
%{_bindir}/codelite-cc
%{_bindir}/codelite-echo
%if %{fedora} != 23
%{_bindir}/codelite-lldb
%endif
%{_bindir}/codelite-make
%{_datadir}/codelite
%{_datadir}/applications/codelite.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-%{name}-workspace.png
%{_datadir}/icons/hicolor/32x32/mimetypes/application-x-%{name}-project.png
%{_datadir}/icons/hicolor/32x32/apps/codelite.png
%{_datadir}/icons/hicolor/32x32@2x/apps/codelite.png
%{_datadir}/icons/hicolor/64x64/apps/codelite.png
%{_datadir}/icons/hicolor/64x64@2x/apps/codelite.png
%{_datadir}/icons/hicolor/128x128/apps/codelite.png
%{_datadir}/icons/hicolor/128x128@2x/apps/codelite.png
%{_datadir}/icons/hicolor/256x256/apps/codelite.png
%{_datadir}/icons/hicolor/256x256@2x/apps/codelite.png
%{_libdir}/%{name}
%{_mandir}/man1/codelite.1*
%{_mandir}/man1/codelite-make.1*
%{_mandir}/man1/codelite_fix_files.1*

%post
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%changelog
* Thu Jun 23 2016 DH
- Update for fedora24
* Fri Dec 04 2015 DH
- Update for icon change
* Wed Nov 04 2015 DH
- Fixes for fedora23 build
* Wed May 27 2015 DH
- Use the official wxGTK3 package for fedora22 builds
- Don't include the wx libs in the CL binary for fedora22
- Updated .*Requires accordingly
* Sat May 02 2015 DH
- Updated .*Requires and %files as CL no longer supplies clang/lldb
* Thu Feb 05 2015 DH
- Updated %files
* Tue May 13 2014 DH
- Added new files to %files
- Updated BuildRequires (libedit)
* Fri Jan 10 2014 DH
- Added a new file to %files
- Updated BuildRequires
* Sun Oct 20 2013 DH
- Added a new file to %files
- Updated BuildRequires
* Thu Jul 11 2013 DH
- Added two new files to %files
* Fri Mar 01 2013 DH
- Updated for the change to using cmake
* Wed Jan 23 2013 DH
- Additions for wxCrafter
* Wed Aug 29 2012 DH
- Added new binary codelitegcc to %files
* Tue Nov 22 2011 DH
- Add libclang.so to the Requires filter
* Wed May 25 2011 DH
- Add filter for FC15 to remove the codelite-provided lib*.so from 'Requires'!
* Tue Jan 18 2011 DH
- Changes for mimetype stuff
* Fri Dec 24 2010 DH
- Use %find_lang for translations
* Wed Mar 03 2010 DH
- Spec file: Added codelite_xterm
* Thu Sep 24 2009 DH
- Spec file: Added codelite_cppcheck
* Tue Feb 24 2009 DH
- Spec file: Corrected names. Disabled unwanted things in configure
* Tue Feb 24 2009 Jess Portnoy <kernel01@gmail.com> 1.0.2782-1
- Spec file: Added call to desktop-file-install and %doc
  code: fixed perms and other rpmlint issues.
* Sat Feb 21 2009 Jess Portnoy <kernel01@gmail.com> 1.0.2781-1
- Reworked the rpm package to satisfy Fedora Core conventions.
