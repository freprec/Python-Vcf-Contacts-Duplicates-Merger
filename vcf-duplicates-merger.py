import vobject

s = """
BEGIN:VCARD
VERSION:3.0
EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
FN:Jeffrey Harris
N:Harris;Jeffrey;;;
ORG:Wk
END:VCARD
BEGIN:VCARD
VERSION:3.0
EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
FN:Jeffrey Harris
N:Harris;Jeffrey;;;
END:VCARD
"""

vcardlist = []
for vcard in vobject.readComponents( s ):
    vcardlist.append(vcard)

# v = vobject.readOne( s.serialize )
# v.prettyPrint()

# v = vobject.readOne( s )
# v.prettyPrint()

# returns true if two vCards have the same names and organization
def identical_name_check(vcard_a, vcard_b, ambiguity_warnings):
    has_n_attr_a = hasattr(vcard_a, 'n')
    has_fn_attr_a = hasattr(vcard_a, 'fn')
    has_org_attr_a = hasattr(vcard_a, 'org')
    
    has_n_attr_b = hasattr(vcard_b, 'n')
    has_fn_attr_b = hasattr(vcard_b, 'fn')
    has_org_attr_b = hasattr(vcard_b, 'org')

    ret = True
    if (has_n_attr_a and has_n_attr_b):
        ret = ret and (vcard_a.n.value == vcard_b.n.value)

    if (has_fn_attr_a and has_fn_attr_b):
        ret = ret and (vcard_a.fn.value == vcard_b.fn.value)
        
    if (has_org_attr_a and has_org_attr_b):
        ret = ret and (vcard_a.org.value == vcard_b.org.value)

    if (ret):
        if (has_n_attr_a ^ has_n_attr_b):
            ambiguity_warnings.append('Attribute N exists only once.\n')
        if (has_fn_attr_a ^ has_fn_attr_b):
            ambiguity_warnings.append('Attribute FN exists only once.\n')
        if (has_org_attr_a ^ has_org_attr_b):
            ambiguity_warnings.append('Attribute ORG exists only once.\n')
    
    return ret

# prints warning messages and vCards for the user to check if they are being correctly merged
def print_ambiguity_warning(ambiguity_warnings, vcard_a, vcard_b):
    print ('--- Merged with {} warning(s) ---'.format(len(ambiguity_warnings)))
    for line in ambiguity_warnings:
        print (line)
    print (vcard_a.serialize())
    print (' --and-- \n')
    print (vcard_b.serialize())





ambiguity_warnings = []
is_identical_name = identical_name_check(vcardlist[0], vcardlist[1], ambiguity_warnings)
if (len(ambiguity_warnings) > 0):
    print_ambiguity_warning(ambiguity_warnings, vcardlist[0], vcardlist[1])
