#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Attansic(R) L2 Fast Ethernet Adapter driver for Linux
Summary(pl.UTF-8):	Sterownik do kart Attansic(R) L2 Fast Ethernet Adapter
Name:		kernel%{_alt_kernel}-net-atl2
Version:	2.0.4
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://people.redhat.com/csnook/atl2/atl2-%{version}.tar.bz2
# Source0-md5:	22b22dc9d45b85549b002cf152c8ac27
URL:		http://www.attansic.com/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains the Linux driver for the Attansic(R) L2 Fast
Ethernet Adapter.

%description -l pl.UTF-8
Ten pakiet zawiera sterownik dla Linuksa do kart sieciowych
Attansic(R) L2 Fast Ethernet Adapter.

%prep
%setup -q -n atl2-%{version}

%build
%build_kernel_modules -m atl2 EXTRA_CFLAGS="-DDBG=0"

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m atl2 -d kernel/drivers/net

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/atl2*.ko*
