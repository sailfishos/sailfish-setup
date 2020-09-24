#!/bin/sh
# Copyright (c) 2020 Open Mobile Platform LLC.
#
# Manages groups created within packages.
# Currently only groups for accounts may be managed with this.
#
# Use like this in spec file to create a group named account-provider_name for
# account provider named provider_name (substitute your own provider name):
#
#     Requires(post): %{_libexecdir}/manage-groups
#     Requires(postun): %{_libexecdir}/manage-groups
#
#     %post
#     %{_libexecdir}/manage-groups add account-provider_name || :
#
#     %postun
#     if [ "$1" -eq 0 ]; then
#         %{_libexecdir}/manage-groups remove account-provider_name || :
#     fi

usage() { # $1: invalid argument or an error message
    echo "Invalid arguments: $1"
    echo "$0 add|remove <group>"
    echo "or"
    echo "$0 check <uid>"
    exit 1
}

_group_name_check() { # $1: group name
    if [ "$1" = "${1#account-}" ]
    then
        echo "Currently only groups with account- prefix may be managed"
        exit 2
    fi
}

_get_flag_file() { # $1: group name or group prefix
    case "${1%%-*}" in
        "account") echo "/var/lib/sailfish-mdm/accounts-managed" ;;
        "*") echo "/doesnotexist" ;;
    esac
}

_add_users_to_managed_group() { # $1: usernames, $2: group name
    if [ ! -e "$(_get_flag_file "$1")" ]
    then
        for username in $(echo "$1" | tr , " ")
        do
            usermod -a -G "$2" "$username"
        done
    fi
}

add_group() { # $1: group name
    _group_name_check "$1"
    groupadd -r "$1"
    _add_users_to_managed_group "$(getent group users | cut -d: -f4)" "$1"
}

remove_group() { # $1: group name
    _group_name_check "$1"
    groupdel "$1"
}

_add_to_groups() { # $1: username, $2: new groups
    # Try to add all at once
    if ! usermod -a -G "$2" "$1"
    then
        # In case of a failure add one by one and log errors
        for group in $(echo "$2" | tr , " ")
        do
            if ! usermod -a -G "$group" "$1"
            then
                # Let's be loud about the error
                echo "ERROR: Could not add $1 to $group, the system may be broken"
            fi
        done
    fi
}

_add_to_managed_groups() { # $1: username, $2: prefix
    if [ -e "$(_get_flag_file "$2")" ]
    then
        echo "${2}-* groups are managed, not touching"
    else
        _add_to_groups "$1" "$(grep -oE "^${2}-[^:]+" "/etc/group" | head -c -1 | tr '\n' ,)"
    fi
}

check_user() { # $1: uid
    # shellcheck source=group_ids.env
    . "/usr/share/sailfish-setup/group_ids.env"
    username=$(getent passwd "$1" | cut -d: -f1)
    if [ "$1" -eq "100000" ] # checking for device owner
    then
        _add_to_groups "$username" "$SYSTEM_GROUPS"
    fi
    # everyone
    _add_to_groups "$username" "$USER_GROUPS"
    _add_to_managed_groups "$username" "account"
}

if [ "$#" -lt "2" ]
then
    usage "Not enough arguments"
elif [ "$#" -gt "2" ]
then
    usage "Too many arguments"
fi

case "$1" in
    "add") add_group "$2" ;;
    "remove") remove_group "$2" ;;
    "check") check_user "$2" ;;
    *) usage "$1" ;;
esac

# vim: expandtab sw=4 ts=4
