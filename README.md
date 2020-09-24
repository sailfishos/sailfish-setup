Sailfish Setup
==============

This package is responsible for creating Sailfish OS specific users
and groups which other packages may depend on.

Usage
-----

A package that requires that Sailfish OS specific users and/or groups are
already created should have following prerequisite:
Requires(pre): sailfish-setup

Users
-----
Users that this package defines are listed below.

- privileged
- sailfish-mdm
- sailfish-actdead
- sailfish-code
- sailfish-fingerprint

Groups
------
Groups that this package defines are listed below.

- privileged
  - For processes that need to be able to access privileged data.
- sailfish-system
  - For users that need to be able to control the device settings.
    Device owner belongs to this group.
- sailfish-mdm
  - For sailfish-mdm user and processes that need to be able to access
    MDM APIs.
- sailfish-radio
  - For processes that need to be able to access mobile network related APIs.
- sailfish-phone
  - For users that need to be able to make calls.
- sailfish-messages
  - For users that need to be able to send SMS and MMS.
- sailfish-alarms
  - For users that need to be able to access shared alarm events.
- sailfish-datetime
  - For users that need to be able to modify clock settings.
- timed
  - For users and timed process, required to change system default timezone.
- sailfish-actdead
  - For sailfish-actdead user.
- sailfish-authentication
  - For device lock.

Device owner's (SYSTEM\_GROUPS) and additional users' (USER\_GROUPS and
USER\_GROUPS\_DEFAULT) groups are stored in file
***/usr/share/sailfish-setup/group_ids.env***. Device owner will be created
during boot if it does not already exist.

Account groups
--------------
Account provider group specifies all users that are allowed to create an account
for respective provider. They are not created inside this package but instead
they have a specific format and are created by account packages themselves.

There is a script for managing these groups. If you want that to limit an
account provider to arbitrary users, see ***scripts/manage-groups.sh*** script
for more instructions. If account provider is limited to a group that is already
listed in this file instead, you don't need to create account provider group but
you should still specify the needed group within account provider configuration.
