# Ansel Hartanto code for parsing txt file for stack differential



def main():
    #read file
    sourcefile = open("startelFile.txt", "r")
    linesinfile = sourcefile.readlines()
    sourcefile.close()

    #contextual calcualtion of text parsing
    s = []  #stack of ints indicating which time, global var
    str_stack = [] #stack for indicating which function
    int_delaystack = []

    result_stack = []
    int_resultstack = []
    times_called = []


    for line in linesinfile:
        line = line.strip();
        words = line.split(" ")
        if "Enter" in line and words[2] not in result_stack:
            s.append(words[0]) #store the time of execution in stack
            str_stack.append(words[2]) #store function identifier
            times_called.append(1)
        elif "Enter" in line:
            s.append(words[0])
            str_stack.append(words[2]) #hmm
            index = result_stack.index(words[2])
            times_called[index] += 1 #tick up times_called for specific function ALREADY SEEN
        elif "Exit" in line:
            x = s.pop() #time int
            y = str_stack.pop() #function identifier
            result = int(words[0]) - int(x)

            if len(int_delaystack) != 0: #still more functions to finish executing
                f_delay = int_delaystack.pop()
                int_delaystack.append(result)
                result -= f_delay        #additional substraction
            elif len(int_delaystack) == 0:
                int_delaystack.append(result)



            #elif len(int_delaystack) == 0 and y in result_stack:
                #index_2 = result_stack.index(y)
                #int_resultstack[index_2] += result

            if y not in result_stack:
                int_resultstack.append(result) #save duration
                result_stack.append(y) #save identifier
        else:
            continue

    itemcount = len(times_called)
    print (result_stack)
    print(len(int_resultstack))
    print(len(times_called))

    while(itemcount != 0):
        w = result_stack.pop()
        t = int_resultstack.pop()
        c = times_called.pop()
        print (str(w)," is called ",str(c)," times for a total duration of ",str(t), "seconds")
        print ("hello")
        itemcount -= 1


main()
