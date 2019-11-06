Name:       sailfish-setup
Summary:    Sailfish Setup
Version:    0.1.0
Release:    1
Group:      System/Base
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
Recommends: hardware-adaptation-setup

%description
%{summary}.

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

# TODO : This should be moved to the first boot (JB#48049)
# Make sure that device owner exists.
groupadd -fg 100000 nemo || :
if ! getent passwd nemo >/dev/null ; then
    # Requirements - source component in brackets:
    # video for display (setup), input input devices (systemd), audio for itself (setup)
    useradd -g nemo -G "video,input,audio" -u 100000 -m nemo || :
fi

groupadd -rf sailfish-system || :
usermod -a -G sailfish-system nemo || :
usermod -a -G sailfish-system sailfish-mdm || :

groupadd -rf ssu || :

%files
%defattr(-,root,root,-)
