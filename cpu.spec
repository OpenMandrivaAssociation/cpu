%define	name	cpu
%define version 1.4.3
%define release %mkrel 6

%define	lib_name_orig lib%{name}

%define	lib_major 0
%define	libname %mklibname %name %lib_major
%define	libnamedev %mklibname %name %lib_major -d

# (misc) disabled as plugins do not link otherwise
%define _disable_ld_no_undefined 1


Summary:	Ldap aware command like useradd, userdel, usermod and others
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://prdownloads.sourceforge.net/cpu/cpu-%version.tar.bz2
# first hunk taken from the debian unstable package,
# author is Guido Trotter <ultrotter@debian.org>
Patch:		cpu-1.4.3-gcc4.patch
Patch1:     cpu-1.4.3-fix_open_usage.diff
Patch2:     cpu-1.4.3-fix_makefile.diff
License:	GPLv2+
Url:		http://cpu.sourceforge.net
Group:		System/Base
BuildRequires:	openldap-devel
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
Provides:	lib%{name}-devel %{name}-devel

%description -n %libnamedev
CPU is an LDAP user management tool written in C and loosely based
on FreeBSD's pw(8). The goal of CPU is to be a suitable replacement
of the useradd/usermod/userdel utilities for administrators using an
LDAP backend and wishing to have a suite of command line tools for
doing the administration.

%prep
%setup -q
%patch -p1 -b .gcc4
%patch1 -p0
%patch2 -p0

%build
# for patch 2
aclocal && autoconf && automake
%configure
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
%config(noreplace) %{_sysconfdir}/cpu.conf

%files -n %libname
%defattr(-, root, root)
%_libdir/*.so.*

%files -n %libnamedev
%defattr(-, root, root)
%{_libdir}/*.so
%_libdir/*.*a

