from opentrons import protocol_api

#meta
metadata = {
    'protocolName': 'demo chacha_tbst_tubeholder',
    'author': 'thuanvo',
    'description': 'Demo',
    'apiLevel': '2.10'
}

def run(protocol: protocol_api.ProtocolContext):

    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', location='4')
    pipette = protocol.load_instrument('p1000_single', 'right', tip_racks=[tiprack])
    chacha_labware = protocol.load_labware('kissicklabdesign_384_wellplate_80ul', location='5')
    
    pipette.pick_up_tip()

    # slides positions
    # pipette.move_to(chacha_labware['D2'].top())
    # pipette.move_to(chacha_labware['F2'].top())
    # pipette.move_to(chacha_labware['D3'].top())
    # pipette.move_to(chacha_labware['F3'].top())
    # protocol.delay(seconds=5)


    pipette.move_to(chacha_labware['A6'].top(20))
    pipette.move_to(chacha_labware['A6'].top(-10), speed=150)
    protocol.pause()
    pipette.move_to(chacha_labware['A6'].top(-5))
    protocol.pause()
    pipette.move_to(chacha_labware['A6'].top(-10), speed=150)
    protocol.pause()




    protocol.delay(seconds=5)

    pipette.move_to(chacha_labware['L6'].top(20))
    pipette.move_to(chacha_labware['L6'].top(5), speed=150)
    pipette.move_to(chacha_labware['O6'].top(5), speed=150)
    pipette.move_to(chacha_labware['O6'].top(-1), speed=100)
    pipette.return_tip()
