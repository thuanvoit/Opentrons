from opentrons import protocol_api


#meta
metadata = {
    'protocolName': 'Opal Assay Testing CD8 Antibody',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):
    
    
    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    ######## START ####################################################

    #command

    protocol.comment(f"{tiprack}")