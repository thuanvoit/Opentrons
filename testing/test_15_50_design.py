from opentrons import protocol_api

#meta
metadata = {
    'protocolName': 'Volume testing',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):
    
    
    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    #tuberack
    tuberack = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', location='3')

    ######## START ####################################################

    #command

    protocol.set_rail_lights(on=False)

    # protocol.pause()

    pipette.pick_up_tip()

    pipette.move_to(tuberack['A1'].bottom())
    pipette.move_to(tuberack['A2'].bottom())
    pipette.move_to(tuberack['A3'].bottom())
    pipette.move_to(tuberack['A4'].bottom())
    
    pipette.move_to(tuberack['B1'].bottom())
    pipette.move_to(tuberack['B1'].bottom())
     
    pipette.move_to(tuberack['C1'].bottom())
    pipette.move_to(tuberack['C1'].bottom())

    pipette.return_tip()

