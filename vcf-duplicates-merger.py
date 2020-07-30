import vobject
card = vobject.vCard()
card.behavior

s = """
BEGIN:VCARD
VERSION:3.0
EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
FN:Jeffrey Harris
N:Harris;Jeffrey;;;
END:VCARD
BEGIN:VCARD
VERSION:3.0
EMAIL;TYPE=INTERNET:jeffrey@osafoundation.org
FN:Jeffrey Arsch
N:Arsch;Jeffrey;;;
END:VCARD
"""

vcardlist = []
for vcard in vobject.readComponents( s ):
    vcardlist.append(vcard)

vcard0 = vcardlist[0].serialize()
vcard1 = vcardlist[1].serialize()

vcardlist[0].prettyPrint()
vcardlist[1].prettyPrint()

# v = vobject.readOne( s.serialize )
# v.prettyPrint()

# v = vobject.readOne( s )
# v.prettyPrint()