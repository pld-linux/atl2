#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	1
Summary:	Attansic(R) L2 Fast Ethernet Adapter driver for Linux
Summary(pl.UTF-8):	Sterownik do kart Attansic(R) L2 Fast Ethernet Adapter
Name:		kernel%{_alt_kernel}-net-atl2
Version:	1.4.0.20
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL v2
Group:		Base/Kernel
Source0:	http://starowa.one.pl/~uzi/pld/atl2-%{version}.tar.gz
# Source0-md5:	196771fa8e7164d4c9beabcfdf4058b5
Patch0:		kernel-net-atl2-build.patch
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
%patch0 -p0

cat > src/Makefile <<'EOF'
obj-m := atl2.o
atl2-objs := at_main.o at_hw.o at_param.o at_ethtool.o kcompat.o
EOF

%build
%build_kernel_modules -C src -m atl2

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m src/atl2 -d kernel/drivers/net

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%doc atl2.7 COPYING readme release_note.txt ldistrib.txt
#/etc/modprobe.d/%{_kernel_ver}/atl2.conf
/lib/modules/%{_kernel_ver}/kernel/drivers/net/atl2*.ko*
