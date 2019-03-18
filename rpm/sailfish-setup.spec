Name:       sailfish-setup
Summary:    Sailfish Setup
Version:    0.1.0
Release:    1
Group:      System/Base
License:    Public Domain
Url:        https://github.com/sailfishos/sailfish-setup
Source0:    %{name}-%{version}.tar.bz2

Requires(pre): setup

%description
%{summary}.

%pre
groupadd -rf privileged || :
groupadd -rf sailfish-mdm || :
if ! getent passwd sailfish-mdm >/dev/null ; then
    useradd -r -g sailfish-mdm -G privileged -d / -s /sbin/nologin sailfish-mdm || :
fi
groupadd -rf sailfish-radio || :

%files
%defattr(-,root,root,-)
