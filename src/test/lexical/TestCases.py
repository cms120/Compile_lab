from lexical.FA import FA

fa_s = [FA(  # ppt 3_2 page22
    k=['S', 'Q', 'U', 'V', 'Z', 'phi'],
    letters=['0', '1'],
    f=[(('S', '0'), ['V', 'Q']),
       (('S', '1'), ['U', 'Q']),
       (('U', '0'), ['phi']),
       (('U', '1'), ['Z']),
       ],
    s='S',
    z=['Z']
)]