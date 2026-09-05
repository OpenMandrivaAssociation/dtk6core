%define libname %mklibname dtk6core
%define devname %mklibname -d dtk6core

Name:           dtk6core
Version:        6.0.16
Release:        3
Summary:        Deepin tool kit core modules
License:        LGPL-3.0-or-later
Group:          System/Deepin
URL:            https://github.com/linuxdeepin/dtk6core
Source0:        https://github.com/linuxdeepin/dtk6core/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         https://github.com/linuxdeepin/dtkcore/pull/420.patch
# Qt 6.8–6.11 QAbstractFileEngine API (create unique_ptr, advance, TriStateResult)
Patch1:         dtk6core-qt-6.11-fileengine.patch
# QObjectPrivate no longer takes int; QFile no longer converts from QString
Patch2:         dtk6core-qt-6.11-log.patch

BuildRequires:  cmake
BuildRequires:  ninja

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6CorePrivate)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6DBusPrivate)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  cmake(Qt6ToolsTools)
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(DtkBuildHelper)
BuildRequires:  cmake(spdlog)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(libsystemd)
#BuildRequires:  libasan

%description
Deepin tool kit core modules.

%package -n %{libname}
Summary:        Shared library for %{name}

%description -n %{libname}
Libs for deepin tool kit core modules.

%package -n %{devname}
Summary:        Development files for %{name}
Requires:	%{libname} = %{EVRD}
Requires:       cmake(Dtk6)
Provides:       dtk6core-devel = %{EVRD}

%description -n %{devname}
This package contains development files for %{name}.

%prep
%autosetup -p1
# comply with dtkcore in Fedora and dtk6core in Arch Linux
sed -i 's|/etc/os-version|/etc/uos-version|' src/dsysinfo.cpp
# Qt 6.11 no longer creates Qt6::CorePrivate from COMPONENTS Core
sed -i \
	-e 's/COMPONENTS Core)/COMPONENTS Core CorePrivate)/' \
	-e 's/COMPONENTS DBus)/COMPONENTS DBus DBusPrivate)/' \
	src/CMakeLists.txt tools/*/CMakeLists.txt

%build
%cmake \
    -DBUILD_WITH_SYSTEMD=ON \
    -DDTK_VERSION=%{version} \
    -G Ninja

%ninja_build

%install
%ninja_install -C build

%files -n %{libname}
%license LICENSE
%doc README.md
%{_libdir}/libdtk6core.so.6*
%dir %{_libexecdir}/dtk6
%{_libexecdir}/dtk6/DCore/

%files -n %{devname}
%{_libdir}/libdtk6core.so
%dir %{_includedir}/dtk6
%{_includedir}/dtk6/DCore/
%{_libdir}/cmake/Dtk6Core/
%{_libdir}/cmake/Dtk6CMake/
%{_libdir}/cmake/Dtk6DConfig/
%{_libdir}/cmake/Dtk6Tools/
%{_libdir}/pkgconfig/dtk6core.pc
%{_libdir}/qt6/mkspecs/features/dtk_install_dconfig.prf
%{_libdir}/qt6/mkspecs/modules/qt_lib_dtkcore.pri
