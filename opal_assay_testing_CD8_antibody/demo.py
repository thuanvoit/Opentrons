from opentrons import protocol_api
from opentrons.commands.protocol_commands import delay

class Opentron_Chacha:
    
    def __init__(self, protocol, pipette, chacha_labware, slides_num, antibody_solution, blocking_position):
        self.protocol = protocol
        self.pipette = pipette
        self.chacha_labware = chacha_labware
        self.antibody_solution = antibody_solution
        self.blocking_position = blocking_position
        self.slides_num = slides_num

    def check_antibodies(self):
        count = 0
        for antibody in self.antibody_solution:
            if antibody != "empty":
                sol_labware = self.get_labware(antibody)
                position = self.get_position(antibody)
                self.pipette.move_to(sol_labware[position].top(20))
                
                self.comment(f"PLEASE CANCEL IF '{antibody}' IS NOT AT {sol_labware} '{position}' \nTASKS WILL RESUME IN 5 SECONDS")
                
                self.protocol.delay(seconds=5)
                count+=1
        self.protocol.comment(f"{count} ANTIBODIES DETECTED SUCESFULLY")
    
    def comment(self, msg):
        self.protocol.comment("--------------------------------------------------")
        self.protocol.comment(msg)
        self.protocol.comment("--------------------------------------------------")
        
    #wash stuff
    ## NEED TO BE REDESIGN FOR DIFFERENT TIPS
    def washing(self, wash_n_time):
        self.comment('DUMP EVERYTHING OUT =))')
        for i in range(wash_n_time):
            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-12), speed=150) #speed to not throw slides =))
            

            self.pipette.move_to(self.chacha_labware['L6'].top(20))
            self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)


            self.pipette.move_to(self.chacha_labware['A6'].top(20))
            self.pipette.move_to(self.chacha_labware['A6'].top(-5), speed=100)
            self.pipette.move_to(self.chacha_labware['A6'].top(-12), speed=150) #speed to not throw slides =))

            self.protocol.delay(seconds=5)

        self.pipette.move_to(self.chacha_labware['L6'].top(20))
        self.pipette.move_to(self.chacha_labware['L6'].top(-2), speed=50)

    def get_position(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            position = self.antibody_solution[antibody_type]['position']
            return position
        else:
            self.protocol.pause(f"ERROR: Something wrong with '{antibody_type}'")
            return None

    def get_volume(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            volume = self.antibody_solution[antibody_type]['volume']
            return volume
        else:
            self.protocol.pause(f"ERROR: Something wrong with '{antibody_type}'")
            return None

    def get_time(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            time = [self.antibody_solution[antibody_type]['time']['mins'], self.antibody_solution[antibody_type]['time']['sec']]
            return time
        else:
            self.protocol.pause(f"ERROR: Something wrong with '{antibody_type}'")
            return None
        
    def get_labware(self, antibody_type):
        if antibody_type in self.antibody_solution.keys():
            labware = self.antibody_solution[antibody_type]['labware']
            return labware
        else:
            self.protocol.pause(f"ERROR: '{antibody_type}' is not one of antibody_solution defined")
            return None
    
    def volume_used(self, antibody_type, volume_used):
        current_volume_used = self.antibody_solution[antibody_type]['used']
        current_volume_used += volume_used
        self.antibody_solution[antibody_type]['used'] = current_volume_used
    
    def volume_used_report(self):
        self.comment(f'TOTAL VOLUME REPORT')
        for antibody in self.antibody_solution:
            if antibody != "empty":
                solution = self.antibody_solution[antibody]
                volume_used = solution['used']
                self.protocol.comment(f'Total Volume {antibody} used is {volume_used}uL ~ {str(volume_used/1000)}mL')

    def mix_up_n_down(self, volume, location, n_time):
        self.comment('MIX UP & DOWN')
        for n in range(n_time):
            self.pipette.aspirate(volume, location)
            self.pipette.dispense(volume, location)
            self.pipette.blow_out(location)

    #blocking method
    def blocking(self, antibody_type):
        
        position = self.get_position(antibody_type)
        volume = self.get_volume(antibody_type)
        time = self.get_time(antibody_type)

        sol_labware = self.get_labware(antibody_type)
        
        max_vol_aspirate = self.pipette.max_volume
        volume_to_do = 0
        

        while (volume > 0):

            if (volume > max_vol_aspirate):
                volume_to_do = max_vol_aspirate
            else:
                volume_to_do = volume
            
            self.comment(f'BLOCK WITH {volume_to_do} uL {antibody_type} FROM {sol_labware} - {position}')

            for i in range(self.slides_num):
                self.mix_up_n_down(max_vol_aspirate, sol_labware[position], 3)
                self.pipette.aspirate(volume_to_do, sol_labware[position])
                self.volume_used(antibody_type, volume_to_do)

                self.pipette.move_to(sol_labware[position].top(20), speed=50) # move slowly up

                for col in self.blocking_position[f'slide{i+1}']['cols']:
                    for row in self.blocking_position[f'slide{i+1}']['rows']:
                        self.pipette.dispense(volume_to_do/4, location=self.chacha_labware[row+col].top(5))

                #
                last_row_pos = self.blocking_position[f'slide{i+1}']['rows'][-1]
                last_col_pos = self.blocking_position[f'slide{i+1}']['cols'][-1]
                last_drop_position = self.chacha_labware[last_row_pos+last_col_pos]
                while (self.pipette.current_volume > 0):
                    self.pipette.dispense(self.pipette.current_volume, location=last_drop_position.top(5))
                self.pipette.blow_out(location=last_drop_position.top(5))
                #
            
            volume -= volume_to_do
            
        delay_min = time[0]
        delay_sec = time[1]
        
        self.comment(f'DELAY {delay_min} min, {delay_sec} sec')
        self.pipette.home()
        self.protocol.delay(minutes=delay_min, seconds=delay_sec)
        

    ### NEW RINSING
    def rinsing_with(self, antibody_type, n_time, n_each, delay_min_in_btw, delay_sec_in_btw):
        
        position = self.get_position(antibody_type)

        sol_labware = self.get_labware(antibody_type)
        
        self.pipette.pick_up_tip()
        
        for n in range(n_time):
            self.comment(f'WASH WITH {antibody_type} {n+1} time')
            # Washing TBST 4 times (30 seconds * 4 = 2 mins)
            for j in range(n_each):
                
                volume = self.get_volume(antibody_type)

                max_vol_aspirate = self.pipette.max_volume

                volume_to_do = 0

                while (volume > 0):

                    if (volume > max_vol_aspirate):
                        volume_to_do = max_vol_aspirate
                    else:
                        volume_to_do = volume

                    for i in range(self.slides_num):
                        
                        self.mix_up_n_down(max_vol_aspirate, sol_labware[position], 3)
                        self.pipette.aspirate(volume_to_do, sol_labware[position])
                        self.volume_used(antibody_type, volume_to_do)
                        
                        self.pipette.move_to(sol_labware[position].top(20), speed=50) # move slowly up

                        for col in self.blocking_position[f'slide{i+1}']['cols']:
                            for row in self.blocking_position[f'slide{i+1}']['rows']:
                                self.pipette.dispense(volume_to_do/4, location=self.chacha_labware[row+col].top(5))

                        #
                        last_row_pos = self.blocking_position[f'slide{i+1}']['rows'][-1]
                        last_col_pos = self.blocking_position[f'slide{i+1}']['cols'][-1]
                        last_drop_position = self.chacha_labware[last_row_pos+last_col_pos]
                        
                        while (self.pipette.current_volume > 0):
                            self.pipette.dispense(self.pipette.current_volume, location=last_drop_position.top(5))
                        self.pipette.blow_out(location=last_drop_position.top(5))
                        #
                    
                    volume -= volume_to_do

                    
                self.comment(f'DELAY {delay_min_in_btw} min, {delay_sec_in_btw} sec')
                self.pipette.home()
                self.protocol.delay(minutes=delay_min_in_btw, seconds=delay_sec_in_btw)
                self.washing(1)
                
            self.washing(3)
        
        # Remove OLD Tip
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
    
    # INTRODUCE BLOCKING POSITION

    #chacha1
    chacha1 = {"location": 2,
                "slide_number": 4, 
                "blocking_position": {
                    'slide1': { 'cols': ['2', '3'], # KEEP CONSTANT
                                'rows': ['D', 'F'], # OR
                                },
                    'slide2': { 'cols': ['9', '10'], # KEEP CONSTANT
                                'rows': ['F', 'H'], # OR
                                },
                    'slide3': { 'cols': ['16', '17'], # KEEP CONSTANT
                                'rows': ['F', 'H'], # OR
                                },
                    'slide4': { 'cols': ['23', '24'], # KEEP CONSTANT
                                'rows': ['F', 'H'], # OR
                                        #['B', 'C'],
                                        #['F', 'G'],
                                },
                    }
                }

    # labwares
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', location='1')
    chacha_labware = protocol.load_labware('corning_384_wellplate_112ul_flat', location=chacha1["location"])
    tuberack_15 = protocol.load_labware('opentrons_15_tuberack_falcon_15ml_conical', location='7')
    tuberack_15_50 = protocol.load_labware('opentrons_10_tuberack_falcon_4x50ml_6x15ml_conical', location='8')
        

    #tube introduce for opentrons_15_tuberack_falcon_15ml_conical
    antibody_solution = {
        # --- 1ST ROW ---
        'opal_antibody_dilluent': {'labware': tuberack_15, 'position': 'A1', 'volume': 400, 'time': {"mins": 10, "sec": 0}, 'used':0},
        'cd8_antibody': {'labware': tuberack_15, 'position': 'A2', 'volume': 400, 'time': {"mins": 30, "sec": 0}, 'used':0},
        'opal_polymer_HRP': {'labware': tuberack_15, 'position': 'A3', 'volume': 400, 'time': {"mins": 10, "sec": 0}, 'used':0},
        'opal_fluorophore': {'labware': tuberack_15, 'position': 'A4', 'volume': 400, 'time': {"mins": 10, "sec": 0}, 'used':0},

        # --- 2ND ROW ---
        #'ar6_buffer': {'labware': tuberack_15, 'position': 'B1', 'volume': 400, 'time': {"mins": 0, "sec": 5}, 'used':0},
        'dapi': {'labware': tuberack_15, 'position': 'B2', 'volume': 400, 'time': {"mins": 5, "sec": 0}, 'used':0},
        'h2o': {'labware': tuberack_15, 'position': 'B3', 'volume': 400, 'time': {"mins": 2, "sec": 0}, 'used':0},
        'tbst1': {'labware': tuberack_15_50, 'position': 'A3', 'volume': 400, 'time': {"mins": 1, "sec": 0}, 'used':0},
        'tbst2': {'labware': tuberack_15_50, 'position': 'A4', 'volume': 400, 'time': {"mins": 1, "sec": 0}, 'used':0},
        'empty': {'labware': 'empty', 'position': 'B5', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},

        # --- 3RD ROW ---
        'empty': {'labware': 'empty', 'position': 'C1', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},
        'empty': {'labware': 'empty', 'position': 'C2', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},
        'empty': {'labware': 'empty', 'position': 'C3', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},
        'empty': {'labware': 'empty', 'position': 'C4', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},
        'empty': {'labware': 'empty', 'position': 'C5', 'volume': 0, 'time': {"mins": 0, "sec": 0}, 'used':0},
    }

    

    #pipettes
    pipette = protocol.load_instrument('p300_single', 'left', tip_racks=[tiprack])

    ######## START ####################################################

    #command

    chacha = Opentron_Chacha(protocol, pipette, chacha_labware, chacha1['slide_number'], antibody_solution, chacha1['blocking_position'])

    chacha.check_antibodies()

    chacha.comment('TASKS START AFTER 5 SECONDS')
    protocol.delay(minutes=0, seconds=5)

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
    #TBST
    chacha.rinsing_with(antibody_type='tbst1', n_time=5, n_each=2, delay_min_in_btw=1, delay_sec_in_btw=0)

    ###################################################################
    ######## SECONDARY HRP ############################################
    ###################################################################

    pipette.pick_up_tip()
    chacha.blocking('opal_polymer_HRP')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()  
    #TBST
    chacha.rinsing_with(antibody_type='tbst1', n_time=5, n_each=2, delay_min_in_btw=1, delay_sec_in_btw=0)

    ###################################################################
    ######## OPAL FLUOROPHORE #########################################
    ###################################################################

    pipette.pick_up_tip()
    chacha.blocking('opal_fluorophore')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()
    #TBST
    chacha.rinsing_with(antibody_type='tbst2', n_time=5, n_each=2, delay_min_in_btw=1, delay_sec_in_btw=0)
    

    ######## SKIP AR6 BUFFER #########################################
    ######## AR6 BUFFER ##############################################

    # pipette.pick_up_tip()
    # chacha.blocking('ar6_buffer')
    # chacha.washing(wash_n_time=3)
    # pipette.drop_tip()

    ######## DAPI ####################################################
    ## PAUSE PROGRAM BEFORE DAPI ##

    protocol.pause(f"PUT DAPI INTO {antibody_solution['dapi']['labware']} - {antibody_solution['dapi']['position']}")

    pipette.pick_up_tip()
    chacha.blocking('dapi')
    chacha.washing(wash_n_time=3)
    pipette.drop_tip()

    #TBST
    chacha.rinsing_with(antibody_type='tbst2', n_time=2, n_each=1, delay_min_in_btw=2, delay_sec_in_btw=0)
    chacha.rinsing_with(antibody_type='h2o', n_time=2, n_each=1, delay_min_in_btw=2, delay_sec_in_btw=0)

    ######## END #####################################################

    chacha.volume_used_report()