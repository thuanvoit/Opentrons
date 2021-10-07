# This protocol is by me; it’s called Opentrons Protocol Tutorial and is used for demonstrating the OT-2 Python Protocol API. It uses version 2.0 of this API.

# Begin the protocol

# Add a 96 well plate, and place it in slot ‘2’ of the robot deck

# Add a 300 µL tip rack, and place it in slot ‘1’ of the robot deck

# Add a single-channel 300 µL pipette to the left mount, and tell it to use that tip rack

# Transfer 100 µL from the plate’s ‘A1’ well to its ‘B2’ well

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'Testing Protocol',
    'author': 'tv',
    'description': 'Simple protocol to get started using OT2',
    'apiLevel': '2.10'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions
def run(protocol: protocol_api.ProtocolContext):

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', location='5')
    tuberack = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', location='3')

    # pipettes
    left_pipette = protocol.load_instrument(
         'p300_single', 'left', tip_racks=[tiprack])

    # commands
    rows = ['A', 'B', 'C']

    for row in rows:
        left_pipette.pick_up_tip()

        for i in range(2):
            left_pipette.aspirate(100, tuberack[f'{row}1'])
            left_pipette.dispense(100, plate[f'{row}{i+1}'])

        left_pipette.drop_tip()
    
    left_pipette.pick_up_tip()
    left_pipette.aspirate(300, tuberack[f'{rows[0]}3'])
    for i in range(3):
        left_pipette.dispense(100, plate[f'{rows[2]}{i+1}'])
    left_pipette.drop_tip()