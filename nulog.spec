Summary:	Firewall log analysis interface written in python
Name:		nulog
Version:	2.1.5
Release:	4
License:	GPL
Group:		System/Servers
URL:		http://www.inl.fr/Nulog.html
Source0:	http://www.inl.fr/download/%{name}-%{version}.tar.bz2
Source1:	nulog
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	python-devel
BuildRequires:	python-docutils
BuildRequires:	gettext
Requires:	python-nevow
Requires:	python-twisted-core
Requires:	python-matplotlib
Requires:	python-soap
Requires:	python-mysql
Requires:	mysql
Requires:	python-ipy
Requires:	python-docutils
Requires:	ulogd-mysql
Provides:	ulog-php = %{version}
Obsoletes:	ulog-php
BuildArch:	noarch

%description
Nulog is a firewall log analysis interface written in python. Netfilter and
NuFW are able to log selected packets directly in a database like MySQL or
PostgreSQL. Nulog uses this interface to display security events in real-time
on a user-friendly interface.

%prep

%setup -q

%build
make

%install
python setup.py install --root=%{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/nulog/default_user
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -d %{buildroot}/var/run/nulog
install -d %{buildroot}/var/lib/nucentral
install -d %{buildroot}%{_datadir}/nulog

mv %{buildroot}%{_sysconfdir}/nulog/default.core.conf %{buildroot}%{_sysconfdir}/nulog/core.conf
mv %{buildroot}%{_sysconfdir}/nulog/default.nulog.conf %{buildroot}%{_sysconfdir}/nulog/nulog.conf
mv %{buildroot}%{_sysconfdir}/nulog/default.wrapper.conf %{buildroot}%{_sysconfdir}/nulog/wrapper.conf

cp -fr scripts/ %{buildroot}%{_datadir}/nulog/scripts

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}

# install log rotation stuff
cat > %{buildroot}%{_sysconfdir}/logrotate.d/nulog << EOF
/var/log/nulog.log {
    create 640 root root 
    monthly
    compress
    missingok
    postrotate
	%{_initrddir}/nulog condrestart > /dev/null 2>&1 || :
    endscript
}
EOF

%post
%_post_service %{name}

%preun
%_preun_service %{name}


%files
%defattr(-,root,root)
%doc COPYING README
%{_initrddir}/%{name}
%dir %{_sysconfdir}/nulog
%dir %{_sysconfdir}/nulog/default_user
%config(noreplace) %{_sysconfdir}/nulog/core.conf
%config(noreplace) %{_sysconfdir}/nulog/nulog.conf
%config(noreplace) %{_sysconfdir}/nulog/wrapper.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/nulog
%{py_puresitedir}/auth
%{py_puresitedir}/nulog-core
%{py_puresitedir}/nulog-web
%{py_puresitedir}/wrapper
%{py_puresitedir}/Nulog-*egg-info
%{_sbindir}/nulog.tac
%{_datadir}/locale/fr/LC_MESSAGES/nulog.mo
%{_datadir}/nulog/scripts
%dir /var/run/nulog
%dir /var/lib/nucentral


%changelog
* Fri Nov 19 2010 Funda Wang <fwang@mandriva.org> 2.1.5-2mdv2011.0
+ Revision: 598867
- rebuild

* Thu Mar 04 2010 Oden Eriksson <oeriksson@mandriva.com> 2.1.5-1mdv2010.1
+ Revision: 514190
- sync with mes5 updates:
 - BR: python-docutils
 - BR: gettext
 - misc spec file fixes
 - add log rotation script

* Wed Feb 17 2010 Guillaume Rousse <guillomovitch@mandriva.org> 1.2.14-6mdv2010.1
+ Revision: 507257
- rely on filetrigger for reloading apache configuration begining with 2010.1, rpm-helper macros otherwise

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.2.14-5mdv2010.0
+ Revision: 430189
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 1.2.14-4mdv2009.0
+ Revision: 254122
- rebuild

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 1.2.14-2mdv2008.1
+ Revision: 171002
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- auto-convert XDG menu entry

* Sat Jan 05 2008 Jérôme Soyer <saispo@mandriva.org> 1.2.14-1mdv2008.1
+ Revision: 145740
- Add xdg menu
- Rediff the patch for Mandriva webapps policy
  Fix some filename
  Bump to the last release

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Wed Jun 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.8-1mdv2007.0
- 1.1.8
- rediffed P0

* Wed Jun 14 2006 Oden Eriksson <oeriksson@mandriva.com> 1.1.7-1mdk
- 1.1.7
- new name (was ulog-php)
- fix a menuentry
- add mod_rewrite rules to enforce ssl connections
- fix deps
- fix the apache config

* Sat Apr 30 2005 Marcel Pol <mpol@mandriva.org> 1.0.1-2mdk
- update filelist

* Fri Apr 29 2005 Marcel Pol <mpol@mandriva.org> 1.0.1-1mdk
- 1.0.1
- don't require mysqlserver

* Sat Aug 28 2004 Franck Villaume <fvill@freesurf.fr> 0.8.2-1mdk
- 0.8.2

* Thu Aug 14 2003 Oden Eriksson <oden.eriksson@kvikkjokk.net> 0.7-1mdk
- initial cooker contrib

