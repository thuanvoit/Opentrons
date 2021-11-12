from opentrons import protocol_api

#meta
metadata = {
    'protocolName': 'well testing',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):

    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    well = protocol.load_labware('agilent_1_reservoir_290ml', location='2')


    pipette.pick_up_tip()
    
    pipette.move_to(well['A1'].top())

    protocol.pause()

    pipette.move_to(well['A1'].bottom())

    protocol.pause()

    pipette.aspirate(300, well['A1'])
    pipette.dispense(300, well['A1'])

    pipette.return_tip()
