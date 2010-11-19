Summary:	Firewall log analysis interface written in python
Name:		nulog
Version:	2.1.5
Release:	%mkrel 2
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
Requires:	python-IPy
Requires:	python-docutils
Requires:	ulogd-mysql
Provides:	ulog-php = %{version}
Obsoletes:	ulog-php
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

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
