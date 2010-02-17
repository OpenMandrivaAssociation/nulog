Summary:	Firewall log analysis interface written in php
Name:		nulog
Version:	1.2.14
Release:	%mkrel 6
License:	GPL
Group:		System/Servers
URL:		http://www.inl.fr/Nulog.html
Source0:	http://www.inl.fr/download/%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-mdv_config.diff
Requires:	apache-mod_php
Requires:	apache-mod_ssl
Requires:	php-mysql
BuildRequires:	imagemagick
Requires(post):	ccp >= 0.4.0
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
Requires:	ulogd-mysql
Provides:	ulog-php = %{version}
Obsoletes:	ulog-php
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Nulog is a firewall log analysis interface written in php. Netfilter and NuFW
are able to log selected packets directly in a database like MySQL or
PostgreSQL. Nulog uses this interface to display security events in real-time
on a user-friendly interface.

%prep

%setup -q
%patch0 -p0

# clean up CVS stuff
for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

# fix dir perms
find . -type d | xargs chmod 755

# fix file perms
find . -type f | xargs chmod 644

%build

%install
rm -rf %{buildroot}

export DONT_RELINK=1

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}/var/www/%{name}
install -d %{buildroot}%{_datadir}/%{name}

cp -aRf * %{buildroot}/var/www/%{name}/

# cleanup
pushd %{buildroot}/var/www/%{name}
    rm -rf debian
    rm -f AUTHORS COPYING Changelog README Makefile
    find -name "\.htaccess" | xargs rm -f
popd

# fix config file location
mv %{buildroot}/var/www/%{name}/include/config.template.php %{buildroot}%{_sysconfdir}/%{name}/config.php

# fix scrips location
mv %{buildroot}/var/www/%{name}/scripts/* %{buildroot}%{_datadir}/%{name}/
rm -rf %{buildroot}/var/www/%{name}/scripts
chmod 755 %{buildroot}%{_datadir}/%{name}/*.sh
chmod 755 %{buildroot}%{_datadir}/%{name}/*.pl

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /%{name} /var/www/%{name}

<Directory /var/www/%{name}>
    Order allow,deny
    Allow from all
</Directory>

<Directory /var/www/%{name}/include>
    Order deny,allow
    Deny from all
</Directory>
EOF

# install script to call the web interface from the menu.
install -d %{buildroot}%{_libdir}/%{name}/scripts
cat > %{buildroot}%{_libdir}/%{name}/scripts/%{name} <<EOF
#!/bin/sh

url='http://localhost/%{name}'
if ! [ -z "\$BROWSER" ] && ( which \$BROWSER ); then
  browser=\`which \$BROWSER\`
elif [ -x /usr/bin/mozilla-firefox ]; then
  browser=/usr/bin/mozilla-firefox
elif [ -x /usr/bin/konqueror ]; then
  browser=/usr/bin/konqueror
elif [ -x /usr/bin/lynx ]; then
  browser='xterm -bg black -fg white -e lynx'
elif [ -x /usr/bin/links ]; then
  browser='xterm -bg black -fg white -e links'
else
  xmessage "No web browser found, install one or set the BROWSER environment variable!"
  exit 1
fi
\$browser \$url
EOF
chmod 755 %{buildroot}%{_libdir}/%{name}/scripts/%{name}

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}

convert images/nupik.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert images/nupik.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert images/nupik.png -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

# install menu entry.
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=System;Monitor;
Name=Nulog
Comment=Nulog is a firewall log analysis interface written in php.  Set the $BROWSER environment variable to choose your preferred browser.
Exec=%{_libdir}/%{name}/scripts/%{name} 1>/dev/null 2>/dev/null
Icon=%{name}xdg="true"
EOF

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt config_version \
    --oldfile %{_sysconfdir}/%{name}/config.php \
    --newfile %{_sysconfdir}/%{name}/config.php.rpmnew
%if %mdkversion < 201010
%_post_webapp
%endif
%if %mdkversion < 200900
%update_menus
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif
%if %mdkversion < 200900
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING Changelog README
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%dir %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
/var/www/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/scripts/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

