%define		_modname		mmcache
%define		_pkgname	turck-mmcache
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	Turck MMCache extension module for PHP
Summary(pl.UTF-8):	Moduł Turck MMCache dla PHP
Name:		php4-%{_modname}
Version:	2.4.6
Release:	9
License:	GPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/%{_pkgname}/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	bcf671bec2e8b009e9b2d8f8d2574041
Patch0:		%{name}-debian-8.patch
URL:		http://turck-mmcache.sourceforge.net
BuildRequires:	php4-devel >= 3:4.1
BuildRequires:	rpmbuild(macros) >= 1.322
%{?requires_php_extension}
%{?requires_zend_extension}
Requires:	%{_sysconfdir}/conf.d
Requires:	php(zlib)
Requires:	webserver = apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Turck MMCache is a PHP Accelerator & Encoder. It increases performance
of PHP scripts by caching them in compiled state, so that the overhead
of compiling is almost completely eliminated. Also it uses some
optimizations for speed up of scripts execution.

More information can be find at %{url}.

%description -l pl.UTF-8
Turck MMCache jest akceleratorem i koderem PHP. Zwiększa on
efektywność skryptów PHP poprzez buforowanie ich w postaci
skompilowanej, dzięki czemu powtórne kompilowanie jest praktycznie
wyeliminowane. Wykorzystywane jest także parę optymalizacji, aby
przyspieszyć wykonywanie skryptów.

Więcej informacji można znaleźć pod %{url}.

%package TurckLoader
Summary:	Standalone loader of Turck MMCache's cached files
Summary(pl.UTF-8):	Osobny loader plików Turck MMCache
Group:		Libraries
Requires:	apache >= 1.3
%{?requires_php_extension}
%{?requires_zend_extension}
Provides:	TurckLoader = %{epoch}:%{version}-%{release}

%description TurckLoader
TurckLoader is a standalone loader. You can use files encoded by
without it.

%description TurckLoader -l pl.UTF-8
TurckLoader jest osobnym loaderem. Można używać plików zakodowanych
poprzez Truck MMCache bez niego samego.

%package webinterface
Summary:	WEB interface for Turck MMCache
Summary(pl.UTF-8):	Interfejs WEB dla Turck MMCache
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description webinterface
Turck MMCache can be managed through web interface script mmcache.php.
So you need to put this file on your web site. For security reasons it
is recommended to restrict the usage of this script by your local IP.

More information you can find at %{url}.

%description webinterface -l pl.UTF-8
Turck MMCache może być sterowany ze strony internetowej z
wykorzystaniem skryptu mmcache.php. Jedyne co trzeba zrobić, to
umieścić plik we właściwym miejscu na stronie internetowej. Z powodów
bezpieczeństwa zalecane jest, aby ograniczyć korzystanie ze skryptu do
lokalnego adresu.

Więcej informacji można znaleźć %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}
%patch0 -p1

%build
phpize
%configure \
	--enable-mmcache=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

cd TurckLoader
./create_links
phpize
%configure \
	--with-php-config=%{_bindir}/php-config
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir},%{_bindir},%{_mandir}/man1,%{_datadir}/%{name}}

install ./modules/mmcache.so $RPM_BUILD_ROOT%{extensionsdir}

install ./encoder.php $RPM_BUILD_ROOT%{_bindir}/turck-encode
echo '#!%{_bindir}/php4 -q' > $RPM_BUILD_ROOT%{_bindir}/turck-mmcache_password
cat ./mmcache_password.php >> $RPM_BUILD_ROOT%{_bindir}/turck-mmcache_password

install ./mmcache*.php $RPM_BUILD_ROOT%{_datadir}/%{name}

install ./TurckLoader/modules/TurckLoader.so $RPM_BUILD_ROOT%{extensionsdir}
install debian/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/TurckLoader.ini
; Enable TurckLoader
extension=TurckLoader.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%post TurckLoader
[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart

%postun TurckLoader
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php4.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php4.conf ] || %service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/mmcache.so
%attr(755,root,root) %{_bindir}/turck-encode
%attr(755,root,root) %{_bindir}/turck-mmcache_password
%{_mandir}/man1/*

%files TurckLoader
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README.loader
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/TurckLoader.ini
%attr(755,root,root) %{extensionsdir}/TurckLoader.so

%files webinterface
%defattr(644,root,root,755)
%{_datadir}/%{name}
