#Program Written by Devin T. Brown
#Uses the following advanced natural language processing libraries: 
# https://github.com/datamade/usaddress , https://github.com/GreenBuildingRegistry/usaddress-scourgify 
# to parse PRMD table data and fill in void columns where existing data is already known for that row.
from tableToolz import *


    
   
def main():
    labels, records = getLabelsRecords('nameAddress.csv')
    oldRecords = copy.deepcopy( records )
    refined = sorted( [ r for r in filter( refine, records ) ] )    
    updatedRecords = open( 'updatedRecords.csv', 'w', newline = '' )
    preUpdatedRecords = open( 'preUpdatedRecords.csv', 'w', newline = '' )
    updatedRecordsCSVWriter  = csv.writer( updatedRecords, dialect='excel' )
    preUpdatedRecordsCSVWriter  = csv.writer(preUpdatedRecords, dialect='excel' )

    updatedRecordsCSVWriter.writerow( labels )        
    for r in refined:
        updatedRecordsCSVWriter.writerow( r[ : REFINEINFO ] )
    preUpdatedRecordsCSVWriter.writerow( labels )
    preUpdatedRecords.write( '\n' )
    for r in refined:
        for rec in oldRecords:
            if r[0] in rec[0]:
                preUpdatedRecords.write( 'Updates Made --> ' + r[REFINEINFO] + '\n' )
                preUpdatedRecordsCSVWriter.writerow( rec )
                break
    
    return                      
            
if __name__=="__main__":
    main()



