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
# Commands used by scriptlets
Requires(pre): /usr/bin/getent
Requires(pre): /usr/sbin/groupadd
Requires(pre): /usr/sbin/useradd
Requires(pre): /usr/sbin/usermod
# Needed by manage-groups.sh
Requires: /usr/bin/getent
Requires: /usr/sbin/groupadd
Requires: /usr/sbin/groupdel
Requires: /usr/sbin/usermod
Requires: coreutils
Requires: grep
# Other
Recommends: hardware-adaptation-setup
Provides: %{_libexecdir}/manage-groups

%description
This package is responsible for creating Sailfish OS specific users
and groups on which other packages may depend on.

%pre
groupadd -rf privileged || :
if ! getent passwd privileged >/dev/null ; then
    useradd -r -g privileged  -d / -s /sbin/nologin privileged || :
fi

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

groupadd -rf sailfish-phone || :

groupadd -rf sailfish-messages || :

groupadd -rf sailfish-authentication || :
if ! getent passwd sailfish-code >/dev/null ; then
    useradd -r -g sailfish-authentication -d / -s /sbin/nologin sailfish-code || :
fi
if ! getent passwd sailfish-fingerprint >/dev/null ; then
    useradd -r -g sailfish-authentication -d / -s /sbin/nologin sailfish-fingerprint || :
fi

APPSUPPORT_BASE_UID=500000
if ! getent group appsupport-root >/dev/null ; then
    groupadd -g $APPSUPPORT_BASE_UID appsupport-root || :
fi

if ! getent group appsupport-system >/dev/null ; then
    APPSUPPORT_SYSTEM=$(($APPSUPPORT_BASE_UID + 1000))
    groupadd -g $APPSUPPORT_SYSTEM appsupport-system || :
fi

if ! getent group appsupport-radio >/dev/null ; then
    APPSUPPORT_RADIO=$(($APPSUPPORT_BASE_UID + 1001))
    groupadd -g $APPSUPPORT_RADIO appsupport-radio || :
fi

if ! getent group appsupport-media_rw >/dev/null ; then
    APPSUPPORT_MEDIA_RW=$(($APPSUPPORT_BASE_UID + 1023))
    groupadd -g $APPSUPPORT_MEDIA_RW appsupport-media_rw || :
fi

if ! getent passwd appsupport-root >/dev/null ; then
    useradd -u $APPSUPPORT_BASE_UID -g appsupport-root -G appsupport-system,appsupport-radio,appsupport-media_rw -d /home/appsupport-root -s /sbin/nologin appsupport-root || :
fi

usermod --add-subuids $APPSUPPORT_BASE_UID-$(($APPSUPPORT_BASE_UID + 200000 - 1)) --add-subgids $APPSUPPORT_BASE_UID-$(($APPSUPPORT_BASE_UID + 200000 - 1)) root || :
usermod --add-subuids $APPSUPPORT_BASE_UID-$(($APPSUPPORT_BASE_UID + 200000 - 1)) --add-subgids $APPSUPPORT_BASE_UID-$(($APPSUPPORT_BASE_UID + 200000 - 1)) appsupport-root || :

%prep
%setup -q

%build

%install
install -D group_ids.env $RPM_BUILD_ROOT%{_datadir}/%{name}/group_ids.env
install -D scripts/manage-groups.sh $RPM_BUILD_ROOT%{_libexecdir}/manage-groups

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_libexecdir}/manage-groups
