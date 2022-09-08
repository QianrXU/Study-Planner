#from app import db
#from app import pd
import pandas as pd
import os
import json

masterData=[]

#Send data to database
def data_to_database(file):
    data = pd.read_csv(file)
    data_shape= data.shape
    create_masterData(data_shape[0], data_shape[1], data)
    print(data)

#Generate array from csv file
def create_masterData(data_len, data_width, data):
    col_names = []
    i=0
    
    #Get list of columns
    for col in data.columns:
        col_names[i]=col
        i+=1        
    i=0

    while i < data_len:
        j=0
        major_array = []
        while j < data_width:
            #add data to masterData
            row_dict={}
            cell_value=data.iat[i,j]
            
            #if the column is Structure then break the data down further.
            if j==4:
                json_col= cell_value
                #convert json array to python array.
                structure_array= json.loads(cell_value)
                sub_array1 = structure_array[0]['levelsSpecials'][0]
                sub_array2= structure_array[0]['levelsSpecials'][1]
                sub_array3= structure_array[0]['levelsSpecials'][2]

                a=0
                for value in sub_array1:
                    #store data
                    if a==2:
                        #drill down further
                        num_units=len(value)
                        for unit in value:
                            #store data!                    
                    a+=1
                #split data in this column
            else:
                row_dict[col_names[j]]=cell_value
            j+=1    
        
        masterData[i]=row_dict
        i+=1

def json_array_breakdown(row_dict, json_cell):
    #convert json array to python array.
    structure_array= json.loads(cell_value)
    levels=structure_array[0]['levelsSpecials'][0]
    unit_dict={}

    for sub_array in levels:
        sub_type = sub_array[0]
        sub_points =sub_array[1]
        sub_units = sub_array[2]
        for units in sub_units:
            for unit_detail in units:
                unit_dict[unit_detail]: sub_units[unit_detail]
    #break down into levels
    sub_array1 = structure_array[0]['levelsSpecials'][0]
    sub1_type = sub_array1[0]
    sub1_points = sub_array1[1]
    sub1_units = sub_array1[2]

    sub_array2= structure_array[0]['levelsSpecials'][1]
    sub2_type = sub_array2[0]
    sub2_points= sub_array2[1]
    sub2_units = sub_array2[2]
    
    sub_array3= structure_array[0]['levelsSpecials'][2]
    sub3_type = sub_array3[0]
    sub3_points= sub_array3[1]
    sub3_units = sub_array3[2]

# parse files in csv folder and send them to the database
for dir_name, subdir_list, file_list in os.walk('./csv', topdown=True):
    for fname in file_list:
        if fname[-4:] == '.csv':
            print (fname)
            data_to_database('%s/%s' % (dir_name, fname))


"""

#HEADERS
ID,
CourseID,
Year,
Structure,#--> This category has many sub-Headings
    introduction,
    levelsSpecials,
        levelName: Level 1/2/3
            unit info
ListMajors,
ListMajors2,
ListPG,
AdmissionRequirements,
AdmissionRanking,
Title,
Faculty,
ROE,
Availability,
CommencementYear,
DeliveryMode,
DeliveryLocations,
IntakePeriods,
AttendanceType,
StandardFullTimeCompletion,
TimeLimit,
AvailableToInternationalStudents,
Accreditation,
HonoursOfferedInMajor,
MinATAR

#INPUT
3255,
MJD-ARCTR,
2018,
"[
    {""introduction"":"",
    ""levelsSpecials"":[
        {
            ""levelName"":""Level 1"",
            ""typeInto"":"",
            ""unitTypes"":[
                {
                    ""typeName"":""Core"",
                    ""typeInto"":""Take all units (12 points):"",
                    ""units"":[
                        {""unitCode"":""ARCT1001"",
                        ""unitTitle"":""Architecture Studio 1"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT1001""},
                        {""unitCode"":""ARCT1010"",
                        ""unitTitle"":""Drawing History"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT1010""}
                        ]
                },
                {
                    ""typeName"":""Complementary"",
                    ""typeInto"":""Take all complementary units (12 points):"",
                    ""units"":[
                        {""unitCode"":""HART1001"",
                        ""unitTitle"":""Art,
                        Technology and Society"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=HART1001""},
                        {""unitCode"":""IDES1040"",
                        ""unitTitle"":""Techniques of Visualisation"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=IDES1040""}]
                }
            ]
        },
        {
            ""levelName"":""Level 2"",
            ""typeInto"":"",
            ""unitTypes"":[
                {
                    ""typeName"":""Core"",
                    ""typeInto"":""Take all units from this group (18 points):"",
                    ""units"":[
                        {""unitCode"":""ARCT2000"",
                        ""unitTitle"":""Architecture Studio 2"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT2000""},
                        {""unitCode"":""ARCT2050"",
                        ""unitTitle"":""Environmental Design"",
                        ""unitPoints"":""6"",""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT2050""}
                    ]
                },
                {
                    ""typeName"":""Complementary"",
                    ""typeInto"":""Take all complementary units (6 points):"",
                    ""units"":[
                        {""unitCode"":""ARCT2010"",
                        ""unitTitle"":""Parallel Modernities in Art and Architecture"",
                        ""unitPoints"":""6"",
                        ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT2010""}
                    ]
                }
            ]
        },
        {
            ""levelName"":""Level 3"",
            ""typeInto"":"",
            ""unitTypes"":[
                {
                    ""typeName"":""Core"",
                    ""typeInto"":""Take all units (18 points):"",
                    ""units"":[
                        {
                            ""unitCode"":""ARCT3001"",
                            ""unitTitle"":""Architecture Studio 4"",
                            ""unitPoints"":""12"",
                            ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT3001""
                        },
                        {
                            ""unitCode"":""ARCT3010"",
                            ""unitTitle"":""History and Theories of the Built Environment"",
                            ""unitPoints"":""6"",""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=ARCT3010""
                        }
                    ]
                },
                {
                    ""typeName"":""Complementary"",
                    ""typeInto"":""Take all complementary units (6 points):"",
                    ""units"":[
                        {
                            ""unitCode"":""IDES3010"",
                            ""unitTitle"":""Advanced Design Thinking"",
                            ""unitPoints"":""6"",
                            ""unitURL"":""http:\/\/handbooks.uwa.edu.au\/units\/unitdetails?code=IDES3010""
                        }
                    ]
                }
            ]
        }
    ]}
]",


NULL,NULL,NULL,NULL,NULL,"Architecture A","Arts, Business, Law and Education","UWA Design School","current / 2018",2012,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,False,NULL

"""