from opentrons import protocol_api
from opentrons.commands.protocol_commands import delay

class Opentron_Chacha:
    def __init__(self, protocol, pipette, chacha_labware, slides_num, tuberack, antibody_solution, blocking_position):
        self.protocol = protocol
        self.pipette = pipette
        self.chacha_labware = chacha_labware
        self.tuberack = tuberack
        self.antibody_solution = antibody_solution
        self.blocking_position = blocking_position
        self.slides_num = slides_num

    def check_antibodies(self):
        count = 0
        for antibody in self.antibody_solution:
            if antibody != "empty":
                self.pipette.move_to(self.chacha_labware[self.antibody_solution[antibody]['position']].top(20))
                self.protocol.comment('-------- WARNING ---------------------------------')
                self.protocol.comment(f"PLEASE CANCEL IF '{antibody}' IS NOT AT TUBERACK '{self.antibody_solution[antibody]['position']}'")
                self.protocol.comment(f"TASKS WILL RESUME IN 5 SECONDS")
                self.protocol.comment('--------------------------------------------------')
                self.protocol.delay(seconds=5)
                count+=1
        self.protocol.comment(f"{count} ANTIBODIES DETECTED SUCESFULLY")
        
        
    #wash stuff
    def washing(self, wash_n_time):
        for i in range(wash_n_time):
            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-13))
            

            self.pipette.move_to(self.chacha_labware['L6'].top(20))
            self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)


            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-13))

            self.protocol.delay(seconds=5)

        self.pipette.move_to(self.chacha_labware['L6'].top(20))
        self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)



    def antibody_info(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            position = self.antibody_solution[antibody_type]['position']
            volume = self.antibody_solution[antibody_type]['volume']
            time = [self.antibody_solution[antibody_type]['time']['mins'], self.antibody_solution[antibody_type]['time']['sec']]
            return [position, volume, time]
        else:
            self.protocol.pause(f"ERROR: '{antibody_type}' is not one of antibody_solution defined")
            return None

    #blocking method
    def blocking(self, antibody_type):
        for i in range(self.slides_num):
            info = self.antibody_info(antibody_type)
            self.pipette.aspirate(info[1], self.tuberack[info[0]])
            for col in self.blocking_position[f'slide{i+1}']['cols']:
                for row in self.blocking_position[f'slide{i+1}']['rows']:
                    self.pipette.dispense(info[1]/4, location=self.chacha_labware[row+col].top())

            #
            while (self.pipette.current_volume > 0):
                self.pipette.dispense(self.pipette.current_volume, location=self.chacha_labware[self.blocking_position[f'slide{i+1}']['rows'][-1]+self.blocking_position[f'slide{i+1}']['cols'][-1]].top())
            self.pipette.blow_out(location=self.chacha_labware[self.blocking_position[f'slide{i+1}']['rows'][-1]+self.blocking_position[f'slide{i+1}']['cols'][-1]].top())
            #

        self.protocol.delay(minutes=info[2][0], seconds=info[2][1])
        

    # TBST RINSING
    def rinsing_with_tbst(self, antibody_type, n_time):
        info = self.antibody_info(antibody_type)
        self.pipette.pick_up_tip()

        for n in range(n_time):
            # Washing TBST 6 times (30 seconds * 6 = 2 mins)
            for j in range(6):
                for i in range(self.slides_num):
                    self.blocking(antibody_type)
                self.protocol.delay(minutes=info[2][0], seconds=info[2][1])
            self.washing(3)
        
        #Remove OLD Tip
        self.pipette.drop_tip()
        ######## REMOVE TBST #########################

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


def run(protocol: protocol_api.ProtocolContext):
    
    #tube introduce for opentrons_15_tuberack_falcon_15ml_conical
    antibody_solution = {
        # --- 1ST ROW ---
        'opal_antibody_dilluent': {'position': 'A1', 'volume': 300, 'time': {"mins": 30, "sec": 0}},
        'cd8_antibody': {'position': 'A2', 'volume': 300, 'time': {"mins": 30, "sec": 0}},
        'tbst': {'position': 'A3', 'volume': 200, 'time': {"mins": 0, "sec": 30}},
        'opal_polymer_HRP': {'position': 'A4', 'volume': 300, 'time': {"mins": 10, "sec": 0}},
        'opal_fluorophore': {'position': 'A5', 'volume': 300, 'time': {"mins": 10, "sec": 0}},
        
        # --- 2ND ROW ---
        'ar6_buffer': {'position': 'B1', 'volume': 300, 'time': {"mins": 0, "sec": 5}},
        'empty': {'position': 'B2', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B3', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B4', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'B5', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        
        # --- 3RD ROW ---
        'empty': {'position': 'C1', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C2', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C3', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C4', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
        'empty': {'position': 'C5', 'volume': 0, 'time': {"mins": 0, "sec": 0}},
    }

    # INTRODUCE BLOCKING POSITION

    #chacha1
    chacha1 = {"location": 2,
                "slide_number": 4, 
                "blocking_position": {
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
                }

    #labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha_labware = protocol.load_labware('corning_384_wellplate_112ul_flat', location=chacha1["location"])
    tuberack = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    
    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    ######## START ####################################################

    #command

    chacha = Opentron_Chacha(protocol, pipette, chacha_labware, chacha1['slide_number'], tuberack, antibody_solution, chacha1['blocking_position'])

    chacha.check_antibodies()

    ###################################################################
    ######## BLOCKING using Opal Antibody Dilluent ####################
    ###################################################################

    pipette.pick_up_tip()
    chacha.blocking('opal_antibody_dilluent')
    chacha.washing(3)
    pipette.drop_tip()
    
    ###################################################################
    ######## PRIMARY ANTIBODY INCUBATION ##############################
    ###################################################################

    pipette.pick_up_tip()
    chacha.blocking('cd8_antibody')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()
    chacha.rinsing_with_tbst('tbst', 5)

    ###################################################################
    ######## SECONDARY HRP ############################################
    ###################################################################

    pipette.pick_up_tip()
    chacha.blocking('opal_polymer_HRP')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()
    chacha.rinsing_with_tbst('tbst', 5)

    ###################################################################
    ######## OPAL FLUOROPHORE #########################################
    ###################################################################
    
    pipette.pick_up_tip()
    chacha.blocking('opal_fluorophore')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()
    chacha.rinsing_with_tbst('tbst', 5)

    ######## AR6 BUFFER ##############################################

    pipette.pick_up_tip()
    chacha.blocking('ar6_buffer')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()

    ######## END #####################################################
