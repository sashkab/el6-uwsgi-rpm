Name:           uwsgi
Version:        2.0.8
Release:        2%{?dist}
Summary:        Fast, self-healing, application container server
Group:          System Environment/Daemons
License:        GPLv2
URL:            http://projects.unbit.it/uwsgi
Source0:        http://projects.unbit.it/downloads/%{name}-%{version}.tar.gz
Source1:        rhel6.ini
Source2:        uwsgi.init
Patch0:         uwsgi_trick_chroot_rpmbuild.patch
Patch1:         uwsgi_fix_rpath.patch
Patch2:         uwsgi_multi_app_env.patch
BuildRequires:  python2-devel, libxml2-devel, libuuid-devel, ruby, ruby-devel
BuildRequires:  libyaml-devel, perl-devel, pcre-devel, perl-ExtUtils-Embed

%description
uWSGI is a fast (pure C), self-healing, developer/sysadmin-friendly
application container server.  Born as a WSGI-only server, over time it has
evolved in a complete stack for networked/clustered web applications,
implementing message/object passing, caching, RPC and process management.
It uses the uwsgi (all lowercase, already included by default in the Nginx
and Cherokee releases) protocol for all the networking/interprocess
communications.  Can be run in preforking mode, threaded,
asynchronous/evented and supports various form of green threads/co-routine
(like uGreen and Fiber).  Sysadmin will love it as it can be configured via
command line, environment variables, xml, .ini and yaml files and via LDAP.
Being fully modular can use tons of different technology on top of the same
core.

%package -n %{name}-devel
Summary:  uWSGI - Development header files and libraries
Group:    Development/Libraries
Requires: %{name}

%description -n %{name}-devel
This package contains the development header files and libraries
for uWSGI extensions


%package -n %{name}-plugin-cgi
Summary:  uWSGI - CGI plugin for uWSGI
Group:    System Environment/Daemons
Requires: %{name}

%description -n %{name}-plugin-cgi
This package contains the CGI plugin used with uWSGI.


%package -n %{name}-plugin-python
Summary:  uWSGI - Plugin for Python support
Group:    System Environment/Daemons
Requires: python, %{name}

%description -n %{name}-plugin-python
This package contains the python plugin for uWSGI

%package -n %{name}-plugin-rack
Summary:  uWSGI - Plugin for Ruby rack support
Group:    System Environment/Daemons
Requires: ruby, %{name}

%description -n %{name}-plugin-rack
This package contains the Ruby rack plugin for uWSGI

%package -n %{name}-plugin-psgi
Summary:  uWSGI - Plugin for Perl PSGI support
Group:    System Environment/Daemons
Requires: perl, %{name}

%package -n %{name}-plugin-http
Summary:  uWSGI - Plugin for HTTP support
Group:    System Environment/Daemons
Requires: %{name}

%package -n %{name}-plugin-corerouter
Summary:  uWSGI - Plugin for corerouter
Group:    System Environment/Daemons
Requires: %{name}

%description -n %{name}-plugin-psgi
This package contains the Perl PSGI plugin for uWSGI

%description -n %{name}-plugin-http
This package contains the HTTP plugin for uWSGI

%description -n %{name}-plugin-corerouter
This package contains the corerouter plugin for uWSGI

%prep
%setup -q
cp -p %{SOURCE1} buildconf/
echo "plugin_dir = %{_libdir}/%{name}" >> buildconf/$(basename %{SOURCE1})
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
CFLAGS="%{optflags}" python uwsgiconfig.py --build rhel6

%install
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
mkdir -p %{buildroot}%{_localstatedir}/run/%{name}
%{__install} -p -m 0755 uwsgi %{buildroot}%{_sbindir}
%{__install} -d -m 0755 %{buildroot}%{_initrddir}
%{__install} -p -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%{__install} -p -m 0644 *.h %{buildroot}%{_includedir}/%{name}
%{__install} -p -m 0755 *_plugin.so %{buildroot}%{_libdir}/%{name}

%pre
getent group uwsgi >/dev/null || groupadd -r uwsgi
getent passwd uwsgi >/dev/null || \
    useradd -r -g uwsgi -d '/etc/uwsgi' -s /sbin/nologin \
    -c "uWSGI Service User" uwsgi

%post
/sbin/chkconfig --add uwsgi

%preun
if [ $1 -eq 0 ]; then
    /sbin/service uwsgi stop >/dev/null 2>&1
    /sbin/chkconfig --del uwsgi
fi

%postun
if [ $1 -ge 1 ]; then
    /sbin/service uwsgi condrestart >/dev/null 2>&1 || :
fi

%files
%defattr(-,root,root)
%{_sbindir}/%{name}
%dir %{_sysconfdir}/%{name}
%{_initrddir}/%{name}
%doc LICENSE README
%attr(0755,uwsgi,uwsgi) %{_localstatedir}/log/%{name}
%attr(0755,uwsgi,uwsgi) %{_localstatedir}/run/%{name}

%files -n %{name}-devel
%{_includedir}/%{name}

%files -n %{name}-plugin-cgi
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/cgi_plugin.so

%files -n %{name}-plugin-python
%{_libdir}/%{name}/python_plugin.so

%files -n %{name}-plugin-rack
%{_libdir}/%{name}/rack_plugin.so

%files -n %{name}-plugin-psgi
%{_libdir}/%{name}/psgi_plugin.so

%files -n %{name}-plugin-http
%{_libdir}/%{name}/http_plugin.so

%files -n %{name}-plugin-corerouter
%{_libdir}/%{name}/corerouter_plugin.so

%changelog
* Wed Feb 11 2015 Rohit Deshmukh <raigad1630@gmail.com> - 2.0.8-2
- added patch multi_app_env.patch to remove env error messages on multi app setup

* Tue Dec 02 2014 Mark Carbonaro <mark@carbonaro.org> - 2.0.8
- Updated to latest upstream stable version
- Added http and corerouter plugins

* Sat Sep 06 2014 Alan Chalmers <alan.chalmers@gmail.com> - 2.0.7
- Upgraded to latest stable upstream version

* Thu Jun 19 2014 Aleks Bunin <sbunin@gmail.com> - 2.0.5.1-2
- Restored cgi plugin

* Tue Jun 03 2014 Sergey Morozov <sergey.morozov@corp.mail.ru> - 2.0.5.1-1
- Build now inherits "base" buildconf with only python, rack and psgi plugins
- Removed wiki doc
- Upgraded to latest stable upstream version

* Thu Apr 19 2012 Aleks Bunin <sbunin@gmail.com> - 1.1.2-1
- RHEL 6 Support (removed not compatible plugins)
- Upgraded to latest stable upstream version

* Sun Feb 19 2012 Jorge A Gallegos <kad@blegh.net> - 1.0.4-1
- Addressing issues from package review feedback
- s/python-devel/python2-devel
- Make the libdir subdir owned by -plugins-common
- Upgraded to latest stable upstream version

* Mon Feb 06 2012 Jorge A Gallegos <kad@blegh.net> - 1.0.2.1-2
- Fixing 'unstripped-binary-or-object'

* Thu Jan 19 2012 Jorge A Gallegos <kad@blegh.net> - 1.0.2.1-1
- New upstream version

* Thu Dec 08 2011 Jorge A Gallegos <kad@blegh.net> - 0.9.9.3-1
- New upstream version

* Sun Oct 09 2011 Jorge A Gallegos <kad@blegh.net> - 0.9.9.2-2
- Don't download the wiki page at build time

* Sun Oct 09 2011 Jorge A Gallegos <kad@blegh.net> - 0.9.9.2-1
- Updated to latest stable version
- Correctly linking plugin_dir
- Patches 1 and 2 were addressed upstream

* Sun Aug 21 2011 Jorge A Gallegos <kad@blegh.net> - 0.9.8.3-3
- Got rid of BuildRoot
- Got rid of defattr()

* Sun Aug 14 2011 Jorge Gallegos <kad@blegh.net> - 0.9.8.3-2
- Added uwsgi_fix_rpath.patch
- Backported json_loads patch to work with jansson 1.x and 2.x
- Deleted clean steps since they are not needed in fedora

* Sun Jul 24 2011 Jorge Gallegos <kad@blegh.net> - 0.9.8.3-1
- rebuilt
- Upgraded to latest stable version 0.9.8.3
- Split packages

* Sun Jul 17 2011 Jorge Gallegos <kad@blegh.net> - 0.9.6.8-2
- Heavily modified based on Oskari's work

* Mon Feb 28 2011 Oskari Saarenmaa <os@taisia.fi> - 0.9.6.8-1
- Initial.
