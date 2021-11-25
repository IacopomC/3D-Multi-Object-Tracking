# ---------------------------------------------------------------------
# Project "Track 3D-Objects Over Time"
# Copyright (C) 2020, Dr. Antje Muntzinger / Dr. Andreas Haja.
#
# Purpose of this file : Classes for track and track management
#
# You should have received a copy of the Udacity license together with this program.
#
# https://www.udacity.com/course/self-driving-car-engineer-nanodegree--nd013
# ----------------------------------------------------------------------
#

# imports
import numpy as np
import collections
import misc.params as params

# add project directory to python path to enable relative imports
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))


class Track:
    """
    Track class with state, covariance, id, score
    """

    def __init__(self, meas, id):
        print('creating track no.', id)
        M_rot = meas.sensor.sens_to_veh[0:3, 0:3]  # rotation matrix from sensor to vehicle coordinates
        
        ############
        # Initialize x and P based on unassigned measurement transformed from sensor to vehicle coordinates
        ############

        # initialize state vector x with zeros
        self.x = np.zeros((params.dim_state, 1))

        # transform measurement values from sensor to vehicle coordinates
        z = np.ones((4, 1))  # transform into homogenous coordinates to apply coord transform
        z[0:3] = meas.z[:3]
        z = meas.sensor.sens_to_veh * z

        # initialize position part state vector with measurement values
        self.x[:3] = z[0:3]

        # initialize covariance error matrix P with zeros
        self.P = np.zeros((params.dim_state, params.dim_state))

        # fill position covariance error part using measurement error R (convert from sensor to vehicle coordinates)
        self.P[0:3, 0:3] = M_rot * meas.R * M_rot.transpose()

        # fill velocity covariance error part using lidar parameters
        self.P[3:, 3:] = np.diag([params.sigma_lidar_x**2, params.sigma_lidar_y**2, params.sigma_lidar_z**2])

        self.state = 'initialized'
        self.score = 1./params.window

        # other track attributes
        self.id = id
        self.width = meas.width
        self.length = meas.length
        self.height = meas.height

        # transform rotation from sensor to vehicle coordinates
        self.yaw = np.arccos(M_rot[0, 0]*np.cos(meas.yaw) + M_rot[0, 1]*np.sin(meas.yaw))
        self.t = meas.t

    def set_x(self, x):
        self.x = x
        
    def set_P(self, P):
        self.P = P  
        
    def set_t(self, t):
        self.t = t  
        
    def update_attributes(self, meas):
        # use exponential sliding average to estimate dimensions and orientation
        if meas.sensor.name == 'lidar':
            c = params.weight_dim
            self.width = c*meas.width + (1 - c)*self.width
            self.length = c*meas.length + (1 - c)*self.length
            self.height = c*meas.height + (1 - c)*self.height
            M_rot = meas.sensor.sens_to_veh

            # transform rotation from sensor to vehicle coordinates
            self.yaw = np.arccos(M_rot[0, 0]*np.cos(meas.yaw) + M_rot[0, 1]*np.sin(meas.yaw))


class Trackmanagement:
    """
    Track manager with logic for initializing and deleting objects
    """

    def __init__(self):
        self.N = 0 # current number of tracks
        self.track_list = []
        self.last_id = -1
        self.result_list = []
        
    def manage_tracks(self, unassigned_tracks, unassigned_meas, meas_list):  
        ############
        # TODO Step 2: implement track management:
        # - decrease the track score for unassigned tracks
        # - delete tracks if the score is too low or P is too big (check params.py for parameters that might be helpful, but
        # feel free to define your own parameters)
        ############
        
        # decrease score for unassigned tracks
        for i in unassigned_tracks:
            track = self.track_list[i]
            # check visibility    
            if meas_list: # if not empty
                if meas_list[0].sensor.in_fov(track.x):
                    # your code goes here
                    pass 

        # delete old tracks   

        ############
        # END student code
        ############ 
            
        # initialize new track with unassigned measurement
        for j in unassigned_meas: 
            if meas_list[j].sensor.name == 'lidar': # only initialize with lidar measurements
                self.init_track(meas_list[j])
            
    def addTrackToList(self, track):
        self.track_list.append(track)
        self.N += 1
        self.last_id = track.id

    def init_track(self, meas):
        track = Track(meas, self.last_id + 1)
        self.addTrackToList(track)

    def delete_track(self, track):
        print('deleting track no.', track.id)
        self.track_list.remove(track)
        
    def handle_updated_track(self, track):      
        ############
        # TODO Step 2: implement track management for updated tracks:
        # - increase track score
        # - set track state to 'tentative' or 'confirmed'
        ############

        pass
        
        ############
        # END student code
        ############ 