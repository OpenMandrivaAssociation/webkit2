%define debug_package %{nil}

%define oname webkitgtk

%define api 4.0

%define javascriptcoregtk_major 18
%define libjavascriptcoregtk %mklibname javascriptcoregtk %{api} %{javascriptcoregtk_major}
%define javascriptcoregtk_gir %mklibname javascriptcore-gir %{api}

%define webkit2_major 37
%define libwebkit2 %mklibname webkit2gtk %{api} %{webkit2_major}
%define webkit2_gir %mklibname webkit2gtk-gir %{api}

%define develname %mklibname -d webkit2

Summary:	Web browser engine
Name:		webkit2
Version:	2.8.3
Release:	2
License:	BSD and LGPLv2+
Group:		System/Libraries
Source0:	http://webkitgtk.org/releases/%{oname}-%{version}.tar.xz
Patch0:		webkitgtk-typelib-sharelib-link.patch
# our cairo is not built with egl so build fails without this
Patch1:		webkitgtk-2.6.1-disable_egl.patch
URL:		http://www.webkitgtk.org
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	curl-devel >= 7.11.0
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	gperf
BuildRequires:	icu-devel
BuildRequires:	jpeg-devel
BuildRequires:	png-devel
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	librsvg-devel >= 2.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	libsoup-devel >= 2.42.0
BuildRequires:	libtool
BuildRequires:	libxslt-devel
BuildRequires:	libxt-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	gtk+3-devel
BuildRequires:	libgail-3.0-devel
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	sqlite3-devel
BuildRequires:	pkgconfig(xft)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	libgnome-keyring-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	enchant-devel
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(geoclue-2.0)
BuildRequires:	gail-devel
BuildRequires:	ruby
BuildRequires:	cmake >= 2.8.8
Requires:	%{libwebkit2} = %{version}

%description
WebKit is an open source web browser engine.

%package	jsc
Summary:	JavaScriptCore shell for WebKit GTK+
Group:		Development/GNOME and GTK+

%description	jsc
jsc is a shell for JavaScriptCore, WebKit's JavaScript engine. It
allows you to interact with the JavaScript engine directly.

%package -n	%{libwebkit2}
Summary:	GTK+ port of WebKit web browser engine
Group:		System/Libraries
Requires:	%{name} = %{version}

%description -n	%{libwebkit2}
The GTK+ port of WebKit is intended to provide a browser component
primarily for users of the portable GTK+ UI toolkit on platforms like
Linux.

%package -n	%{libjavascriptcoregtk}
Summary:        GTK+ port of WebKit web browser engine
Group:          System/Libraries

%description -n	%{libjavascriptcoregtk}
The GTK+ port of WebKit is intended to provide a browser component
primarily for users of the portable GTK+ UI toolkit on platforms like
Linux.

%package -n	%{develname}
Summary:	Development files for WebKit GTK+ port
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libwebkit2gtk-devel = %{version}-%{release}
Requires:	%{libjavascriptcoregtk} = %{version}
Requires:	%{libwebkit2} = %{version}
Requires:	%{javascriptcoregtk_gir} = %{version}
Requires:	%{webkit2_gir} = %{version}

%description -n	%{develname}
The GTK+ port of WebKit is intended to provide a browser component
primarily for users of the portable GTK+ UI toolkit on platforms like
Linux. This package contains development headers.

%package -n	%{javascriptcoregtk_gir}
Summary:        GObject Introspection interface description for JSCore
Group:          System/Libraries
Requires:       %{libjavascriptcoregtk} = %{version}-%{release}

%description -n	%{javascriptcoregtk_gir}
GObject Introspection interface description for JSCore.

%package -n	%{webkit2_gir}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libwebkit2} = %{version}-%{release}

%description -n	%{webkit2_gir}
GObject Introspection interface description for WebKit.

%prep
%setup -qn %{oname}-%{version}
%apply_patches

%build
# (tpg) do not build debug code
%global optflags %(echo %{optflags} | sed -e 's/-g /-g0 /' -e 's/-gdwarf-4//')

%ifarch %arm %ix86
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
%cmake -DPORT=GTK -DLIB_INSTALL_DIR:PATH=%{_libdir}
%make

%install
%makeinstall_std -C build

%find_lang WebKit2GTK-%{api}

%files -f WebKit2GTK-%{api}.lang
%dir %{_libexecdir}/webkit2gtk-%{api}
%{_libexecdir}/webkit2gtk-%{api}/*
%dir %{_libdir}/webkit2gtk-%{api}
%dir %{_libdir}/webkit2gtk-%{api}/injected-bundle
%{_libdir}/webkit2gtk-%{api}/injected-bundle/libwebkit2gtkinjectedbundle.so

%files jsc
%{_bindir}/jsc

%files -n %{libjavascriptcoregtk}
%{_libdir}/libjavascriptcoregtk-%{api}.so.%{javascriptcoregtk_major}
%{_libdir}/libjavascriptcoregtk-%{api}.so.%{javascriptcoregtk_major}.*

%files -n %{libwebkit2}
%{_libdir}/libwebkit2gtk-%{api}.so.%{webkit2_major}
%{_libdir}/libwebkit2gtk-%{api}.so.%{webkit2_major}.*

%files -n %{develname}
%{_includedir}/webkitgtk-%{api}
%{_libdir}/*-%{api}.so
%{_libdir}/pkgconfig/*-%{api}.pc
%{_datadir}/gir-1.0/*-%{api}.gir

%files -n %{javascriptcoregtk_gir}
%{_libdir}/girepository-1.0/JavaScriptCore-%{api}.typelib

%files -n %{webkit2_gir}
%{_libdir}/girepository-1.0/WebKit2-%{api}.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-%{api}.typelib

