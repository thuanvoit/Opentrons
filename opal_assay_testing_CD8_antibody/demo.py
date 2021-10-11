from opentrons import protocol_api
from opentrons.commands.protocol_commands import delay
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
slides_number = 4

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

    #tube introduce for opentrons_15_tuberack_falcon_15ml_conical
    antibody_solution = {
        # --- 1ST ROW ---
        'opal_antibody_dilluent': 'A1',
        'cd8_antibody': 'A2',
        'tbst': 'A3',
        'opal_polymer_HRP': 'A4',
        'opal_fluorophore': 'A5',
        # --- 2ND ROW ---
        'ar6_buffer': 'B1',
        '': 'B2',
        '': 'B3',
        '': 'B4',
        '': 'B5',
        # --- 3RD ROW ---
        '': 'C1',
        '': 'C2',
        '': 'C3',
        '': 'C4',
        '': 'C5',

    }

    #command

    ###################################################################
    ######## BLOCKING using Opal Antibody Dilluent ####################
    ###################################################################
    pipette.pick_up_tip()
    
    # BLOCKING
    volume_per_slide = 300
    for i in range(slides_number):
        chachacmd.chacha_blocking(protocol, pipette, chacha, 
                                    antibody_solution['opal_antibody_dilluent'], 
                                    volume_per_slide, 
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
    for i in range(slides_number):
        chachacmd.chacha_blocking(protocol, pipette, chacha, 
                                    antibody_solution['cd8_antibody'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 30 mins incubate
    protocol.delay(minutes=30)
    
    # Drain Blocking Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chachacmd.rinsing_with_tbst(protocol, pipette, chacha, slides_number, blocking_position, antibody_solution)

    ###################################################################
    ######## SECONDARY HRP ############################################
    ###################################################################
    pipette.pick_up_tip()

    # Aspirate HRP
    volume_per_slide = 300
    for i in range(slides_number):
        chachacmd.chacha_blocking(protocol, pipette, chacha, 
                                    antibody_solution['opal_polymer_HRP'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    protocol.delay(minutes=10)
    
    # Drain Blocking Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chachacmd.rinsing_with_tbst(protocol, pipette, chacha, slides_number, blocking_position, antibody_solution)


    ###################################################################
    ######## OPAL FLUOROPHORE #########################################
    ###################################################################
    pipette.pick_up_tip()

    # Aspirate HRP
    volume_per_slide = 300
    for i in range(slides_number):
        chachacmd.chacha_blocking(protocol, pipette, chacha, 
                                    antibody_solution['opal_fluorophore'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    protocol.delay(minutes=10)
    
    # Drain HRP Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)

    # Remove the tip
    pipette.drop_tip()

    chachacmd.rinsing_with_tbst(protocol, pipette, chacha, slides_number, blocking_position, antibody_solution)

    ######## AR6 BUFFER ##############################################

    volume_per_slide = 300
    for i in range(slides_number):
        chachacmd.chacha_blocking(protocol, pipette, chacha, 
                                    antibody_solution['ar6_buffer'], 
                                    volume_per_slide, 
                                    blocking_position[f'slide{i+1}']['cols'], 
                                    blocking_position[f'slide{i+1}']['rows'])
    # 10 mins incubate
    protocol.delay(seconds=5)

    # Drain AR6 Buffer
    chachacmd.chacha_washing(protocol, pipette, chacha, wash_n_time=3)




    



