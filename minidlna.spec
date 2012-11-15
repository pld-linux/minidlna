Summary:	DLNA server software
Summary(pl.UTF-8):	Oprogramowanie serwerowe DLNA
Name:		minidlna
Version:	1.0.25
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://downloads.sourceforge.net/minidlna/%{name}_%{version}_src.tar.gz
# Source0-md5:	d966256baf2f9b068b9de871ab5dade5
Source1:	%{name}.init
# https://gitorious.org/debian-pkg/minidlna/blobs/raw/master/debian/minidlna.1
Source4:	%{name}.1
# https://gitorious.org/debian-pkg/minidlna/blobs/raw/master/debian/minidlna.conf.5
Source5:	%{name}.conf.5
Patch0:		%{name}-ffmpeg10.patch
URL:		http://sourceforge.net/projects/minidlna/
# libavcodec libavformat libavutil
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	gettext-devel
BuildRequires:	libdlna-devel >= 0.2.1
BuildRequires:	libexif-devel
BuildRequires:	libid3tag-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
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
%patch0 -p1

%{__sed} -i -e 's#-g -O3#$(OPTFLAGS)#g' Makefile

# Verbose Makefile
sed -i 's/@$(CC)/$(CC)/' Makefile

%build
%{__make} -j1 \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} %{rpmcppflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_mandir}/man{1,5}}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 install-conf \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

# Install man pages
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man5/

for f in po/*.po ; do
	lang=$(basename $f .po)
	install -d $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES
	msgfmt -v -o $RPM_BUILD_ROOT%{_localedir}/${lang}/LC_MESSAGES/minidlna.mo $f
done

%find_lang %{name}

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

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENCE.miniupnpd NEWS README TODO
%attr(754,root,root) /etc/rc.d/init.d/minidlna
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/minidlna.conf
%attr(755,root,root) %{_sbindir}/minidlna
%{_mandir}/man1/*
%{_mandir}/man5/*
