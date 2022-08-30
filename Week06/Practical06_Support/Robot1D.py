import numpy as np

class Robot1D(object):

    """
    A simple implementation of a 1D robot in state-space form
    The constant MAX_CONTROL bounds the magnitude of the control signal that can be applied to the robot 
    """

    MAX_CONTROL = 500
    
    def __init__(self, A=np.eye(2), B=np.array([[0],[0]]), C=np.array([0, 0]), initial_state=np.array([[10],[0]])):
        
        """
        Initialize a new model. 
        :param A: nxn state matrix, where n = state dimensionality
        :param B: nx1 input matrix, where n = state dimensionality
        :param C: 1xn input matrix, where n = state dimensionality
        :param initial_state: 2x1 vector with the initial state of our system
        """
        self.A = A
        self.B = B
        self.C = C
        self.state = initial_state
                
    def drive(self, control_u=10):
        """
        Update the system's state given a new control input
        :param control_u: Control input
        """
        # Make sure control signal is within -MAX_CONTROL < control_u < MAX_CONTROL
        clip_control = np.clip(control_u, -self.MAX_CONTROL, self.MAX_CONTROL)
        state_t1 = self.A @ self.state + self.B * clip_control
        self.state = state_t1
            
    def get_state(self):
        """
        Get the system's current state
        """
        return self.state
    
    def get_output(self):
        """
        Get the system's ouput (position of the robot along the 1D line)
        """
        return self.C @ self.state
                
    def get_error(self, desired_x):
        """
        This method measures the error (scalar) between the current robot's state and the desired state
        :param desired_x: Desired state (i.e., position) on the 1D line
        """
        return (desired_x - self.state)[0][0]