import struct


# You parse function here

def _parse_template(msg_in):
    out_msg = struct.unpack('i', msg_in)
    return out_msg[0]

PROFILE_TYPE = {
    "1": _parse_template,
}


def parse_data_by_profile_type(msg, profile_type):
    out_msg = None
    if profile_type in PROFILE_TYPE:
        try:
            out_msg = PROFILE_TYPE[profile_type](msg)
        except Exception as e:
            print e
    else:
        print "profile type %s not exist"%profile_type
    return out_msg
