from math import radians, cos, sin, asin, sqrt, degrees
"""Shrink Coordinate"""
class GridCal():
    def __init__(self) -> None:
        pass
    def distance(self,edge): 
        
        # The math module contains a function named 
        # radians which converts from degrees to radians.
        if(edge[0] < edge[1]):
            lon1 = radians(edge[0][0]) 
            lat1 = radians(edge[0][1]) 
            lon2 = radians(edge[1][0]) 
            lat2 = radians(edge[1][1]) 
        else:
            lon1 = radians(edge[1][0]) 
            lat1 = radians(edge[1][1]) 
            lon2 = radians(edge[0][0]) 
            lat2 = radians(edge[0][1])

        # Haversine formula  
        dlon = lon2 - lon1  
        dlat = lat2 - lat1 
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
        c = 2 * asin(sqrt(a))
        
        # calculate the result 
        return(c * 6371) 


    def shrink_horizontal_coordinates(self,horizontal_edge, horizontal_distance):
        # The math module contains a function named 
        # radians which converts from degrees to radians. 
        lon1 = radians(horizontal_edge[0][0]) 
        lat1 = radians(horizontal_edge[0][1]) 
        lon2 = radians(horizontal_edge[1][0]) 
        lat2 = radians(horizontal_edge[1][1]) 
        dis = horizontal_distance
        #long2-long1 should be positive

        a = []

        if(lon2 > lon1):

            dis3 = dis/4 * 3
            a.append(degrees(-(  2*asin(sqrt((sin(dis3/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2))))  ) + lon2))

        else:
            lon1 = lon2           #this will change the cordinates

            dis3 = (dis/4) * 3
            a.append(degrees(2*asin(sqrt((sin(dis3/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2)))) + lon1))

        return(a) 



    #incomplete
    def shrink_vertical_coordinates(self,vertical_edge, vertical_distance):
        
        lon1 = radians(vertical_edge[0][0]) 
        lat1 = radians(vertical_edge[0][1]) 
        lon2 = radians(vertical_edge[1][0]) 
        lat2 = radians(vertical_edge[1][1]) 
        dis = vertical_distance
        a = []
        
        # calculate the result 
        if(lat1 < lat2): #lar1 is known


            dis3 = dis/4 * 3
            a.append(degrees(dis3/6371 + lat1))

        else:
            print("reached2")
            lat2 = lat1

            dis3 = dis/4 * 3
            a.append(degrees(-dis3/6371 + lat2))


        return(a) 

    def shrink_total(self,cordinates): 

        horizontal_edge = list()
        vertical_edge    = list()

        horizontal_edge.append(cordinates[0][0])
        horizontal_edge.append(cordinates[0][1])
        vertical_edge.append(cordinates[0][1])
        vertical_edge.append(cordinates[0][2])


        unique_cordinates = {
            "horizontal_edge_coordinates" : [cordinates[0][1][0]],
            "vertical_edge_coordinates"   : [cordinates[0][1][1]]
        }


        horizontal_distance = self.distance(horizontal_edge)
        vertical_distance = self.distance(vertical_edge)

        # print(vertical_edge)

        unique_cordinates["horizontal_edge_coordinates"] = unique_cordinates["horizontal_edge_coordinates"] + self.shrink_horizontal_coordinates(horizontal_edge, horizontal_distance)
        unique_cordinates["vertical_edge_coordinates"] = unique_cordinates["vertical_edge_coordinates"] + self.shrink_vertical_coordinates(vertical_edge, vertical_distance)


        # horizontal_edge_coordinates = longitude = l
        # vertical_edge_coordinates = latitude    = b


        l = list(unique_cordinates["horizontal_edge_coordinates"])
        b = list(unique_cordinates["vertical_edge_coordinates"])


        rec1 = [    [
                    [l[1],b[0]] , 
                    [l[0],b[0]] , 
                    [l[0],b[1]] , 
                    [l[1],b[1]] , 
                    [l[1],b[0]]]    
                ]


        return(rec1)

    """divide Grid"""

    def distance(self,edge): 
        
        # The math module contains a function named 
        # radians which converts from degrees to radians.
        if(edge[0] < edge[1]):
            lon1 = radians(edge[0][0]) 
            lat1 = radians(edge[0][1]) 
            lon2 = radians(edge[1][0]) 
            lat2 = radians(edge[1][1]) 
        else:
            lon1 = radians(edge[1][0]) 
            lat1 = radians(edge[1][1]) 
            lon2 = radians(edge[0][0]) 
            lat2 = radians(edge[0][1])

        # Haversine formula  
        dlon = lon2 - lon1  
        dlat = lat2 - lat1 
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
        c = 2 * asin(sqrt(a))
        
        # calculate the result 
        return(c * 6371) 


    def horizontal_coordinates(self,horizontal_edge, horizontal_distance):
        # The math module contains a function named 
        # radians which converts from degrees to radians. 
        lon1 = radians(horizontal_edge[0][0]) 
        lat1 = radians(horizontal_edge[0][1]) 
        lon2 = radians(horizontal_edge[1][0]) 
        lat2 = radians(horizontal_edge[1][1]) 
        dis = horizontal_distance
        #long2-long1 should be positive

        a = []

        if(lon2 > lon1):
            dis1 = (dis/4)
            a.append(degrees(-(  2*asin(sqrt((sin(dis1/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2))))  ) + lon2))
            dis2 = (dis/2)
            a.append(degrees(-(  2*asin(sqrt((sin(dis2/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2))))  ) + lon2))
            dis3 = dis/4 * 3
            a.append(degrees(-(  2*asin(sqrt((sin(dis3/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2))))  ) + lon2))

            a.append(horizontal_edge[0][0])
            # a=lon1
        else:
            lon1 = lon2           #this will change the cordinates
            dis1 = (dis/4)
            a.append(degrees(2*asin(sqrt((sin(dis1/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2)))) + lon1))
            dis2 = (dis/2)
            a.append(degrees(2*asin(sqrt((sin(dis2/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2)))) + lon1))
            dis3 = (dis/4) * 3
            a.append(degrees(2*asin(sqrt((sin(dis3/(6371*2))**2)  *  1/(cos(lat1) * cos(lat2)))) + lon1))

            a.append(horizontal_edge[0][0])
            # a=lon2
        # lon2 = 2*a + lon1       
        # calculate the result 
        return(a) 



    #incomplete
    def vertical_coordinates(self,vertical_edge, vertical_distance):
        
        lon1 = radians(vertical_edge[0][0]) 
        lat1 = radians(vertical_edge[0][1]) 
        lon2 = radians(vertical_edge[1][0]) 
        lat2 = radians(vertical_edge[1][1]) 
        dis = vertical_distance
        a = []
        
        # calculate the result 
        if(lat1 < lat2): #lar1 is known
            dis1 = (dis/4)
            a.append(degrees(dis1/6371 + lat1))
            
            dis2 = (dis/2)
            a.append(degrees(dis2/6371 + lat1))

            dis3 = dis/4 * 3
            a.append(degrees(dis3/6371 + lat1))

            a.append(vertical_edge[1][1])
            # a = lat2
        else:
            print("reached2")
            lat2 = lat1

            dis1 = (dis/4)
            a.append(degrees(-dis1/6371 + lat2))

            dis2 = (dis/2)
            a.append(degrees(-dis2/6371 + lat2))

            dis3 = dis/4 * 3
            a.append(degrees(-dis3/6371 + lat2))

            a.append(vertical_edge[1][1])
            # a = lat1

        return(a) 

    def grid(self,cordinates): 

        horizontal_edge = list()
        vertical_edge    = list()

        horizontal_edge.append(cordinates[0][0])
        horizontal_edge.append(cordinates[0][1])
        vertical_edge.append(cordinates[0][1])
        vertical_edge.append(cordinates[0][2])


        unique_cordinates = {
            "horizontal_edge_coordinates" : [cordinates[0][1][0]],
            "vertical_edge_coordinates"   : [cordinates[0][1][1]]
        }


        horizontal_distance = self.distance(horizontal_edge)
        vertical_distance = self.distance(vertical_edge)

        # print(vertical_edge)

        unique_cordinates["horizontal_edge_coordinates"] = unique_cordinates["horizontal_edge_coordinates"] + self.horizontal_coordinates(horizontal_edge, horizontal_distance)
        unique_cordinates["vertical_edge_coordinates"] = unique_cordinates["vertical_edge_coordinates"] + self.vertical_coordinates(vertical_edge, vertical_distance)


        # horizontal_edge_coordinates = longitude = l
        # vertical_edge_coordinates = latitude    = b

        totalrect = []
        for x in range(0,4):
            
            l = list(unique_cordinates["horizontal_edge_coordinates"])
            b = list(unique_cordinates["vertical_edge_coordinates"])

            rec1 = [    [[l[x],b[0]] , [l[x + 1],b[0]] , [l[x + 1],b[1]] , [l[x],b[1]] , [l[x],b[0]]]    ]
            rec2 = [    [[l[x],b[1]] , [l[x + 1],b[1]] , [l[x + 1],b[2]] , [l[x],b[2]] , [l[x],b[1]]]    ]
            rec3 = [    [[l[x],b[2]] , [l[x + 1],b[2]] , [l[x + 1],b[3]] , [l[x],b[3]] , [l[x],b[2]]]    ]
            rec4 = [    [[l[x],b[3]] , [l[x + 1],b[3]] , [l[x + 1],b[4]] , [l[x],b[4]] , [l[x],b[3]]]    ]

            totalrect = totalrect + rec1 + rec2 + rec3 + rec4

        return(totalrect)