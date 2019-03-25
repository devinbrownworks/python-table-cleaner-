import csv 
import usaddress
import scourgify
from pycountry import countries
import re
import copy
from typing import Tuple, Dict, List

country_re = re.compile('|'.join(c.name.upper() for c in countries))         
APN, CAREOF, DBA, STREET, CITY, STATE, ZIP, ADDRESS1, ADDRESS2, ADDRESS3, ADDRESS4, REFINEINFO = (0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15 )

def getLabelsRecords(filename):
    with open(filename) as f:
        table = [ r for r in csv.reader(f) ]
        for r in table:
            r.append( '' )
        return ( table[0], table[1:] )

def usAddressGet( usadd: List[ Tuple[ str, str ] ], addType: str ) -> bool:
    matchedAddType = ''
    for pair in usadd:
        if pair[1] == addType:
            matchedAddType += pair[0]
    if matchedAddType:
        return matchedAddType
    return False 

def refine( record: List[ str ] ):
    filtered = False 
    usadd = usaddress.parse( formattedColumns( record ) )
    #if the address is foreign do nothing 
    if not usAddressGet( usadd, 'ZipCode') and record[STATE] == '':
        return filtered
    filtered = refinePO( record )
    filtered |= refineCityStateZip( record, usadd )
    filtered |= refineStreet( record )
    filtered |= refineRecipient( record, usadd )
    if hasNullAddressVal( record ) and hasFormattedVal( record ):
        record[REFINEINFO] += ' NULLVALUES'
        filtered = True  
    return filtered

def refinePO( record ):
    for col in record[ ADDRESS1 : ADDRESS4 + 1 ]:
        if record[STREET] == '' and 'PO BOX' in col:
            record[REFINEINFO] += ' PO'
            record[STREET] = record[ADDRESS3]        
            return True 
    return False 

def refineCityStateZip( record, usadd ):
    city, state, zipcode = ( usAddressGet( usadd, 'PlaceName' ), usAddressGet( usadd, 'StateName' ),
                             usAddressGet( usadd, 'ZipCode' ) )
    filtered = False 
    if city and record[CITY] == '':
        record[REFINEINFO] += ' CITY'
        record[CITY] = city
        filtered = True 
    if state and record[STATE] == '':
        record[REFINEINFO] += ' STATE'        
        record[STATE] = state
        filtered = True 
    if zipcode and record[ZIP] == '':
        record[REFINEINFO] += ' ZIPCODE'
        record[ZIP] = zipcode
        filtered = True
    return filtered

def refineStreet( record ):
    for i in range( ADDRESS1, ADDRESS4 + 1 ):
        try:
            street = scourgify.normalize_address_record( record[i] )['address_line_1'] 
            if record[STREET] == '':
                record[REFINEINFO] += ' STREET'
                record[STREET] = street 
                return True 
        except:
            pass
    return False

def refineRecipient( record, recipient ):
    filtered = False
    recipRecord = getRecipient( recipient )
    if recipRecord:
        if recipRecord[0] == 'DBA' and record[DBA] == '':
            record[DBA] = ' '.join( recipRecord )
            record[REFINEINFO] += ' DBA'
            filtered = True 
        elif recipRecord[0] == 'C/O' and record[CAREOF] == '':
            record[CAREOF] = ' '.join( recipRecord )
            record[REFINEINFO] += ' C/O'
            filtered = True 
    
    return filtered


def formattedColumns( record ):
    return  ( record[ADDRESS1] + ' ' + record[ADDRESS2] + ' ' + 
                record[ADDRESS3] + ' ' + record[ADDRESS4] )


def getRecipient( recipient ):
        filterRecip = filter( lambda record: record[1] == 'Recipient', recipient )
        return [ recipient[0] for recipient in filterRecip ]

def hasNullAddressVal( record ):
    return ( record[CITY] == '' or record[STATE] == '' or
             record[STREET] == '' or record[ZIP] == '')

def hasFormattedVal( record ):
    return ( record[ADDRESS1] != '' and record[ADDRESS2] != '' and 
             record[ADDRESS3] != '' and record[ADDRESS4] )

''' 
    updatedRecords.sort( )
    preUpdateRecords.sort( )
    updatedRecords = labels + updatedRecords
    preUpdateRecords = labels + preUpdateRecords
   
    import sys
    aw = csv.writer( sys.stdout, dialect='excel' )
    for r in records:
            if ( r[REFINEINFO] == 'C/O' or r[REFINEINFO] == 'DBA' ):
                aw.writerow( r )
'''


'''
with open( 'interestingbits','w') as f:
        for r in records:
            if ( r[REFINEINFO] == 'NULLVALUES' or  r[REFINEINFO] == 'C/O' or 
                 r[REFINEINFO] == 'DBA' or  r[REFINEINFO] == 'FOREGIN' ):
                
                f.write(
                    ( l[3] + '-->' + printR(r[3]) + ' : ' +l[4] + '-->' + printR(r[4]) + '\n'
                    + l[5] + '-->' + printR(r[5]) ) 
                    )
                f.write(
                    ( l[6] + '-->' + printR(r[6]) + ' : ' + l[7] + '-->' + printR(r[7]) + '\n'
                    + l[8] + '-->' + printR(r[8]) + ' : ' + l[9] + '-->' + printR(r[9]) )
                    )
                f.write(
                    ('#####################################')
                    )
                f.write(
                    ( l[10] + '-->' + printR(r[10]) + ' : ' + l[11] + '-->' + printR(r[11]) )
                    )
                f.write(
                    ( l[12] + '-->' + printR(r[12]) + ' : ' + l[13] + '--> ' +printR(r[13]) )
                    )



    co = [ r for r in records if r[REFINEINFO] == 'C/O' ]
    dba = [ r for r in records if r[REFINEINFO] == 'DBA' ]
    foreign = [ r for r in records if r[REFINEINFO] == 'FOREIGN']
    nullvalues = [ r for r in records if r[REFINEINFO] == 'NULLVALUES']
    failedparse = [ r for r in records if r[REFINEINFO] == 'FAILEDPARSE']
'''
