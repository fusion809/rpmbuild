# Template files in /usr/share/gnome-builder/plugins/autotools_templates/ can't be byte compiled
%global _python_bytecompile_errors_terminate_build 0

%global shortver %(v=%{version}; echo ${v%.*})

Name:    gnome-builder
Version: 3.22.3
Release: 2%{?dist}
Summary: IDE for writing GNOME-based software

# Note: Checked as of 3.20.2
#
# Most of GNOME Builder is licensed under the GPLv3+.
#
# Others are easy to identify
#
# The following files are MIT licensed:
#     - src/resources/css/markdown.css
#     - src/resources/js/marked.js
#
# The following files are licensed under the CC-BY-SA license:
#     - data/icons/
#
# The following files are licensed under the CC0 license:
#     - data/org.gnome.Builder.appdata.xml
#     - data/html-preview.png
License: GPLv3+ and GPLv2+ and LGPLv3+ and LGPLv2+ and MIT and CC-BY-SA and CC0
URL:     https://wiki.gnome.org/Apps/Builder
Source0: https://download.gnome.org/sources/%{name}/%{shortver}/%{name}-%{version}.tar.xz

BuildRequires: vala-devel /usr/bin/vapigen
BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: pkgconfig(flatpak)
BuildRequires: pkgconfig(glibmm-2.4)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(gtkmm-3.0)
BuildRequires: pkgconfig(gtksourceview-3.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(libdevhelp-3.0)
BuildRequires: pkgconfig(libgit2-glib-1.0)
BuildRequires: pkgconfig(libpeas-1.0)
BuildRequires: pkgconfig(mm-common-util)
BuildRequires: pkgconfig(pygobject-3.0) >= 3.19.2
BuildRequires: pkgconfig(sysprof-ui-2)
BuildRequires: pkgconfig(vte-2.91)
BuildRequires: /usr/bin/appstream-util
BuildRequires: llvm-devel >= 3.9.0
BuildRequires: clang-devel
BuildRequires: python3-devel
BuildRequires: gtk-doc
BuildRequires: itstool
Recommends:    python3-jedi

%description
Builder attempts to be an IDE for writing software for GNOME. It does not try
to be a generic IDE, but one specialized for writing GNOME software.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%configure --disable-static
%make_build V=1

%install
%make_install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/org.gnome.Builder.appdata.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Builder.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f gnome-builder.lang
%doc NEWS README
%license COPYING
%{_bindir}/%{name}
%{_bindir}/gnome-builder-cli
%exclude %{_libdir}/%{name}/pkgconfig/
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/
%{_libexecdir}/gnome-builder-worker
%{python3_sitearch}/gi/
# AppData is CC0.
%{_datadir}/appdata/org.gnome.Builder.appdata.xml
%{_datadir}/applications/org.gnome.Builder.desktop
%{_datadir}/dbus-1/services/org.gnome.Builder.service
%{_datadir}/glib-2.0/schemas/org.gnome.builder*.gschema.xml
%exclude %{_datadir}/%{name}/gir-1.0/
%exclude %{_datadir}/%{name}/vapi/
%{_datadir}/%{name}/
%{_datadir}/help/*/%{name}
%{_datadir}/gtksourceview-3.0/styles/builder*.xml
# CC-BY-SA.
%{_datadir}/icons/hicolor/*/apps/org.gnome.Builder.png
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Builder-symbolic.svg

%files devel
%{_libdir}/%{name}/pkgconfig/
%{_datadir}/%{name}/gir-1.0/
%{_datadir}/%{name}/vapi/
%{_datadir}/gtk-doc/html/libide/
%{_includedir}/%{name}-%{version}
%{_includedir}/idemm/

%changelog
* Thu Dec 01 2016 Kalev Lember <klember@redhat.com> - 3.22.3-2
- Enable flatpak support

* Tue Nov 29 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.22.3-1
- Update to 3.22.3

* Wed Nov 02 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 26 2016 Dan Horák <dan[at]danny.cz> - 3.22.0-3
- add missing BR

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 3.22.0-2
- Rebuilt for vala 0.34

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0
- Don't set group tags

* Fri Sep 02 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.21.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Thu Apr 28 2016 Igor Gnatenko <ignatenko@redhat.com> - 3.20.2-1
- Update to 3.20.2

* Thu Mar 24 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.20.0-1
- Update to 3.20.0

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.19.90-3
- Rebuilt for libgit2 0.24.0

* Mon Mar 07 2016 Kalev Lember <klember@redhat.com> - 3.19.90-2
- Rebuilt for vala 0.32

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Fri Feb 19 2016 David King <amigadave@amigadave.com> - 3.19.4-5
- Rebuilt for libclang bump

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Adam Jackson <ajax@redhat.com> 3.19.4-3
- Rebuild for llvm 3.7.1 library split

* Wed Jan 27 2016 David King <amigadave@amigadave.com> - 3.19.4-2
- Fix build against pygobject3

* Wed Jan 27 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.19.4-1
- Update to 3.19.4

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 17 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.18.1-2
- Backport patches from upstream

* Thu Oct 15 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.18.1-1
- Update to 3.18.1

* Wed Sep 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.18.0-2
- Add python3-jedi to Recommends

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Thu Sep 17 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Sat Aug 29 2015 Kalev Lember <klember@redhat.com> - 3.16.3-7
- Backport more fixes for libgit2-glib API changes

* Sat Aug 29 2015 Kalev Lember <klember@redhat.com> - 3.16.3-6
- Drop unneeded uncrustify dependency
- Use make_install macro

* Thu Jul 30 2015 Igor Gnatenko <ignatenko@src.gnome.org> - 3.16.3-5
- Adopt to new API in libgit2-glib (0.23.0)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 13 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.16.3-3
- Remove ineffective local storage crash patch.
- Add patch to increase the max number of files.

* Mon Jun 01 2015 Michael Catanzaro <mcatanzaro@gnome.org> - 3.16.3-2
- Disable HTML5 local storage to avoid a crash.

* Mon May 18 2015  Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.16.3-1
- Update to 3.16.3

* Fri Apr 17 2015 David King <amigadave@amigadave.com> - 3.16.2-2
- Require a recent enough libgit2-glib (#1212804)

* Thu Apr 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Tue Mar 24 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Thu Jan 29 2015 David King <amigadave@amigadave.com> - 3.15.4.1-2
- Add uncrustify Requires

* Fri Jan 23 2015 David King <amigadave@amigadave.com> - 3.15.4.1-1
- Initial packaging (#1185301)
