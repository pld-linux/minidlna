Summary:	DLNA server software
Summary(pl.UTF-8):	DLNA server software
Name:		minidlna
Version:	1.0.22
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/minidlna/%{name}_%{version}_src.tar.gz
# Source0-md5:	3de2f6b54f43bb998dfad3c8fa75cef3
Source1:	%{name}.init
URL:		http://sourceforge.net/projects/minidlna/
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	libdlna-devel >= 0.2.1
BuildRequires:	libexif-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sqlite3-devel
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being
fully compliant with DLNA/UPnP-AV clients.

%description -l pl.UTF-8
MiniDLNA (aka ReadyDLNA) is server software with the aim of being
fully compliant with DLNA/UPnP-AV clients.

%prep
%setup -q
sed -i -e 's#-O3#$(OPTFLAGS)#g' Makefile

%build
%{__make} \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
        %service -q %{name} stop
        /sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/minidlna
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/minidlna.conf
%attr(755,root,root) %{_sbindir}/minidlna
