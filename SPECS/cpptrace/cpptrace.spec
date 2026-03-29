Name:           cpptrace
Version:        1.0.4
Release:        %autorelease
Summary:        Simple, portable, and drop-in C++ stacktrace library

License:        MIT
URL:            https://github.com/jeremy-rifkin/cpptrace
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  libdwarf-devel
BuildRequires:  libunwind-devel
BuildRequires:  ninja-build
BuildRequires:  pkgconf

%description
cpptrace is an easy to use C++ stacktrace library providing a
straightforward unified interface for stack traces in C++.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%ldconfig_scriptlets

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DBUILD_SHARED_LIBS=ON \
       -DCPPTRACE_USE_EXTERNAL_LIBDWARF=ON \
       -DCPPTRACE_FIND_LIBDWARF_WITH_PKGCONFIG=ON \
       -DCPPTRACE_GET_SYMBOLS_WITH_LIBDWARF=ON \
       -DCPPTRACE_UNWIND_WITH_LIBUNWIND=ON
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_libdir}/libcpptrace.so.*

%files devel
%{_includedir}/cpptrace/
%{_includedir}/ctrace/
%{_libdir}/libcpptrace.so
%{_libdir}/cmake/cpptrace/

%changelog
%autochangelog
