%global commit0 b4046140b4253934568bf0289673ec5efeb2a5c9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate 20251112

Name:           yolk-git
Version:        0.3.6
Release:        %autorelease -s %{commitdate}git%{shortcommit0}
Summary:        Yolk

License:        MIT
URL:            https://github.com/elkowar/yolk
Source0:        %{url}/archive/%{commit0}/yolk-%{shortcommit0}.tar.gz

BuildRequires:  cargo-rpm-macros

Obsoletes:      yolk < %{version}-%{release}

%description
Yolk is a cross platform dotfile management tool with a unique spin on templating,
sitting somewhere in between GNU Stow and chezmoi.

%prep
%autosetup -n yolk-%{commit0}
cargo vendor
%cargo_prep -v vendor

%build
%cargo_build

%install
install -Dm755 target/release/yolk -t %{buildroot}%{_bindir}

%files
%license LICENSE.md
%doc docs/ README.md
%{_bindir}/yolk

%changelog
%autochangelog
