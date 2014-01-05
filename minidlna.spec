# TODO:
# logrotate
#
Summary:	DLNA server software
Summary(pl.UTF-8):	Oprogramowanie serwerowe DLNA
Name:		minidlna
Version:	1.1.1
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/minidlna/%{name}-%{version}.tar.gz
# Source0-md5:	653405555ac3f8eb4aacc54c1be7b5fa
Source1:	%{name}.init
Source2:	%{name}.service
Source3:	%{name}.tmpfiles
# https://gitorious.org/debian-pkg/minidlna/blobs/raw/master/debian/minidlna.1
Source4:	%{name}.1
# https://gitorious.org/debian-pkg/minidlna/blobs/raw/master/debian/minidlna.conf.5
Source5:	%{name}.conf.5
Patch0:		%{name}-ffmpeg10.patch
Patch1:		config.patch
URL:		http://sourceforge.net/projects/minidlna/
# libavcodec libavformat libavutil
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	gettext-devel
BuildRequires:	libexif-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.5.1
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MiniDLNA (aka ReadyDLNA) is server software with the aim of being
fully compliant with DLNA/UPnP-AV clients.

%description -l pl.UTF-8
MiniDLNA (znane także jako ReadyDLNA) to oprogramowanie serwerowe,
którego celem jest pełna zgodność z klientami DLNA/UPnP-AV.

%prep
%setup -q
#%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man{1,5}} \
	$RPM_BUILD_ROOT{%{systemdtmpfilesdir},%{systemdunitdir}} \
	$RPM_BUILD_ROOT/var/{log,run,cache}/%{name}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}.conf

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# Install man pages
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man5/

for f in po/*.po ; do
	lang=$(basename $f .po)
	install -d $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES
	msgfmt -v -o $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES/minidlna.mo $f
done

%find_lang %{name}

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

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENCE.miniupnpd NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/minidlna
%attr(640,root,minidlna) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/minidlna.conf
%attr(755,root,root) %{_sbindir}/minidlnad
%{systemdtmpfilesdir}/%{name}.conf
%{systemdunitdir}/%{name}.service
%dir %attr(755,minidlna,minidlna) /var/run/%{name}
%dir %attr(755,minidlna,minidlna) /var/cache/%{name}
%dir %attr(755,minidlna,minidlna) /var/log/%{name}
%{_mandir}/man1/*
%{_mandir}/man5/*
