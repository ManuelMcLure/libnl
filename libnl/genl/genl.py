"""Generic Netlink (lib/genl/genl.c).
https://github.com/thom311/libnl/blob/master/lib/genl/genl.c

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation version 2.1
of the License.
"""

from libnl.errno import NLE_MSG_TOOSHORT
from libnl.linux_private.genetlink import GENL_HDRLEN
from libnl.linux_private.netlink import NLMSG_ALIGN
from libnl.msg import nlmsg_data


def genlmsg_valid_hdr(nlh, hdrlen):
    """Validate Generic Netlink message headers.
    https://github.com/thom311/libnl/blob/master/lib/genl/genl.c#L117

    Verifies the integrity of the Netlink and Generic Netlink headers by enforcing the following requirements:
        - Valid Netlink message header (nlmsg_valid_hdr()).
        - Presence of a complete Generic Netlink header.
        - At least \c hdrlen bytes of payload included after the generic netlink header.

    Returns:
    A positive integer (True) if the headers are valid or 0 (False) if not.
    """
    if not nlmsg_valid_hdr(nlh, GENL_HDRLEN):
        return 0
    ghdr = nlmsg_data(nlh)
    if genlmsg_len(ghdr) < NLMSG_ALIGN(hdrlen):
        return 0
    return 1


def genlmsg_parse(nlh, hdrlen, tb, maxtype, policy):
    """Parse Generic Netlink message including attributes.
    https://github.com/thom311/libnl/blob/master/lib/genl/genl.c#L191

    Verifies the validity of the Netlink and Generic Netlink headers using genlmsg_valid_hdr() and calls nla_parse() on
    the message payload to parse eventual attributes.

    Positional arguments:
    nlh -- pointer to Netlink message header.
    hdrlen -- length of user header.
    tb -- array to store parsed attributes.
    maxtype -- maximum attribute id expected.
    policy -- attribute validation policy.

    Returns:
    0 on success or a negative error code.
    """
    if not genlmsg_valid_hdr(nlh, hdrlen):
        return -NLE_MSG_TOOSHORT
    ghdr = nlmsg_data(nlh)
    _gad = genlmsg_attrdata(ghdr, hdrlen)
    _gal = genlmsg_attrlen(ghdr, hdrlen)
    return int(nla_parse(tb, maxtype, _gad, _gal, policy))