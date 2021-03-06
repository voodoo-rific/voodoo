

import random

class TimeSlotGenerator(object):

    def __init__(self, hours, slots= None):
        self.hours = hours
        self.number_gen = {
            1 : 15,
            2 : 30,
            3 : 45,
            4 : 60,
        }

        # we pass in a list of times for easier testing
        # SHOULD : assert that the total equals self.hours
        if slots:
            self.time_slots = slots
        else:
            self.time_slots = self._get_time_slots(self.hours)


    def _get_time_slots(self, hours):

        in_minutes = hours*60
        total = 0
        slots = []


        # was the last slot a 15 or not
        coming_off_break = False
       
        # once we get to 90, default to break 
        time_without_break = 0



        while total <= in_minutes:
            if total == in_minutes:
                break


            # we are coming off a 15 min break
            if coming_off_break:            
                to_add = random.randint(2, 4)
            
            # we have worked to hard and deserve a break
            elif time_without_break >= 90:
                to_add = 1
                time_without_break = 0

            # not coming off a break
            else:
                to_add = random.randint(1, 4)
                
            
            minute_section = self.number_gen[to_add]
            
            if minute_section == 15:
                coming_off_break = True
            else:
                coming_off_break = False
            
            
            total = total + minute_section
            time_without_break = time_without_break + minute_section


            slots.append(minute_section)

        

        # we have gone over our total
        if total > in_minutes:

            #get the last item in the list
            last_item = slots[-1]


            #subtract it from the total
            total = total - last_item

            #figure out the correct segment to add
            #to get us to the total


            # MAY : further subdivide later
            to_add = in_minutes - total


            ## Need to do some logic in here that will deal
            # with ending 2 breaks in a row 

            # replace the last number if we
            # need to add a final slot
            if to_add != 0:
                slots[-1] = to_add

            # remove the last number if already
            # all slots filled
            else:
                slots = slots[:-1]

        return slots


