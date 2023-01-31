q=[{"Home":[["Sudhanwa","Milind","Bokade"],["Smaran","Bora","Murli"]],
    "Work":[["Do","The","Job"],["Hello","Hi","BYe"]]}]

for dict in q:
    for heading in dict.keys():
        print("Type: ",heading)  #Printing the title of each scrollable list
        for outer in dict.get(heading):
            print(outer)
            for content in outer:
                print(content)
            
    
        