Name:       sailfish-setup
Summary:    Sailfish Setup
Version:    0.1.0
Release:    1
License:    Public Domain
Url:        https://github.com/sailfishos/sailfish-setup
Source0:    %{name}-%{version}.tar.bz2
BuildArch:  noarch

Requires: setup
Requires(pre): setup
# Some mandatory groups are created by systemd like input
Requires: systemd
Requires(pre): systemd
Requires(pre): /usr/bin/getent
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/sbin/usermod
Recommends: hardware-adaptation-setup

%description
This package is responsible for creating Sailfish OS specific users
and groups on which other packages may depend on.

%pre
groupadd -rf privileged || :
groupadd -rf sailfish-mdm || :
if ! getent passwd sailfish-mdm >/dev/null ; then
    useradd -r -g sailfish-mdm -G privileged -d / -s /sbin/nologin sailfish-mdm || :
fi
groupadd -rf sailfish-radio || :
groupadd -rf sailfish-actdead || :
if ! getent passwd sailfish-actdead >/dev/null ; then
    useradd -r -g sailfish-actdead -d / -s /sbin/nologin sailfish-actdead || :
fi

groupadd -rf sailfish-system || :
usermod -a -G sailfish-system sailfish-mdm || :

groupadd -rf ssu || :

groupadd -rf sailfish-alarms || :

groupadd -rf sailfish-datetime || :

groupadd -rf timed || :

%prep
%setup -q

%build

%install
install -D group.ids $RPM_BUILD_ROOT%{_datadir}/%{name}/group.ids

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
