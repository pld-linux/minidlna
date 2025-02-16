# TODO:
# logrotate
#
Summary:	DLNA server software
Summary(pl.UTF-8):	Oprogramowanie serwerowe DLNA
Name:		minidlna
Version:	1.3.3
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/minidlna/%{name}-%{version}.tar.gz
# Source0-md5:	a8b010d8803811f4e26e57894c30fa6c
Source1:	%{name}.init
Source2:	%{name}.service
Source3:	%{name}.tmpfiles
Patch0:		config.patch
URL:		http://sourceforge.net/projects/minidlna/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
# libavcodec libavformat libavutil
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	gettext-tools >= 0.18
BuildRequires:	libexif-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.5.1
Requires(post,preun):	/sbin/chkconfig
Provides:	group(minidlna)
Provides:	user(minidlna)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being
fully compliant with DLNA/UPnP-AV clients.

%description -l pl.UTF-8
MiniDLNA (znane także jako ReadyDLNA) to oprogramowanie serwerowe,
którego celem jest pełna zgodność z klientami DLNA/UPnP-AV.

%prep
%setup -q
%patch -P0 -p1

%build
%{__gettextize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
export CFLAGS="%{rpmcflags} -fcommon"
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}} \
	$RPM_BUILD_ROOT/var/{log,run,cache}/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# not installed by make install: config file
cp -p %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf
# and man pages
cp -p *.5 $RPM_BUILD_ROOT%{_mandir}/man5
cp -p *.8 $RPM_BUILD_ROOT%{_mandir}/man8

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 284 minidlna
%useradd -u 284 -r -d / -s /bin/false -g minidlna minidlna

%post
/sbin/chkconfig --add %{name}
%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun
if [ "$1" = "0" ]; then
	%userremove minidlna
	%groupremove minidlna
fi
%systemd_reload

%triggerpostun -- %{name} < 1.0.25-3
%systemd_trigger %{name}.service

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS LICENCE.miniupnpd NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/minidlna
%attr(640,root,minidlna) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/minidlna.conf
%attr(755,root,root) %{_sbindir}/minidlnad
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/%{name}.service
%dir %attr(755,minidlna,minidlna) /var/run/%{name}
%dir %attr(755,minidlna,minidlna) /var/cache/%{name}
%dir %attr(755,minidlna,minidlna) /var/log/%{name}
%{_mandir}/man5/minidlna.conf.5*
%{_mandir}/man8/minidlnad.8*
