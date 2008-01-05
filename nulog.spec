Summary:	Nulog is a firewall log analysis interface written in php
Name:		nulog
Version:	1.2.14
Release:	%mkrel 1
License:	GPL
Group:		System/Servers
URL:		http://www.inl.fr/Nulog.html
Source0:	http://www.inl.fr/download/%{name}-%{version}.tar.bz2
Patch0:		%{name}-%{version}-mdv_config.diff
Requires(pre):	apache-mod_php apache-mod_ssl php-mysql
Requires:	apache-mod_php apache-mod_ssl php-mysql
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRequires:	ImageMagick
BuildRequires:	apache-base >= 2.0.54
Requires(post):	ccp >= 0.4.0
Requires:	ulogd-mysql
Provides:	ulog-php = %{version}
Obsoletes:	ulog-php
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

# strip away annoying ^M
find -type f | grep -v "\.gif" | grep -v "\.png" | grep -v "\.jpg" | grep -v "\.z" | xargs dos2unix -U

%build

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
    Allow from All
</Directory>

<Directory /var/www/%{name}/include>
    Order Deny,Allow
    Deny from All
    Allow from None
</Directory>

<LocationMatch /%{name}>
    Options FollowSymLinks
    RewriteEngine on
    RewriteCond %{SERVER_PORT} !^443$
    RewriteRule ^.*$ https://%{SERVER_NAME}%{REQUEST_URI} [L,R]
</LocationMatch>

EOF

# install script to call the web interface from the menu.
install -d %{buildroot}%{_libdir}/%{name}/scripts
cat > %{buildroot}%{_libdir}/%{name}/scripts/%{name} <<EOF
#!/bin/sh

url='https://localhost/%{name}'
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
install -d %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%{name}): needs=X11 \
section="System/Monitoring" \
title="Nulog" \
longtitle="Nulog is a firewall log analysis interface written in php.  Set the $BROWSER environment variable to choose your preferred browser." \
command="%{_libdir}/%{name}/scripts/%{name} 1>/dev/null 2>/dev/null" \
icon="%{name}.png"
EOF

%post
ccp --delete --ifexists --set "NoOrphans" --ignoreopt config_version --oldfile %{_sysconfdir}/%{name}/config.php --newfile %{_sysconfdir}/%{name}/config.php.rpmnew
%_post_webapp
%update_menus

%postun
%_postun_webapp
%clean_menus

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING Changelog README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%dir %attr(0755,root,root) %{_sysconfdir}/%{name}
%attr(0640,apache,root) %config(noreplace) %{_sysconfdir}/%{name}/config.php
/var/www/%{name}
%attr(0755,root,root) %{_libdir}/%{name}/scripts/%{name}
%dir %attr(0755,root,root) %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

