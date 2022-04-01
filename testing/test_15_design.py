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
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', location='1')    
    #pipettes
    pipette = protocol.load_instrument('p1000_single', 'right', tip_racks=[tiprack])

    #tuberack
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='3')

    ######## START ####################################################

    #command

    protocol.set_rail_lights(on=False)

    # protocol.pause()

    pipette.pick_up_tip()

    for letter in ["A", "B", "C"]:
        for n in [1,2,3,4,5]:
            pipette.move_to(tuberack[letter+str(n)].top())
            protocol.pause()
            pipette.move_to(tuberack[letter+str(n)].bottom())
            protocol.pause()

        protocol.pause()

    pipette.return_tip()

  