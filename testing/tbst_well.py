from opentrons import protocol_api

#meta
metadata = {
    'protocolName': 'well testing',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):

    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', location='1')
    
    pipette = protocol.load_instrument('p1000_single', 'right', tip_racks=[tiprack])

    well = protocol.load_labware('agilent_1_reservoir_290ml', location='2')
    
    tuberack_15 = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='3')
    

    pipette.pick_up_tip()
    

    pipette.move_to(well['A1'].bottom())

    protocol.pause()

    pipette.move_to(tuberack_15['A1'].top())
    pipette.move_to(tuberack_15['A1'].bottom())

    pipette.move_to(tuberack_15['C2'].top())
    pipette.move_to(tuberack_15['C2'].bottom())

    pipette.move_to(tuberack_15['B3'].top())
    pipette.move_to(tuberack_15['B3'].bottom())

    pipette.move_to(tuberack_15['C4'].top())
    pipette.move_to(tuberack_15['C4'].bottom())

    pipette.move_to(tuberack_15['A5'].top())
    pipette.move_to(tuberack_15['A5'].bottom())



    pipette.return_tip()
