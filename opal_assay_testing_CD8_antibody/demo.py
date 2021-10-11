from opentrons import protocol_api
import chacha_cmd as chachacmd

#meta
metadata = {
    'protocolName': 'Opal Assay Testing CD8 Antibody',
    'author': 'thuanvo',
    'description': 'Demo version',
    'apiLevel': '2.10'
}
    #   RECOMMENDED AREA
    #  ___________________
    # |                   |
    # |      A            |
    # |   ___________     |
    # |  |   B       |    |
    # |  |   C       | OR |  <==  B and C
    # |  |-----------|    |
    # |  |   D       |    |
    # |  |   E       | OR |  <==  D and E
    # |  |-----------|    |
    # |  |   F       |    |
    # |  |   G       | OR |  <==  F and G
    # |  |___________|    |
    # |      H            |
    # |      I            |
    # |      J            |
    # |      K            |
    # |      L            |
    # |      M            |
    # |      N            |
    # |      O            |
    # |      P            |
    # |___________________|
    # |###################|
    # |##### SLIDE #######|
    # |___________________|

# INTRODUCE BLOCKING POSITION
blocking_position = {
    'slide1': { 'cols': ['2', '3'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                
                },
    'slide2': { 'cols': ['9', '10'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    'slide3': { 'cols': ['16', '17'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    'slide4': { 'cols': ['23', '24'], # KEEP CONSTANT
                'rows': ['D', 'E'], # OR
                        #['B', 'C'],
                        #['F', 'G'],
                },
    }


def run(protocol: protocol_api.ProtocolContext):
    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha = protocol.load_labware('corning_384_wellplate_112ul_flat', location='2')
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    #tube introduce
    # Opal Antibody Dilluent at Tuberack A1
    opal_antibody_dilluent = tuberack['A1']
    cd8_antibody = tuberack['A2']

    #command

    ###################################################################
    ######## BLOCKING using Opal Antibody Dilluent ####################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING
    volume_per_slide = 300
    for i in range(3):
        chachacmd.chacha_blocking(protocol, pipette, chacha, opal_antibody_dilluent, volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    protocol.delay(minutes=10)
    
    # Drain Blocking Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()
    
    ###################################################################
    ######## PRIMARY ANTIBODY INCUBATION ##############################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING PRIMARY ANTIBODY INCUBATION
    volume_per_slide = 300
    for i in range(3):
        chachacmd.chacha_blocking(protocol, pipette, chacha, opal_antibody_dilluent, volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 30 mins incubate
    protocol.delay(minutes=30)
    
    # Drain Blocking Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()
    



