%global __cargo_is_lib() 0

%global commit0 a2ca2b3c866bc781b12c334a9f949b3db6d7c943
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20251103

Name:           niri-git
Version:        25.08
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Scrollable-tiling Wayland compositor


SourceLicense:        GPL-3.0-or-later
License:              ((MIT OR Apache-2.0) AND BSD-3-Clause) AND ((MIT OR Apache-2.0) AND Unicode-3.0) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 AND MIT) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 OR MIT OR Unlicense) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-3-Clause OR MIT OR Apache-2.0) AND (GPL-3.0-or-later) AND (ISC) AND (MIT) AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND (MPL-2.0) AND (Unicode-3.0) AND (Unlicense OR MIT) AND (Zlib) AND (Zlib OR Apache-2.0 OR MIT)
URL:            https://github.com/YaLTeR/niri
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pipewire-devel
BuildRequires:  pango-devel
BuildRequires:  cairo-gobject-devel
# Needed for pipewire-rs
BuildRequires:  clang
# Needed for some tests with a surfaceless EGL renderer
BuildRequires:  mesa-libEGL

Requires:       mesa-dri-drivers
Requires:       mesa-libEGL

# Portal implementations used by niri
Recommends:     xdg-desktop-portal-gtk
Recommends:     xdg-desktop-portal-gnome
Recommends:     gnome-keyring

# Obsoletes
Obsoletes:      niri < %{version}-%{release}

%description
A scrollable-tiling Wayland compositor.

Windows are arranged in columns on an infinite strip going to the right.
Opening a new window never causes existing windows to resize.

%prep
%autosetup -n niri-%{commit0}
cargo vendor

# We use vendored sources, but they still need a version rather than a git link in Cargo.toml
sed -i 's/^git = "https:\/\/github.com\/Smithay\/smithay.git"$/version = "*"/' Cargo.toml
sed -i 's/git = "https:\/\/gitlab.freedesktop.org\/pipewire\/pipewire-rs.git"/version = "*"/' Cargo.toml

%cargo_prep -v vendor

# Set the build version string.
sed -i 's/\[env\]/[env]\nNIRI_BUILD_VERSION_STRING="%{version} (%{shortcommit0})"/' .cargo/config.toml

%build
%cargo_build

%{cargo_license_summary}
%{cargo_license} > LICENSE.dependencies
%{cargo_vendor_manifest}

%install
%cargo_install

install -Dm755 -t %{buildroot}%{_bindir} ./resources/niri-session
install -Dm644 -t %{buildroot}%{_datadir}/wayland-sessions ./resources/niri.desktop
install -Dm644 -t %{buildroot}%{_datadir}/xdg-desktop-portal ./resources/niri-portals.conf
install -Dm644 -t %{buildroot}%{_userunitdir} ./resources/niri.service
install -Dm644 -t %{buildroot}%{_userunitdir} ./resources/niri-shutdown.target

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%doc resources/default-config.kdl
%doc docs/wiki
%{_bindir}/niri
%{_bindir}/niri-session
%{_datadir}/wayland-sessions/niri.desktop
%dir %{_datadir}/xdg-desktop-portal
%{_datadir}/xdg-desktop-portal/niri-portals.conf
%{_userunitdir}/niri.service
%{_userunitdir}/niri-shutdown.target

%changelog
%autochangelog
