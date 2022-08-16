import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from ipywidgets import interact, widgets, Layout, Button, Box, VBox, IntSlider
import threading as thrd
import time

class Singleton:
    def __init__(self, cls):
        self._cls = cls

    def Instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._cls()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._cls)

@Singleton
class Renderer(thrd.Thread):
    
    #Make singleton
    _instance = None
    
    def __init__(self):
        # Call the Thread class's init function
        thrd.Thread.__init__(self)

        
    def initialize(self, model_state, pos_error_x, pos_error_y, marker_error_x, marker_error_y, measurements=None, true_state=None, landmarks=None, robot_cov=None, marker_cov=None, add_aruco=False, dt_data=0.2):
        self.lock = thrd.Lock()

        self.initialized = False
        self.measurements = measurements
        self.landmarks = landmarks
        self.marker_cov = marker_cov
        self.true_state = true_state
        self.robot_cov = robot_cov        
        self.paused = False
        self.cur_frame = 0
        self.dt_data = dt_data
        self.dt_render = dt_data
        self.state = model_state
        self.aruco_markers = {}
        self.pex = pos_error_x
        self.pey = pos_error_y
        self.mex = marker_error_x
        self.mey = marker_error_y
                
        # Initialize figure
        fig = plt.figure(constrained_layout=True, figsize=(14, 5))
        gs = fig.add_gridspec(2, 2)
        ax = fig.add_subplot(gs[:, 0])
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_xlim([0, 500])
        ax2.set_ylim([-5, 5])
        ax2.set_title('State Error')
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Difference between true\nand predicted value')
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.set_title('Marker Error')
        ax3.set_xlabel('Time')
        ax3.set_ylabel('Avg. difference between\ntrue and predicted value')
        ax3.set_xlim([0, 500])
        ax3.set_ylim([-5, 5])

        ax.set_xlim([-4,-1.5])
        ax.set_ylim([-3.5,-1.5])
        ax.tick_params(axis='both', which='major', labelsize=7)
        ax.set_title('Overhead View')
        ax.set_xlabel('X (m)',weight='bold')
        ax.set_ylabel('Y (m)',weight='bold')

        self.figure = fig

        # Plot ground truth trajectory
        ax.plot(self.true_state[:, 0], self.true_state[:, 1], c='r', lw=1, label='True state (from data)')
        
        # Plot current model state
        self.line, = ax.plot(self.state[0,0], self.state[0, 1], c='b', lw=1, label='Predicted state (model)')

        # Plot position error
        self.pos_x_error, = ax2.plot(0, self.true_state[0, 0] - self.state[0, 0], label = 'X-coordinate')
        self.pos_y_error, = ax2.plot(0, self.true_state[0, 1] - self.state[0, 1], label = 'Y-coordinate')
        ax2.legend(loc='best')

        self.marker_x_error, = ax3.plot(0, 0, label = 'X-coordinate')
        self.marker_y_error, = ax3.plot(0, 0, label = 'Y-coordinate')
        ax3.legend(loc='best')

        ax.legend(loc='upper right')
        # Create Robot Axes 
        self.robot_ax = []
        self.robot_ax.append(FancyArrowPatch((0,0), (0.15,0),
                                            mutation_scale=8,color='red'))
        self.robot_ax.append(FancyArrowPatch((0,0), (0,0.15),
                                            mutation_scale=8,color='green'))
        
        # Apply translation and rotation as specified by current robot state
        cos_theta, sin_theta = np.cos(self.state[0,2]), np.sin(self.state[0,2])
        Tw_r = np.eye(3)
        Tw_r[0:2,2] = self.state[0,:2]
        Tw_r[0:2,0:2] = [[cos_theta,-sin_theta],[sin_theta,cos_theta]]
        Tw_r_obj = transforms.Affine2D(Tw_r)
        self.ax_trans = ax.transData
        self.robot_ax[0].set_transform(Tw_r_obj+self.ax_trans)
        self.robot_ax[1].set_transform(self.robot_ax[0].get_transform())
        ax.add_patch(self.robot_ax[0])
        ax.add_patch(self.robot_ax[1])


        if add_aruco:
            marker_files = [filename for filename in os.listdir('Practical04_Support/images') if filename.startswith("M")]
            marker_world_width = 0.3
            for i,filename in enumerate(sorted(marker_files)):
                fprts = filename.split('_')
                mp = np.array([float(fprts[1]),float(fprts[2])])
                mi = cv2.imread('Practical04_Support/images/'+filename)
                ext = [mp[0]-marker_world_width/2,mp[0]+marker_world_width/2,\
                mp[1]-marker_world_width/2,mp[1]+marker_world_width/2]
                ax.imshow(mi,extent=ext)
                ax.annotate(str(i),(mp[0],mp[1]),color='red',weight='bold')
                self.aruco_markers[int(fprts[0][-1])] = mp


        #Set up to plot measurements
        if self.measurements is not None:
            self.marker_lines = []
            self.marker_lables = []
            self.marker_scatter = ax.scatter(np.zeros((10,1)),np.zeros((10,1)),color='lime')
            for i in range(10):
                ln, = ax.plot(np.zeros((2,1)),np.zeros((2,1)),color='yellow',alpha=0.5)
                self.marker_lines.append(ln)
                an = ax.annotate(str(i),(-3,-2.5),color='green',weight='bold')
                self.marker_lables.append(an)
                
        #Set up to plot added landmarks
        if self.landmarks is not None:
            self.landmarks_scatter = ax.scatter(self.landmarks[0][0,:],self.landmarks[0][1,:],s=80,color='red')
        
        if self.marker_cov is not None:
            num_landmarks = self.landmarks[-1].shape[1]
            self.marker_ells = []
            for i in range(num_landmarks):
                el = Ellipse((0,0),
                              width=0.3, height=0.3,
                              angle=0,facecolor='none',edgecolor='blue')
                self.marker_ells.append(el)
                ax.add_patch(el)
            for i in range(self.landmarks[self.cur_frame].shape[1]):
                self.marker_ells[i].set_center((self.landmarks[self.cur_frame][0,i],self.landmarks[self.cur_frame][1,i]))
        
        #Set up ellipsoid to draw robot covariance
        if self.robot_cov is not None:
            cov = self.robot_cov[0,:,:]
            a = cov[0,0]
            b = cov[0,1]
            c = cov[1,0]
            d = cov[1,1]
            B = -(a+d)
            C = (a*d-b*c)
            lam1 = (-B+np.sqrt(B**2-4*C))/2
            lam2 = (-B-np.sqrt(B**2-4*C))/2
            v1 = np.array([[lam1-d],[c]])
            self.robo_ell = Ellipse((self.state[0,0],self.state[0,1]),
                              width=lam1, height=lam2,
                              angle=np.rad2deg(np.arccos(v1[0]/np.linalg.norm(v1))))
            self.robo_ell.set_facecolor('none')
            self.robo_ell.set_edgecolor('blue')
            ax.add_patch(self.robo_ell)
                
        btn_play = widgets.Button(description='Play/Pause', layout=Layout(flex='1 1 0%', width='auto'), button_style='success')
        btn_play.on_click(self.pause)
        
        btn_prev = widgets.Button(description='<<', layout=Layout(flex='0.3 1 0%', width='auto'), button_style='warning')
        btn_prev.on_click(self.prv)
        
        btn_next = widgets.Button(description='>>', layout=Layout(flex='0.3 1 0%', width='auto'), button_style='warning')
        btn_next.on_click(self.nxt)

        controls = [
            IntSlider(description='Frame: ', layout=Layout(flex='3 1 0%', width='auto'),min=0, max=(model_state.shape[0]-1)),
            btn_prev,
            btn_play,
            btn_next
         ]


        self.slider = controls[0]
        self.slider.observe(self.slider_change, names='value')
        
        box_layout = Layout(display='flex',
                            flex_flow='row',
                            align_items='stretch',
                            width='70%')
        display(Box(children=controls, layout=box_layout))
        
        if not self.is_alive():
            self.start()
            
        self.initialized = True

        # if self.landmarks is not None and self.measurements is not None:
        #     print(len(self.landmarks))
        #     print(len(self.measurements))
        #     x_values = []
        #     y_values = []
        #     for i in range(0, 300, 10):
        #         true_values = np.array([self.aruco_markers[m.tag] for m in self.measurements[i]]).reshape((len(self.measurements[i]), 2)).T
        #         predicted_values = self.landmarks[i]

        #         end_idx = np.min([true_values.shape[1], predicted_values.shape[1]])
        #         x_error = np.mean(true_values[0,:end_idx] - predicted_values[0,:end_idx])
        #         y_error = np.mean(true_values[1,:end_idx] - predicted_values[1,:end_idx])           

        #         x_values.append(x_error)
        #         y_values.append(y_error)

        #     self.marker_x_error.set_data(np.arange(0,300,10), x_values)
        #     self.marker_y_error.set_data(np.arange(0,300,10), y_values)
                            
    #Render Loop
    def run(self):
        while True:
            if self.paused == False:
                self.cur_frame = int(self.cur_frame + self.dt_render/self.dt_data)
                if self.cur_frame >= self.state.shape[0]:
                    self.cur_frame = 0
                if self.initialized == True:
                    self.render()
            time.sleep(self.dt_render)

            
    def render(self):
        self.lock.acquire()
        self.figure.canvas.draw_idle()

        self.line.set_data(self.state[0:self.cur_frame,0],self.state[0:self.cur_frame,1])
        self.slider.value = self.cur_frame
        
        c, s = np.cos(self.state[self.cur_frame,2]), np.sin(self.state[self.cur_frame,2])
        Tw_r = np.eye(3)
        Tw_r[0:2,2] = [self.state[self.cur_frame,0],self.state[self.cur_frame,1]]
        Tw_r[0:2,0:2] = [[c,-s],[s,c]]
        Tw_r_obj = transforms.Affine2D(Tw_r)
        self.robot_ax[0].set_transform(Tw_r_obj+self.ax_trans)
        self.robot_ax[1].set_transform(self.robot_ax[0].get_transform())

        #Render position error
        x_pos_error = self.pex[0:self.cur_frame]
        y_pos_error = self.pey[0:self.cur_frame]
        time = np.arange(self.cur_frame)

        self.pos_x_error.set_data(time, x_pos_error)
        self.pos_y_error.set_data(time, y_pos_error)
        
        #Render marker error
        x_values = self.mex[0:self.cur_frame]
        y_values = self.mey[0:self.cur_frame]
        time = np.arange(self.cur_frame)
        
        self.marker_x_error.set_data(time, x_values)
        self.marker_y_error.set_data(time, y_values)
        
        #Render Measurements
        if self.measurements is not None:
            # Construct a 2x2 rotation matrix from the robot to world
            th = self.state[self.cur_frame,2]
            Rot_0_rob = np.block([[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]])
            robot_xy = self.state[self.cur_frame,0:2].reshape(-1,1)
            for i in range(len(self.marker_lines)):
                self.marker_lines[i].set_visible(False)
                self.marker_lables[i].set_visible(False)
            marker_pos_all = np.zeros((len(self.measurements[self.cur_frame]),2))
            for i in range(len(self.measurements[self.cur_frame])):
                mes = self.measurements[self.cur_frame][i]
                marker_pos = Rot_0_rob.dot(mes.position.reshape(-1,1)) + robot_xy
                marker_pos_all[i,0] = marker_pos[0]
                marker_pos_all[i,1] = marker_pos[1]
                self.marker_lines[mes.tag].set_data([robot_xy[0],marker_pos[0]],[robot_xy[1],marker_pos[1]])
                self.marker_lines[mes.tag].set_visible(True)
                self.marker_lables[mes.tag].set_x(marker_pos[0])
                self.marker_lables[mes.tag].set_y(marker_pos[1])
                self.marker_lables[mes.tag].set_visible(True)
            self.marker_scatter.set_offsets(marker_pos_all)
        
        #Render Landmarks
        if self.landmarks is not None:
            self.landmarks_scatter.set_offsets(self.landmarks[self.cur_frame].transpose())
        
        #Render Robot Covariance Ellipse
        if self.robot_cov is not None:
            cov = self.robot_cov[self.cur_frame,:,:]
            a = cov[0,0]
            b = cov[0,1]
            c = cov[1,0]
            d = cov[1,1]
            B = -(a+d)
            C = (a*d-b*c)
            lam1 = (-B+np.sqrt(B**2-4*C))/2
            lam2 = (-B-np.sqrt(B**2-4*C))/2
            v1 = np.array([[lam1-d],[c]])
            self.robo_ell.width = lam1
            self.robo_ell.height = lam2
            self.robo_ell.angle = np.rad2deg(np.arccos(v1[0]/np.linalg.norm(v1)))
            self.robo_ell.set_center((self.state[self.cur_frame,0],self.state[self.cur_frame,1]))
        if self.marker_cov is not None:
            for i in range(self.landmarks[self.cur_frame].shape[1]):
                self.marker_ells[i].set_center((self.landmarks[self.cur_frame][0,i],self.landmarks[self.cur_frame][1,i]))
                cov = self.marker_cov[self.cur_frame][i*2:i*2+2,i*2:i*2+2]
                a = cov[0,0]
                b = cov[0,1]
                c = cov[1,0]
                d = cov[1,1]
                B = -(a+d)
                C = (a*d-b*c)
                lam1 = (-B+np.sqrt(B**2-4*C))/2
                lam2 = (-B-np.sqrt(B**2-4*C))/2
                v1 = np.array([[lam1-d],[c]])
                self.marker_ells[i].width=lam1
                self.marker_ells[i].height=lam2
                self.marker_ells[i].angle = np.rad2deg(np.arccos(v1[0]/np.linalg.norm(v1)))
            
        self.lock.release()
        
    def pause(self,b=None):
        self.paused = not self.paused
    
    def prv(self,b=None):
        self.paused = True
        self.cur_frame = int(self.cur_frame-1)
        self.slider.value = self.cur_frame
        if self.cur_frame < 0:
            self.cur_frame = 0
        self.render()
    
    def nxt(self,b=None):
        self.paused = True
        self.cur_frame = int(self.cur_frame + 1)
        self.slider.value = self.cur_frame
        if self.cur_frame >= self.state.shape[0]:
            self.cur_frame = self.state.shape[0]-1
        self.render()
    
    def slider_change(self,change):
        if self.paused == True:
            self.cur_frame = change['new']
            self.render()
