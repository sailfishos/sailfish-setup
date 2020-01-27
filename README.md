Sailfish Setup
==============

This package is responsible for creating Sailfish OS specific users and/or groups on which
other packages could depend on.

Usage
-----

A package that requires that Sailfish OS specific users and/or groups are
already created should have following prerequisite:
Requires(pre): sailfish-setup

Users
-----
Users that this package defines are listed below.

- sailfish-mdm

Groups
------
Groups that this package defines are listed below.

- privileged
  - For processes that need to be able to access privileged data.
- sailfish-system
  - For users and processes that need to be able to control the device.
    Device owner belongs to this group.
- sailfish-mdm
  - For processes that need to be able to access MDM APIs.
- sailfish-radio
  - For processes that need to be able to access mobile network related APIs.
- sailfish-alarms
  - For processes that need to be able to access shared alarm events.
- sailfish-datetime
  - For processes that need to be able to modify clock settings.
- timed
  - For timed process, required for changing system default timezone

Default system (SYSTEM_GROUPS) and additional user (USER_GROUPS) groups are
stored in the file /usr/share/sailfish-setup/group.ids, system user will be created during
boot if it does not already exist.
