%global commit0 e85a6c9ac4efe2362afb6358f8d2f05556a1d1f1
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           matugen-git
Version:        2.4.1
Release:        %autorelease -s git%{shortcommit0}
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
