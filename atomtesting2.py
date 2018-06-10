# Ansel Hartanto code for parsing txt file for call stack management and reporting
from decimal import *

def main():
    #read file
    sourcefile = open("test6.txt", "r")  #change this to the file names of the other files I am sending you (range from 0 to 6)
    linesinfile = sourcefile.readlines()
    sourcefile.close()

    #APPROACH: USE A CALL STACK SYSTEM TO ALLOCATE WHAT'S DONE AND WHAT'S NOT
    call_stack = [] #call stack
    done_stack = [] #finished function execution stack
    level = 0

    result_stack = []  #stack for output, MAY CONTAIN REPEATED IDENTIFIERS
    finish_stack = []  #stack for output, CONTAINS UNIQUE IDENTIFIERS
    for line in linesinfile:
        line = line.strip();
        words = line.split(" ")
        #time, action, identifier = words
        if len(words) != 3 : #more than 3 words, ignore and continue INVALID line
            print('Incorrect validity of input, line ignored or assumed to not be enter/exit action!')
            continue
        time = words[0]
        action = words[1]
        identifier = words[2]
        if action == 'Enter':
            level += 1 #check "how DEEP I AM IN THE CODE NESTING"
            call_stack.append((time, identifier)) #call stack allows duplicates

        elif action == 'Exit':
            item = call_stack.pop()
            x = item[0] #time of start
            y = item[1] #identifier
            cumulative_time = 0

            if len(done_stack) != 0:
                length = len(done_stack) - 1
                top_of_done = done_stack[length]
                level_of_top = top_of_done[2]

                if level < level_of_top:    #substract done_stack acc values only if curr level is lower than prev stores level
                    for doneitems in done_stack:
                        if doneitems[2] > level: #only substract from items in "deeper" level than where you are currently, this is workaround to consider nesting behaviour
                            cumulative_time += doneitems[0]  #subctract done_stack accumulation values

        # subtract sum of current done_stack runtimes and add to done stack with time
            try:
                net_time = Decimal(time) - Decimal(cumulative_time) - Decimal(x)
            except ValueError:
                print("input not allowed! Line", words, "ignored")
                continue;
            temp_level_identifier = level
            level -= 1
            done_stack.append((net_time, identifier, temp_level_identifier)) #allows duplicates of identifiers
            if len(call_stack) == 0: #flush done_stck to result if no more calls to do on call stack
                for item in done_stack:
                    result_stack.append(item)
                del done_stack[:]



    # FINISHING UP, CLEANING UP, AND PACKAGING INFORMATION FOR DISPLAY OF REPORTS
    tempstackof_identifier = []
    tempstackof_duration = []
    tempstackof_count = []
    if len(result_stack) > 0:

        firstitem = result_stack.pop()

        finish_stack.append(firstitem) # list of list of entries
        tempstackof_identifier.append(firstitem[1]) # only FUNCTION IDENIFIERS
        tempstackof_duration.append(firstitem[0]) #only FUNCTION DURATIONS
        tempstackof_count.append(1)

        while result_stack: #while list of result is not empty
            item = result_stack.pop()
            if item[1] not in tempstackof_identifier:
                finish_stack.append(item)
                tempstackof_identifier.append(item[1])
                tempstackof_duration.append(item[0])
                tempstackof_count.append(1)
            else: #already seen the identifier
                index = tempstackof_identifier.index(item[1])
                tempstackof_duration[index] += item[0] #accumulate already seen functions
                tempstackof_count[index] += 1

    for i in range(0, len(tempstackof_count)):
        id = tempstackof_identifier[i]
        count = tempstackof_count[i]
        duration = tempstackof_duration[i]
        #print("Function %s is called %i times for a total duration of" % (id, count), str(duration),"seconds" )
        print("Function %s is called %i times for a total duration of" % (id, count), str(duration),"seconds" )





if __name__ == '__main__': #So script can be used as a module
    main()
