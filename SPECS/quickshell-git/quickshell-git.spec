%global commit0 055e384668d38987a0054169e4feb43645d9735b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20260426

Name:           quickshell-git
Version:        0.2.1
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Flexible QtQuick based desktop shell toolkit

License:        LGPL-3.0-only AND GPL-3.0-only
URL:            https://github.com/quickshell-mirror/quickshell
Source0:        %{url}/archive/%{commit0}/quickshell-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  cpptrace-devel
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(CLI11)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(jemalloc)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(pam)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Qml)
BuildRequires:  pkgconfig(Qt6ShaderTools)
BuildRequires:  pkgconfig(Qt6WaylandClient)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  spirv-tools

Obsoletes:      quickshell < %{version}-%{release}

%description
Flexible toolkit for making desktop shells with QtQuick, targeting
Wayland and X11 compositors.

%prep
%autosetup -n quickshell-%{commit0} -p1

%build
%cmake -GNinja \
       -DBUILD_SHARED_LIBS=OFF \
       -DDISTRIBUTOR="Fedora COPR" \
       -DGIT_REVISION=%{commit0} \
       -DINSTALL_QMLDIR=%{_libdir}/qt6/qml
%cmake_build

%install
%cmake_install

%files
%license LICENSE LICENSE-GPL
%doc BUILD.md CONTRIBUTING.md README.md
%doc changelog/v%{version}.md
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_libdir}/qt6/qml/Quickshell

%changelog
%autochangelog
