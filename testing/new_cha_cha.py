
# THIS IS A DEMO VERSION USING 1000uL
# * NEW CHACHA 
# * NEW TBST 
# * NEW TUBE HOLDER

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
    well = protocol.load_labware('kissicklabdesign_1_reservoir_100000ul', location='5')
    # tuberack_15 = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='6')
    # chacha_labware = protocol.load_labware('kissicklabdesign_384_wellplate_80ul', location='10')

    # PICK UP TIPS 1000
    pipette.pick_up_tip()
    
    # TEST THE TBST WELL
    pipette.move_to(well['A1'].top())
    pipette.move_to(well['A1'].bottom())

    # # PAUSE TO OBSERVE
    protocol.pause()

    # # TEST THE TUBRACK 15ML
    # pipette.move_to(tuberack_15['A1'].top())
    # pipette.move_to(tuberack_15['A1'].bottom())
    # protocol.pause()

    # pipette.move_to(tuberack_15['C2'].top())
    # pipette.move_to(tuberack_15['C2'].bottom())
    # # protocol.pause()

    # pipette.move_to(tuberack_15['B3'].top())
    # pipette.move_to(tuberack_15['B3'].bottom())
    # # protocol.pause()

    # pipette.move_to(tuberack_15['C4'].top())
    # pipette.move_to(tuberack_15['C4'].bottom())
    # # protocol.pause()

    # pipette.move_to(tuberack_15['A5'].top())
    # pipette.move_to(tuberack_15['A5'].bottom())
    # # protocol.pause()

    # for i in range(2):
    #     pipette.move_to(chacha_labware['A6'].top(20))
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['A6'].top(-4), speed=100)
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['A6'].top(-12), speed=150) #speed to not throw slides
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['L6'].top(20))
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['L6'].top(-1), speed=50)
    #     # protocol.pause()


    #     pipette.move_to(chacha_labware['A6'].top(20))
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['A6'].top(-4), speed=100)
    #     # protocol.pause()

    #     pipette.move_to(chacha_labware['A6'].top(-12), speed=150) #speed to not throw slides =))
    #     # protocol.pause()


    #     protocol.delay(seconds=5)

    # list_char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

    # for c in list_char:
    #     pipette.move_to(chacha_labware[c+str(1)].top(), speed=100)
    #     protocol.pause()
    # for i in range(24):
    #     pipette.move_to(chacha_labware['A'+str(i+1)].top(), speed=100)
    #     protocol.pause()

    #pipette.move_to(chacha_labware['L6'].top(20))
    #pipette.move_to(chacha_labware['L6'].top(-2), speed=50)

    # FINISH
    pipette.return_tip()
