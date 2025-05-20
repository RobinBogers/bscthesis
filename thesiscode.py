import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Container:
    def __init__(self,x:int,y:int,z:int):
        #Generates a container of size x,y,z
        self.x=x
        self.y=y
        self.z=z
        self.placed_boxes=[] #[[Corner 0,Corner 1,...,Corner 7],[...],...]
        self.ems=[] #[[min x,min y,min z,max x,max y,max z,Anchor_Distance,Anchor_Corner],[...],...]

    def Print_Boxlist(self):
        #Prints a list of the placed boxes with their index
        for i in self.placed_boxes:
            print(f"Box {self.placed_boxes.index(i)}:{i[0]}")

    def Box_Corners(self,x,y,z,a,b,c):
        #Gives the corner coordinates of a box of size a,b,c placed at coordinates x,y,z
        return [x,y,z],[x+a,y,z],[x,y+b,z],[x,y,z+c],[x+a,y+b,z],[x+a,y,z+c],[x,y+b,z+c],[x+a,y+b,z+c]

    def Check_Placement(self,x,y,z,a,b,c):
        #Checks if a box of size a,b,c can be placed at coordinates x,y,z
        if x>self.x or y>self.y or z>self.z or x+a>self.x or y+b>self.y or z+c>self.z:
            #Checks if the box falls outside the container
            return False  
        #Checks if boxes overlap:
        new_min=[x,y,z]
        new_max=[x+a,y+b,z+c]
        for c in self.placed_boxes:
            placed_min=c[0][0]
            placed_max=c[0][7]
            if not (new_max[0] <= placed_min[0] or new_min[0] >= placed_max[0] or
                new_max[1] <= placed_min[1] or new_min[1] >= placed_max[1] or
                new_max[2] <= placed_min[2] or new_min[2] >= placed_max[2]):
                return False      
        else:
            return True

    def Place_Box(self,x,y,z,a,b,c):
        #Place box of size a,b,c at coordinates x,y,z
        if Container.Check_Placement(self,x,y,z,a,b,c)==True:
            self.placed_boxes.append([Container.Box_Corners(self,x,y,z,a,b,c)])
        else:
            print(f"Can't place box of size ({a},{b},{c}) at coordinates({x},{y},{z})")
            

    def gen_img(self):
        #Generates an image of the container with the placed boxes
        fig=plt.figure()
        ax=fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, self.x)
        ax.set_ylim(0, self.y)
        ax.set_zlim(0, self.z)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Container Visualization')

        def draw_box(ax,corners,color='skyblue',alpha=0.5):
            #Draws boxes
            faces=[
            [corners[0], corners[1], corners[5], corners[3]],
            [corners[1], corners[4], corners[7], corners[5]],
            [corners[2], corners[4], corners[7], corners[6]],
            [corners[0], corners[2], corners[6], corners[3]],
            [corners[0], corners[1], corners[4], corners[2]],
            [corners[3], corners[5], corners[7], corners[6]]]           
            box=Poly3DCollection(faces,alpha=alpha,linewidths=1,edgecolors='k')
            box.set_facecolor(color)
            ax.add_collection3d(box)
            
        for box in self.placed_boxes:
            draw_box(ax,box[0])

        plt.show()

    def EMS(self):
        #Determines all empty maximal spaces and their anchor distance and anchor corner
        """
        After box 1 determine all EMS
        After box 2, split all the EMS it's placed in in max. 3 new EMS since boxes are always placed in a corner of an EMS
        Repeat
        min and max coords of box are starting points for all 3 EMS
        Calc anchor corners and distances for every EMS
        """

        if self.ems==[] and len(self.placed_boxes)==1:
            #First box is always placed at coordinates (0,0,0)
            initial_box=self.placed_boxes[0][0]
            max_corner=initial_box[7]
            Distance1,Anchor1,Container1=self.Anchor_Corner([max_corner[0],0,0,self.x,self.y,self.z])
            Distance2,Anchor2,Container2=self.Anchor_Corner([0,max_corner[1],0,self.x,self.y,self.z])
            Distance3,Anchor3,Container3=self.Anchor_Corner([0,0,max_corner[2],self.x,self.y,self.z])
            self.ems.append([max_corner[0],0,0,self.x,self.y,self.z,Distance1,Anchor1])
            self.ems.append([0,max_corner[1],0,self.x,self.y,self.z,Distance2,Anchor2])
            self.ems.append([0,0,max_corner[2],self.x,self.y,self.z,Distance3,Anchor3])


        else:
            """
            Voor elke EMS, til 1 van de coordinaten omhoog naar de max van de doos die je net hebt geplaatst
            """
            #Boxes are always placed in a corner of an EMS, so split old EMS up into 3 new EMS
            last_box=self.placed_boxes[-1][0]
            old_ems=[]
            box_corner=[]
            #If a corner of the last box is the corner of an EMS, split that EMS up
            for corner in last_box:
                for ems in self.ems:
                    min_x=ems[0]
                    min_y=ems[1]
                    min_z=ems[2]
                    max_x=ems[3]
                    max_y=ems[4]
                    max_z=ems[5]
                    ems_corners=[[min_x,min_y,min_z],[max_x,min_y,min_z],[min_x,max_y,min_z],[min_x,min_y,max_z],
                                 [max_x,max_y,min_z],[max_x,min_y,max_z],[min_x,max_y,max_z],[max_x,max_y,max_z]]    
                    if corner in ems_corners:
                        old_ems.append(ems)
                        box_corner.append(corner)
                        self.ems.remove(ems)                
                    """                  
                    if corner==ems[7]:
                        old_ems.append(ems)
                        self.ems.remove(ems)
                        box_corner.append(corner)                    
                    """

            for ems in old_ems:
                #Splits every old EMS, dependent on which corner the box is placed in
                box_coords=[last_box[0][0],last_box[0][1],last_box[0][2],last_box[7][0],last_box[7][1],last_box[7][2]]
                ems_index=old_ems.index(ems)
                min_x=ems[0]
                min_y=ems[1]
                min_z=ems[2]
                max_x=ems[3]
                max_y=ems[4]
                max_z=ems[5]
                ems_corners=[[min_x,min_y,min_z],[max_x,min_y,min_z],[min_x,max_y,min_z],[min_x,min_y,max_z],
                             [max_x,max_y,min_z],[max_x,min_y,max_z],[min_x,max_y,max_z],[max_x,max_y,max_z]]
                selected_corner=box_corner[ems_index]
                if selected_corner==ems_corners[0]:
                    #Box at (min_x,min_y,min_z)
                    Distance1,Anchor1,Container1=self.Anchor_Corner([box_coords[3],min_y,min_z,max_x,max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,box_coords[4],min_z,max_x,max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,box_coords[5],max_x,max_y,max_z])
                    ems1=[box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)
                    """
                    self.ems.append([box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1])
                    self.ems.append([min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2])
                    self.ems.append([min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3])
                    """
                elif selected_corner==ems_corners[1]:
                    #Box at (BoxX0,min_y,min_z)
                    Distance1,Anchor1,Container1=self.Anchor_Corner([min_x,min_y,min_z,box_coords[0],max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,box_coords[4],min_z,max_x,max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,box_coords[5],max_x,max_y,max_z])
                    ems1=[min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)
                    """                   
                    self.ems.append([min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1])
                    self.ems.append([min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2])
                    self.ems.append([min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3])
                    """  
                elif selected_corner==ems_corners[2]:
                    #Box at (min_x,BoxY0,min_z)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([min_x,min_y,min_z,max_x,box_coords[1],max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,min_y,min_z,box_coords[3],max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,box_coords[5],max_x,max_y,max_z])
                    ems1=[min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance1,Anchor1]
                    ems2=[min_x,min_y,min_z,box_coords[3],max_y,max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3) 
                    """                        
                    self.ems.append([min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance1,Anchor1])
                    self.ems.append([min_x,min_y,min_z,box_coords[3],max_y,max_z,Distance2,Anchor2])
                    self.ems.append([min_x,min_y,box_coords[5],max_x,max_y,max_z,Distance3,Anchor3])
                    """ 
                    
                elif selected_corner==ems_corners[3]:
                    #Box at (min_x,min_y,boxZ0)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([box_coords[3],min_y,min_z,max_x,max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,box_coords[4],min_z,max_x,max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,min_z,max_x,max_y,box_coords[2]])
                    ems1=[box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)                     
                    #self.ems.append([box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1])
                    #self.ems.append([min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2])
                    #self.ems.append([min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3])
                elif selected_corner==ems_corners[4]:
                    #Box at (BoxX0,BoxY0,min_z)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([min_x,min_y,min_z,box_coords[0],max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,min_y,min_z,max_x,box_coords[1],max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,box_coords[2],max_x,max_y,max_z])
                    ems1=[min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,box_coords[2],max_x,max_y,max_z,Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)                     
                    #self.ems.append([min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1])
                    #self.ems.append([min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2])
                    #self.ems.append([min_x,min_y,box_coords[2],max_x,max_y,max_z,Distance3,Anchor3])                               
                elif selected_corner==ems_corners[5]:
                    #Box at (BoxX0,min_y,BoxZ0)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([min_x,min_y,min_z,box_coords[0],max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,box_coords[4],min_z,max_x,max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,min_z,max_x,max_y,box_coords[2]])
                    ems1=[min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)                     
                    #self.ems.append([min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1])
                    #self.ems.append([min_x,box_coords[4],min_z,max_x,max_y,max_z,Distance2,Anchor2])
                    #self.ems.append([min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3])              
                elif selected_corner==ems_corners[6]:
                    #Box at (min_x,BoxY0,BoxZ0)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([box_coords[3],min_y,min_z,max_x,max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,min_y,min_z,max_x,box_coords[1],max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,min_z,max_x,max_y,box_coords[2]])
                    ems1=[box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)                     
                    #self.ems.append([box_coords[3],min_y,min_z,max_x,max_y,max_z,Distance1,Anchor1])
                    #self.ems.append([min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2])
                    #self.ems.append([min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3])
                elif selected_corner==ems_corners[7]:
                    #Box at (BoxX0,BoxY0,BoxZ0)                  
                    Distance1,Anchor1,Container1=self.Anchor_Corner([min_x,min_y,min_z,box_coords[0],max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,min_y,min_z,max_x,box_coords[1],max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,min_y,min_z,max_x,max_y,box_coords[2]])
                    ems1=[min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1]
                    ems2=[min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2]
                    ems3=[min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3]
                    if ems1 not in self.ems:
                        self.ems.append(ems1)
                    if ems2 not in self.ems:
                        self.ems.append(ems2)
                    if ems3 not in self.ems:
                        self.ems.append(ems3)                     
                    #self.ems.append([min_x,min_y,min_z,box_coords[0],max_y,max_z,Distance1,Anchor1])
                    #self.ems.append([min_x,min_y,min_z,max_x,box_coords[1],max_z,Distance2,Anchor2])
                    #self.ems.append([min_x,min_y,min_z,max_x,max_y,box_coords[2],Distance3,Anchor3])
                #print(box_coords)
                #print(self.ems[-3])
                #print(self.ems[-2])
                #print(self.ems[-1])


            """                
                if selected_corner==ems_corners[0]:
                    #Box at (min_x,min_y,min_z)
                    Distance1,Anchor1,Container1=self.Anchor_Corner([box_coords[3],min_y,min_z,max_x,max_y,max_z])
                    Distance2,Anchor2,Container2=self.Anchor_Corner([min_x,box_coords[4],min_z,max_x,max_y,max_z])
                    Distance3,Anchor3,Container3=self.Anchor_Corner([min_x,box_coords[1],min_z,max_x,max_y,max_z])
                    self.ems.append([box_coords[3],box_coords[1],box_coords[2],max_x,max_y,max_z,Distance1,Anchor1])
                    self.ems.append([box_coords[0],box_coords[4],box_coords[2],max_x,max_y,max_z,Distance2,Anchor2])
                    self.ems.append([box_coords[0],box_coords[1],box_coords[5],max_x,max_y,max_z,Distance3,Anchor3])
            """

    def Anchor_Corner(self,ems):
        #Calculates the anchor distance, anchor corner and the closest corner of the container for every EMS
        min_x=ems[0]
        min_y=ems[1]
        min_z=ems[2]
        max_x=ems[3]
        max_y=ems[4]
        max_z=ems[5]
        ems_corners=[[min_x,min_y,min_z],[max_x,min_y,min_z],[min_x,max_y,min_z],[min_x,min_y,max_z],
                     [max_x,max_y,min_z],[max_x,min_y,max_z],[min_x,max_y,max_z],[max_x,max_y,max_z]]
        Manhattan_Distances=[]
        Container_Corners=[]
        for ems_corner in ems_corners:
            M_dist,C_corner=self.Calc_Distance(ems_corner)
            Manhattan_Distances.append(M_dist)
            Container_Corners.append(C_corner)
        min_index=Manhattan_Distances.index(min(Manhattan_Distances))
        return Manhattan_Distances[min_index],ems_corners[min_index],Container_Corners[min_index]

    def Calc_Distance(self,ems_corner):
    #Calculates the Manhattan distance from a corner of an EMS to it's closest corner of the container
    #Returns the Manhattan distance and closest corner of the container
        container_corners=[[0,0,0],[self.x,0,0],[0,self.y,0],[0,0,self.z],
                           [self.x,self.y,0],[self.x,0,self.z],[0,self.y,self.z],[self.x,self.y,self.z]]
        manhattan_distances=[]
        for c_corner in container_corners:
            manhattan_distances.append(abs(c_corner[0]-ems_corner[0])+abs(c_corner[1]-ems_corner[1])+abs(c_corner[2]-ems_corner[2]))
        min_index=manhattan_distances.index(min(manhattan_distances))
        return manhattan_distances[min_index],container_corners[min_index]             

    def Corner_Distances(self,box):
        #Places boxes according to the corner distances rule
        box_x=box[0]
        box_y=box[1]
        box_z=box[2]
        if self.placed_boxes==[]:
            #First box is always placed at (0,0,0)
            Container.Place_Box(self,0,0,0,box_x,box_y,box_z)
            Container.EMS(self)
        else:
            #Check which EMS has the smallest corner distance
            #Place box there
            #Update EMS
            Optimal_ems=[]
            for ems in self.ems:
                if Optimal_ems==[] or ems[6]<Optimal_ems[6]:
                    Optimal_ems=ems
            min_x=Optimal_ems[0]
            min_y=Optimal_ems[1]
            min_z=Optimal_ems[2]
            max_x=Optimal_ems[3]
            max_y=Optimal_ems[4]
            max_z=Optimal_ems[5]
            ems_x=max_x-min_x
            ems_y=max_y-min_y
            ems_z=max_z-min_z
            Anchor_Corner=Optimal_ems[7]
            ems_corners=[[min_x,min_y,min_z],[max_x,min_y,min_z],[min_x,max_y,min_z],[min_x,min_y,max_z],
                         [max_x,max_y,min_z],[max_x,min_y,max_z],[min_x,max_y,max_z],[max_x,max_y,max_z]]
            if ems_corners[0]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,min_x,min_y,min_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[1]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,max_x-box_x,min_y,min_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[2]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,min_x,max_y-box_y,min_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[3]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,min_x,min_y,max_z-box_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[4]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,max_x-box_x,max_y-box_z,min_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[5]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,max_x-box_x,min_y,max_z-box_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[6]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,min_x,max_y-box_y,max_z-box_z,box_x,box_y,box_z)
                Container.EMS(self)
            elif ems_corners[7]==Anchor_Corner and ems_x>=box_x and ems_y>=box_y and ems_z>=box_z:
                Container.Place_Box(self,max_x-box_x,max_y-box_y,max_z-box_z,box_x,box_y,box_z)
                Container.EMS(self)

    def gen_ems(self):
        #Generates an image of the container with all EMS
        fig=plt.figure()
        ax=fig.add_subplot(111, projection='3d')
        ax.set_xlim(0, self.x)
        ax.set_ylim(0, self.y)
        ax.set_zlim(0, self.z)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('EMS Visualization')

        def draw_box(ax,corners,color='skyblue',alpha=0.5):
            #Draws boxes
            faces=[
            [corners[0], corners[1], corners[5], corners[3]],
            [corners[1], corners[4], corners[7], corners[5]],
            [corners[2], corners[4], corners[7], corners[6]],
            [corners[0], corners[2], corners[6], corners[3]],
            [corners[0], corners[1], corners[4], corners[2]],
            [corners[3], corners[5], corners[7], corners[6]]]           
            box=Poly3DCollection(faces,alpha=alpha,linewidths=1,edgecolors='k')
            box.set_facecolor(color)
            ax.add_collection3d(box)
            
        for ems in self.ems:
            min_x=ems[0]
            min_y=ems[1]
            min_z=ems[2]
            max_x=ems[3]
            max_y=ems[4]
            max_z=ems[5]
            ems_corners=[[min_x,min_y,min_z],[max_x,min_y,min_z],[min_x,max_y,min_z],[min_x,min_y,max_z],
                         [max_x,max_y,min_z],[max_x,min_y,max_z],[min_x,max_y,max_z],[max_x,max_y,max_z]]
            draw_box(ax,ems_corners)

        plt.show()
"""
C=Container(1200,230,240)
print(Container.Box_Corners(C,0,0,0,1,2,3))
Container.Place_Box(C,0,0,0,100,100,100)
Container.Place_Box(C,100,0,0,700,100,200)
Container.Place_Box(C,0,0,0,5,6,5)
Container.Print_Boxlist(C)
Container.gen_img(C)
print(Container.Calc_Distance(C,[1000,100,100,500,500,500]))
Container.EMS(C)
"""

C=Container(1200,230,240)
boxes=[[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100],[100,100,100]]
for box in boxes:
    Container.Corner_Distances(C,box)
    Container.gen_ems(C)
    Container.gen_img(C)
Container.gen_img(C)

#EMS code toevoegen
#Opt. placement code toevoegen
#volume utilization code toevoegen