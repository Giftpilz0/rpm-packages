%global commit0 8b5668b8c3187af8a2d21731e9db2be97be5c3dc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20251104

Name:           waypipe-git
Version:        0.10.5
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        waypipe

License:        MIT
URL:            https://gitlab.freedesktop.org/mstoeckl/waypipe
Source0:        %{url}/-/archive/%{commit0}/waypipe-%{commit0}.tar.gz

# Core build requirements
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  pkgconfig
BuildRequires:  clang
BuildRequires:  bindgen

# Documentation
BuildRequires:  scdoc

# Optional feature dependencies
BuildRequires:  pkgconfig(liblz4)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  glslc

# Runtime requirements
Requires:       openssh

# Obsoletes
Obsoletes:      waypipe < %{version}-%{release}

%description
Waypipe is a proxy for Wayland clients. It forwards Wayland messages and
serializes changes to shared memory buffers over a single socket. This makes
application forwarding similar to "ssh -X" feasible.

%prep
%autosetup -n waypipe-%{commit0}

# Fetch Rust dependencies
cargo fetch --locked

%build
%meson \
    -Dwith_lz4=enabled \
    -Dwith_zstd=enabled \
    -Dwith_dmabuf=enabled \
    -Dwith_video=enabled

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
