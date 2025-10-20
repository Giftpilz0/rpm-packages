%global commit0 fddb4a09b107237819e661151e007b99b5cab36d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           eww-git
Version:        0.6.0
Release:        %autorelease -s git%{shortcommit0}
Summary:        ElKowars wacky widgets

License:        MIT
URL:            https://github.com/elkowar/eww
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  pkgconfig(dbusmenu-glib-0.4)
BuildRequires:  pkgconfig(dbusmenu-gtk3-0.4)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gtk-layer-shell-0)

Obsoletes:      eww < %{version}-%{release}

%description
Elkowars Wacky Widgets is a standalone widget system made in Rust that
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
