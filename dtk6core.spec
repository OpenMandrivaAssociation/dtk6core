Name:           dtk6core
Version:        6.0.16
Release:        1
Summary:        Deepin tool kit core modules
License:        LGPL-3.0-or-later
Group:          System/Deepin
URL:            https://github.com/linuxdeepin/dtk6core
Source0:        https://github.com/linuxdeepin/dtk6core/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         https://github.com/linuxdeepin/dtkcore/pull/420.patch

BuildRequires:  cmake

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  cmake(Qt6ToolsTools)
BuildRequires:  cmake(Qt6Concurrent)
#BuildRequires:  qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}

BuildRequires:  cmake(DtkBuildHelper)
BuildRequires:  cmake(spdlog)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(libsystemd)
#BuildRequires:  libasan

%description
Deepin tool kit core modules.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       dtkcommon-devel%{_isa}

%description    devel
This package contains development files for %{name}.

%prep
%autosetup -p1
# comply with dtkcore in Fedora and dtk6core in Arch Linux
sed -i 's|/etc/os-version|/etc/uos-version|' src/dsysinfo.cpp

%build
%cmake \
    -DBUILD_WITH_SYSTEMD=ON \
    -DDTK_VERSION=%{version} \

%cmake_build

%install
%make_install -C build

%files
%license LICENSE
%doc README.md
%{_libdir}/libdtk6core.so.6*
%dir %{_libexecdir}/dtk6
%{_libexecdir}/dtk6/DCore/

%files devel
%{_libdir}/libdtk6core.so
%dir %{_includedir}/dtk6
%{_includedir}/dtk6/DCore/
%{_libdir}/cmake/Dtk6Core/
%{_libdir}/cmake/Dtk6CMake/
%{_libdir}/cmake/Dtk6DConfig/
%{_libdir}/cmake/Dtk6Tools/
%{_libdir}/pkgconfig/dtk6core.pc
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_archdatadir}/mkspecs/features/*.prf

%changelog
%autochangelog
