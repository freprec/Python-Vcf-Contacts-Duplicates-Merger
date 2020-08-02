import vobject

disable_warnings_for_empty_contacts = True  # only show warnings for vCards with more than a single attribute
input_file_path = ""
output_file_path = "dupmerged_" + input_file_path
#input_file = open(input_file_path, "r")
#output_file = open(output_file_path, "w")

vcardlist = []
with open(input_file_path, "rt") as input_file:
    for vcard in vobject.readComponents( input_file.read() ):
        vcardlist.append(vcard)

# count attributes with actual content
def count_vcard_content(vcard):
    content_counter = 0
    for attribute in vcard.contents:
        for item in vcard.contents[attribute]:
            if ((item.value != '') and (attribute not in ['version', 'prodid'])):
                content_counter += 1
    return content_counter

# returns true if both vCards have the same names (or same organization if names are empty)
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
        # count attributes with actual content
        content_counter_a = count_vcard_content(vcard_a)
        content_counter_b = count_vcard_content(vcard_b)

        if ((not disable_warnings_for_empty_contacts) \
            or disable_warnings_for_empty_contacts \
            and content_counter_a > 1 and content_counter_b > 1):   # only show warnings for vCards with more than a single attribute
            if (has_n_attr_a ^ has_n_attr_b):
                ambiguity_warnings.append('Attribute N exists only once.\n')
            if (has_fn_attr_a ^ has_fn_attr_b):
                ambiguity_warnings.append('Attribute FN exists only once.\n')
            if (has_org_attr_a ^ has_org_attr_b):
                ambiguity_warnings.append('Attribute ORG exists only once.\n')
    
    return ret

# prints warning messages and vCards for the user to check if they are being correctly merged
def print_ambiguity_warning(ambiguity_warnings, vcard_a, vcard_b):
    print('--- Merged with {} warning(s): ---'.format(len(ambiguity_warnings)))
    for line in ambiguity_warnings:
        print(line)
    print(vcard_a.serialize())
    print(' --and-- \n')
    print(vcard_b.serialize())

# add the FN attribute to the vCard if not present
def add_fn_attribute(vcard):
    if (not hasattr(vcard, 'fn')):
        vcard.add('fn')

# add an item to a vCard attribute
def add_to_vcard_attribute(vcard, attribute, item):
    vcard.add(attribute).value = item.value
    value_index = len(vcard.contents[attribute]) - 1
    vcard.contents[attribute][value_index].params = item.params

# merge two vCards
def merge_vcards(vcard_in, vcard_merge):
    for attribute in vcard_in.contents:
        if hasattr(vcard_merge, attribute):
            for item in vcard_in.contents[attribute]:
                if item not in vcard_merge.contents[attribute]:
                    add_to_vcard_attribute(vcard_merge, attribute, item)
        else:
            for item in vcard_in.contents[attribute]:
                add_to_vcard_attribute(vcard_merge, attribute, item)

out_index = 0               # index counter for output of vCards
merge_indices_dict = { }    # dictionary for tracking merged vCards: key - input index, value - output index
out_vcards_list = []        # list for the remaining merged vCards

for i in range(len(vcardlist)):
    if i in merge_indices_dict:
        continue    # vCard was already merged into out_vcards_list
    else:
        merge_indices_dict[i] = out_index       # set output index of vCard
        out_vcards_list.append(vcardlist[i])    # add vCard to out_vcards_list

    for j in range(i + 1, len(vcardlist)):
        if j in merge_indices_dict:
            continue    # vCard was already merged into out_vcards_list

        ambiguity_warnings = []
        is_identical_name = identical_name_check(vcardlist[i], vcardlist[j], ambiguity_warnings)
        # VObject requires the FN attribute to be present
        add_fn_attribute(vcardlist[i])
        add_fn_attribute(vcardlist[j])
        if (is_identical_name):
            merge_indices_dict[j] = out_index # set output index of vCard
            # merge the vCards into out_vcards_list
            merge_vcards(vcardlist[j], out_vcards_list[out_index])

            if (len(ambiguity_warnings) > 0):
                print_ambiguity_warning(ambiguity_warnings, vcardlist[i], vcardlist[j])
    
    out_index += 1

# write the vCards to the output file
with open(output_file_path, "wt") as output_file:
    for vcard in out_vcards_list:
        serial_vcard = vcard.serialize()
        output_file.write(vcard.serialize())
