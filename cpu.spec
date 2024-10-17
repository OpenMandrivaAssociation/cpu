%define	name	cpu
%define version 1.4.3
%define release 11

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
Url:		https://cpu.sourceforge.net
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



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.4.3-10mdv2011.0
+ Revision: 617436
- the mass rebuild of 2010.0 packages

* Tue Jun 09 2009 Funda Wang <fwang@mandriva.org> 1.4.3-9mdv2010.0
+ Revision: 384205
- fix provides

* Tue Jun 09 2009 Funda Wang <fwang@mandriva.org> 1.4.3-8mdv2010.0
+ Revision: 384166
- fix module build
- move module into main package

* Tue Jul 08 2008 Michael Scherer <misc@mandriva.org> 1.4.3-7mdv2009.0
+ Revision: 232696
- bunzip patch
- fix license
- fix build, by using _disable_ld_no_undefined ( as plugins do not build without it )
  and by patching their makefile ( seems that LBFLAGS was not expanded in Makefile.am )
- fix build

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 1.4.3-6mdv2008.1
+ Revision: 123432
- kill re-definition of %%buildroot on Pixel's request
- import cpu


* Fri Nov 18 2005 Thierry Vignaud <tvignaud@mandriva.com> 1.4.3-6mdk
- rebuild against openssl-0.9.8

* Wed Sep 07 2005 Andreas Hasenack <andreas@mandriva.com> 1.4.3-5mdk
- added patch to build with gcc4 (first hunk taken from the 
  debian unstable package)
- rebuilt with openldap-2.3.x

* Tue Feb 08 2005 Buchan Milne <bgmilne@linux-mandrake.com> 1.4.3-4mdk
- rebuild for ldap2.2_7

* Fri Feb  4 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 1.4.3-3mdk
- rebuilt against new openldap libs

* Wed Jan 14 2004 Franck Villaume <fvill@freesurf.fr> 1.4.3-2mdk
- BuildRequires : openldap-devel

* Mon Jan 12 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.4.3-1mdk
- 1.4.3

* Fri Dec 12 2003 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.4.2-1mdk
- 1.4.2
- do not rm -rf $RPM_BUILD_ROOT in %%prep
- no explicit library dependencies
- add missing files to %%files
- fix devel provides
- fix devel requires

* Thu Apr 03 2003 Lenny Cartier <lenny@mandrakesoft.com 1.3.99a-1mdk
- 1.3.99a

* Sat Feb 01 2003 Lenny Cartier <lenny@mandrakesoft.com 1.3.12-2mdk
- rebuild

* Thu Aug 22 2002 Lenny Cartier <lenny@mandrakesoft.com> 1.3.12-1mdk
- from Franck Martin <franck@sopac.org> :
	- first release for mdk8.2
