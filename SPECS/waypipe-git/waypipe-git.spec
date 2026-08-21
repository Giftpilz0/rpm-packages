%global commit0 5fc8a456f14499052a4888a25719c462a4cd1b9a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20260819

Name:           waypipe-git
Version:        0.11.1
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Wayland application forwarding proxy

License:        GPL-3.0-or-later
URL:            https://gitlab.freedesktop.org/mstoeckl/waypipe
Source0:        %{url}/-/archive/%{commit0}/waypipe-%{commit0}.tar.gz

BuildRequires:  bindgen
BuildRequires:  cargo
BuildRequires:  cargo-rpm-macros
BuildRequires:  clang
BuildRequires:  glslc
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  rust
BuildRequires:  scdoc

Requires:       openssh

Obsoletes:      waypipe < %{version}-%{release}

%description
Waypipe is a proxy for Wayland clients. It forwards Wayland messages and
serializes changes to shared memory buffers over a single socket. This makes
application forwarding similar to "ssh -X" feasible.

%prep
%autosetup -n waypipe-%{commit0}
cargo vendor
%cargo_prep -v vendor

%build
%meson \
    -Dman-pages=enabled \
    -Dtests=false \
    -Dwith_dmabuf=enabled \
    -Dwith_gbm=enabled \
    -Dwith_lz4=enabled \
    -Dwith_video=enabled \
    -Dwith_zstd=enabled

%meson_build

%install
%meson_install

%files
%license LICENSE.MIT LICENSE.GPLv3
%doc README.md
%{_bindir}/waypipe
%{_mandir}/man1/waypipe.1*

%changelog
%autochangelog
