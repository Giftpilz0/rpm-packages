%global commit0 865cf631d5bbb5f9fccc99b3f4cc80b9eeada18c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20260305

Name:           eww-git
Version:        0.6.0
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Widget daemon for configurable desktop widgets

License:        MIT
URL:            https://github.com/elkowar/eww
Source0:        %{url}/archive/%{commit0}/eww-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)

Obsoletes:      eww < %{version}-%{release}

%description
ElKowar's Wacky Widgets is a standalone widget system made in Rust that
allows you to implement your own, custom widgets in any window manager.

%prep
%autosetup -n eww-%{commit0}
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build

%install
install -Dm755 target/release/eww -t %{buildroot}%{_bindir}

%files
%license LICENSE
%doc examples/ README.md
%{_bindir}/eww

%changelog
%autochangelog
