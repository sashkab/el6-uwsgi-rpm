el6-uwsgi-rpm
=============

Files to create RPM for uwsgi on el6 (rhel 6 or centos 6).  Updated to latest stable version.

Based on following:

https://github.com/jgoldschrafe/rpm-uwsgi

https://github.com/rthill/rpm-uwsgi

https://bugzilla.redhat.com/show_bug.cgi?id=682704

https://github.com/edestler/el6-uwsgi-rpm

## Installation instructions

    yum install -y rpm-build rpmdevtools readline-devel ncurses-devel gdbm-devel tcl-devel openssl-devel db4-devel byacc libuuid-devel ruby ruby-devel perl-ExtUtils-Embed libyaml-devel libffi-devel make python2-devel libxml2-devel pcre-devel gcc
    git clone https://github.com/sashkab/el6-uwsgi-rpm.git $HOME/rpmbuild
    wget http://projects.unbit.it/downloads/uwsgi-2.0.7.tar.gz -O $HOME/rpmbuild/SOURCES/uwsgi-2.0.7.tar.gz
    cd $HOME/rpmbuild/SPECS && rpmbuild -bb uwsgi.spec

When compilations completes, rpms will be in `$HOME/rpmbuild/RPMS`.
