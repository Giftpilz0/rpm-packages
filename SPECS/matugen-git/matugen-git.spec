%global commit0 b969eb7cae79744cbb92e78d40dbcc11dd0f25e9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20251115

Name:           matugen-git
Version:        3.0.0
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
