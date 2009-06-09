%define	name	cpu
%define version 1.4.3
%define release %mkrel 9

%define	lib_major 0
%define	libname %mklibname %name %lib_major
%define	libnamedev %mklibname %name -d

Summary:	Ldap aware command like useradd, userdel, usermod and others
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/cpu/cpu-%version.tar.bz2
# first hunk taken from the debian unstable package,
# author is Guido Trotter <ultrotter@debian.org>
Patch0:		cpu-1.4.3-gcc4.patch
Patch1: 	cpu-1.4.3-fix_open_usage.diff
Patch2:		cpu-1.4.3-fix_makefile.diff
Patch3:		cpu-1.4.3-linkage.patch
License:	GPLv2+
Url:		http://cpu.sourceforge.net
Group:		System/Base
BuildRequires:	openldap-devel
Conflicts:	%{_lib}cpu0-devel < 1.4.3-8
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
CPU is an LDAP user management tool written in C and loosely based
on FreeBSD's pw(8). The goal of CPU is to be a suitable replacement
of the useradd/usermod/userdel utilities for administrators using an
LDAP backend and wishing to have a suite of command line tools for
doing the administration.

%package -n %libname

Summary:	Ldap aware command like useradd, userdel, usermod and others
Group:		System/Base

%description -n %libname
CPU is an LDAP user management tool written in C and loosely based
on FreeBSD's pw(8). The goal of CPU is to be a suitable replacement
of the useradd/usermod/userdel utilities for administrators using an
LDAP backend and wishing to have a suite of command line tools for
doing the administration.

%package -n %libnamedev

Summary:	Ldap aware command like useradd, userdel, usermod and others
Group:		System/Base
Requires:	%libname = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}cpu0-devel < 1.4.3-8

%description -n %libnamedev
CPU is an LDAP user management tool written in C and loosely based
on FreeBSD's pw(8). The goal of CPU is to be a suitable replacement
of the useradd/usermod/userdel utilities for administrators using an
LDAP backend and wishing to have a suite of command line tools for
doing the administration.

%prep
%setup -q
%patch0 -p1 -b .gcc4
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
autoreconf -fi
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

rm -f $RPM_BUILD_ROOT%{_datadir}/{cpu.conf.doc,test.ldif}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS COPYING INSTALL NEWS README doc/cpu.conf.doc
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_sbindir}/cpu
%{_libdir}/libcpu_ldap.so
%config(noreplace) %{_sysconfdir}/cpu.conf

%files -n %libname
%defattr(-, root, root)
%_libdir/*.so.%{lib_major}*

%files -n %libnamedev
%defattr(-, root, root)
%{_libdir}/libcputil.so
%_libdir/*.*a

