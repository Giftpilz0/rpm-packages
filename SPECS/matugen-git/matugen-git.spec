%global __brp_mangle_shebangs_exclude_from ^/usr/src/debug/.*\.rs$

%global commit0 3a3fb9c710b1ad67df500dfd2ba5b12dea281d9d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20260322

Name:           matugen-git
Version:        4.1.0
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        matugen

License:        GPL-2.0-only
URL:            https://github.com/InioX/matugen
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros

Obsoletes:      matugen < %{version}-%{release}

%description
A material you color generation tool with templates

%prep
%autosetup -n matugen-%{commit0}
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build

%install
install -Dm755 target/release/matugen -t %{buildroot}%{_bindir}

%files
%license LICENSE
%doc CHANGELOG.md README.md
%{_bindir}/matugen

%changelog
%autochangelog
