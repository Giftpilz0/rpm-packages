%global commit0 e9c182a13c1d12762351ec01ce0ec711d41b0337
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20260420

Name:           niri-git
Version:        25.11
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Scrollable-tiling Wayland compositor

License:        ((MIT OR Apache-2.0) AND BSD-3-Clause) AND ((MIT OR Apache-2.0) AND Unicode-3.0) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0) AND (Apache-2.0 AND MIT) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR MIT) AND (Apache-2.0 OR MIT OR Unlicense) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND (BSD-3-Clause OR MIT OR Apache-2.0) AND (GPL-3.0-or-later) AND (ISC) AND (MIT) AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND (MPL-2.0) AND (Unicode-3.0) AND (Unlicense OR MIT) AND (Zlib) AND (Zlib OR Apache-2.0 OR MIT)
URL:            https://github.com/niri-wm/niri
Source0:        %{url}/archive/%{commit0}/niri-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  cairo-gobject-devel
BuildRequires:  clang
BuildRequires:  mesa-libEGL
BuildRequires:  pango-devel
BuildRequires:  pipewire-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  wayland-devel

Requires:       libwayland-server
Requires:       mesa-dri-drivers
Requires:       mesa-libEGL

Recommends:     gnome-keyring
Recommends:     xdg-desktop-portal-gnome
Recommends:     xdg-desktop-portal-gtk

Obsoletes:      niri < %{version}-%{release}

%description
A scrollable-tiling Wayland compositor.

Windows are arranged in columns on an infinite strip going to the right.
Opening a new window never causes existing windows to resize.

%prep
%autosetup -n niri-%{commit0}
cargo vendor

# Replace upstream git dependencies so cargo can use the vendored sources.
sed -i 's/^git = "https:\/\/github.com\/Smithay\/smithay.git"$/version = "*"/' Cargo.toml
sed -i 's/git = "https:\/\/gitlab.freedesktop.org\/pipewire\/pipewire-rs.git"/version = "*"/' Cargo.toml

%cargo_prep -v vendor
sed -i 's/\[env\]/[env]\nNIRI_BUILD_VERSION_STRING="%{version} (%{shortcommit0})"/' .cargo/config.toml

%build
%cargo_build

target/rpm/niri completions bash > ./niri
target/rpm/niri completions fish > ./niri.fish
target/rpm/niri completions zsh > ./_niri

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

install -Dm644 -t %{buildroot}%{bash_completions_dir} ./niri
install -Dm644 -t %{buildroot}%{fish_completions_dir} ./niri.fish
install -Dm644 -t %{buildroot}%{zsh_completions_dir} ./_niri

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

%{bash_completions_dir}/niri
%{fish_completions_dir}/niri.fish
%{zsh_completions_dir}/_niri

%changelog
%autochangelog
